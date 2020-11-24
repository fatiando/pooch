# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the utility functions.
"""
import os
import shutil
import hashlib
import time
from pathlib import Path
import tempfile
from tempfile import NamedTemporaryFile, TemporaryDirectory
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import pytest

from ..core import Pooch
from ..utils import (
    make_registry,
    parse_url,
    make_local_storage,
    file_hash,
    hash_matches,
    temporary_file,
    unique_file_name,
)
from .utils import check_tiny_data

DATA_DIR = str(Path(__file__).parent / "data" / "store")
REGISTRY = (
    "tiny-data.txt baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d\n"
)
REGISTRY_RECURSIVE = (
    "subdir/tiny-data.txt baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d\n"
    "tiny-data.txt baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d\n"
)


def test_unique_name_long():
    "The file name should never be longer than 255 characters"
    url = f"https://www.something.com/data{'a' * 500}.txt"
    assert len(url) > 255
    fname = unique_file_name(url)
    assert len(fname) == 255
    assert fname[-10:] == "aaaaaa.txt"
    assert fname.split("-")[1][:10] == "aaaaaaaaaa"


@pytest.mark.parametrize(
    "pool",
    [ThreadPoolExecutor, ProcessPoolExecutor],
    ids=["threads", "processes"],
)
def test_make_local_storage_parallel(pool, monkeypatch):
    "Try to create the cache folder in parallel"
    # Can cause multiple attempts at creating the folder which leads to an
    # exception. Check that this doesn't happen.
    # See https://github.com/fatiando/pooch/issues/170

    # Monkey path makedirs to make it delay before creating the directory.
    # Otherwise, the dispatch is too fast and the directory will exist before
    # another process tries to create it.

    # Need to keep a reference to the original function to avoid infinite
    # recursions from the monkey patching.
    makedirs = os.makedirs

    def mockmakedirs(path, exist_ok=False):  # pylint: disable=unused-argument
        "Delay before calling makedirs"
        time.sleep(1.5)
        makedirs(path, exist_ok=exist_ok)

    monkeypatch.setattr(os, "makedirs", mockmakedirs)

    data_cache = os.path.join(os.curdir, "test_parallel_cache")
    assert not os.path.exists(data_cache)

    try:
        with pool() as executor:
            futures = [
                executor.submit(make_local_storage, data_cache) for i in range(4)
            ]
            for future in futures:
                future.result()
            assert os.path.exists(data_cache)
    finally:
        if os.path.exists(data_cache):
            shutil.rmtree(data_cache)


def test_local_storage_makedirs_permissionerror(monkeypatch):
    "Should warn the user when can't create the local data dir"

    def mockmakedirs(path, exist_ok=False):  # pylint: disable=unused-argument
        "Raise an exception to mimic permission issues"
        raise PermissionError("Fake error")

    data_cache = os.path.join(os.curdir, "test_permission")
    assert not os.path.exists(data_cache)

    monkeypatch.setattr(os, "makedirs", mockmakedirs)

    with pytest.raises(PermissionError) as error:
        make_local_storage(
            path=data_cache,
            env="SOME_VARIABLE",
        )
        assert "Pooch could not create data cache" in str(error)
        assert "'SOME_VARIABLE'" in str(error)


def test_local_storage_newfile_permissionerror(monkeypatch):
    "Should warn the user when can't write to the local data dir"
    # This is a separate function because there should be a warning if the data
    # dir already exists but we can't write to it.

    def mocktempfile(**kwargs):  # pylint: disable=unused-argument
        "Raise an exception to mimic permission issues"
        raise PermissionError("Fake error")

    with TemporaryDirectory() as data_cache:
        os.makedirs(os.path.join(data_cache, "1.0"))
        assert os.path.exists(data_cache)

        monkeypatch.setattr(tempfile, "NamedTemporaryFile", mocktempfile)

        with pytest.raises(PermissionError) as error:
            make_local_storage(
                path=data_cache,
                env="SOME_VARIABLE",
            )
            assert "Pooch could not write to data cache" in str(error)
            assert "'SOME_VARIABLE'" in str(error)


def test_registry_builder():
    "Check that the registry builder creates the right file names and hashes"
    outfile = NamedTemporaryFile(delete=False)
    # Need to close the file before writing to it.
    outfile.close()
    try:
        make_registry(DATA_DIR, outfile.name, recursive=False)
        with open(outfile.name) as fout:
            registry = fout.read()
        assert registry == REGISTRY
        # Check that the registry can be used.
        pup = Pooch(path=DATA_DIR, base_url="some bogus URL", registry={})
        pup.load_registry(outfile.name)
        true = os.path.join(DATA_DIR, "tiny-data.txt")
        fname = pup.fetch("tiny-data.txt")
        assert true == fname
        check_tiny_data(fname)
    finally:
        os.remove(outfile.name)


def test_registry_builder_recursive():
    "Check that the registry builder works in recursive mode"
    outfile = NamedTemporaryFile(delete=False)
    # Need to close the file before writing to it.
    outfile.close()
    try:
        make_registry(DATA_DIR, outfile.name, recursive=True)
        with open(outfile.name) as fout:
            registry = fout.read()
        assert registry == REGISTRY_RECURSIVE
        # Check that the registry can be used.
        pup = Pooch(path=DATA_DIR, base_url="some bogus URL", registry={})
        pup.load_registry(outfile.name)
        assert os.path.join(DATA_DIR, "tiny-data.txt") == pup.fetch("tiny-data.txt")
        check_tiny_data(pup.fetch("tiny-data.txt"))
        true = os.path.join(DATA_DIR, "subdir", "tiny-data.txt")
        assert true == pup.fetch("subdir/tiny-data.txt")
        check_tiny_data(pup.fetch("subdir/tiny-data.txt"))
    finally:
        os.remove(outfile.name)


def test_parse_url():
    "Parse URL into 3 components"
    url = "http://127.0.0.1:8080/test.nc"
    assert parse_url(url) == {
        "protocol": "http",
        "netloc": "127.0.0.1:8080",
        "path": "/test.nc",
    }

    url = "ftp://127.0.0.1:8080/test.nc"
    assert parse_url(url) == {
        "protocol": "ftp",
        "netloc": "127.0.0.1:8080",
        "path": "/test.nc",
    }


def test_file_hash_invalid_algorithm():
    "Test an invalid hashing algorithm"
    with pytest.raises(ValueError) as exc:
        file_hash(fname="something", alg="blah")
    assert "'blah'" in str(exc.value)


@pytest.mark.parametrize("alg", ["sha256", "sha512", "md5"])
def test_hash_matches(alg):
    "Make sure the hash checking function works"
    fname = os.path.join(DATA_DIR, "tiny-data.txt")
    check_tiny_data(fname)
    with open(fname, "rb") as fin:
        data = fin.read()
    # Check if the check passes
    hasher = hashlib.new(alg)
    hasher.update(data)
    known_hash = f"{alg}:{hasher.hexdigest()}"
    assert hash_matches(fname, known_hash)
    # And also if it fails
    known_hash = f"{alg}:p98oh2dl2j2h2p8e9yfho3fi2e9fhd"
    assert not hash_matches(fname, known_hash)


@pytest.mark.parametrize("alg", ["sha256", "sha512", "md5"])
def test_hash_matches_strict(alg):
    "Make sure the hash checking function raises an exception if strict"
    fname = os.path.join(DATA_DIR, "tiny-data.txt")
    check_tiny_data(fname)
    with open(fname, "rb") as fin:
        data = fin.read()
    # Check if the check passes
    hasher = hashlib.new(alg)
    hasher.update(data)
    known_hash = f"{alg}:{hasher.hexdigest()}"
    assert hash_matches(fname, known_hash, strict=True)
    # And also if it fails
    bad_hash = f"{alg}:p98oh2dl2j2h2p8e9yfho3fi2e9fhd"
    with pytest.raises(ValueError) as error:
        hash_matches(fname, bad_hash, strict=True, source="Neverland")
    assert "Neverland" in str(error.value)
    with pytest.raises(ValueError) as error:
        hash_matches(fname, bad_hash, strict=True, source=None)
    assert fname in str(error.value)


def test_hash_matches_none():
    "The hash checking function should always returns True if known_hash=None"
    fname = os.path.join(DATA_DIR, "tiny-data.txt")
    assert hash_matches(fname, known_hash=None)
    # Should work even if the file is invalid
    assert hash_matches(fname="", known_hash=None)
    # strict should cause an error if this wasn't working
    assert hash_matches(fname, known_hash=None, strict=True)


@pytest.mark.parametrize("alg", ["sha256", "sha512", "md5"])
def test_hash_matches_uppercase(alg):
    "Hash matching should be independent of upper or lower case"
    fname = os.path.join(DATA_DIR, "tiny-data.txt")
    check_tiny_data(fname)
    with open(fname, "rb") as fin:
        data = fin.read()
    # Check if the check passes
    hasher = hashlib.new(alg)
    hasher.update(data)
    known_hash = f"{alg}:{hasher.hexdigest().upper()}"
    assert hash_matches(fname, known_hash, strict=True)
    # And also if it fails
    with pytest.raises(ValueError) as error:
        hash_matches(fname, known_hash[:-5], strict=True, source="Neverland")
    assert "Neverland" in str(error.value)


def test_temporary_file():
    "Make sure the file is writable and cleaned up in the end"
    with temporary_file() as tmp:
        assert Path(tmp).exists()
        with open(tmp, "w") as outfile:
            outfile.write("Meh")
        with open(tmp) as infile:
            assert infile.read().strip() == "Meh"
    assert not Path(tmp).exists()


def test_temporary_file_path():
    "Make sure the file is writable and cleaned up in the end when given a dir"
    with TemporaryDirectory() as path:
        with temporary_file(path) as tmp:
            assert Path(tmp).exists()
            assert path in tmp
            with open(tmp, "w") as outfile:
                outfile.write("Meh")
            with open(tmp) as infile:
                assert infile.read().strip() == "Meh"
        assert not Path(tmp).exists()


def test_temporary_file_exception():
    "Make sure the file is writable and cleaned up when there is an exception"
    try:
        with temporary_file() as tmp:
            assert Path(tmp).exists()
            raise ValueError("Nooooooooo!")
    except ValueError:
        assert not Path(tmp).exists()
