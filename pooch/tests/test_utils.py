"""
Test the utility functions.
"""
import os
import hashlib
from pathlib import Path
import tempfile
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from ..core import Pooch
from ..utils import (
    make_registry,
    parse_url,
    make_local_storage,
    file_hash,
    hash_matches,
)
from .utils import check_tiny_data, capture_log

DATA_DIR = str(Path(__file__).parent / "data" / "store")
REGISTRY = (
    "tiny-data.txt baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d\n"
)
REGISTRY_RECURSIVE = (
    "subdir/tiny-data.txt baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d\n"
    "tiny-data.txt baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d\n"
)


def test_local_storage_makedirs_permissionerror(monkeypatch):
    "Should warn the user when can't create the local data dir"

    def mockmakedirs(path, exist_ok=False):  # pylint: disable=unused-argument
        "Raise an exception to mimic permission issues"
        raise PermissionError("Fake error")

    data_cache = os.path.join(os.curdir, "test_permission")
    assert not os.path.exists(data_cache)

    monkeypatch.setattr(os, "makedirs", mockmakedirs)

    with capture_log() as log_file:
        make_local_storage(
            path=data_cache, version="1.0", env="SOME_VARIABLE",
        )
        logs = log_file.getvalue()
        assert logs.startswith("Cannot create data cache")
        assert "'SOME_VARIABLE'" in logs


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

        with capture_log() as log_file:
            make_local_storage(
                path=data_cache, version="1.0", env="SOME_VARIABLE",
            )
            logs = log_file.getvalue()
            assert logs.startswith("Cannot write to data cache")
            assert "'SOME_VARIABLE'" in logs


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


def test_hash_matches():
    "Make sure the hash checking function works"
    fname = os.path.join(DATA_DIR, "tiny-data.txt")
    check_tiny_data(fname)
    with open(fname, "rb") as fin:
        data = fin.read()
    # Check if the check passes
    hasher = hashlib.new("sha256")
    hasher.update(data)
    known_hash = "{}".format(hasher.hexdigest())
    assert hash_matches(fname, known_hash)
    for alg in ("sha512", "md5"):
        hasher = hashlib.new(alg)
        hasher.update(data)
        known_hash = "{}:{}".format(alg, hasher.hexdigest())
        assert hash_matches(fname, known_hash)
    # And also if it fails
    known_hash = "p98oh2dl2j2h2p8e9yfho3fi2e9fhd"
    assert not hash_matches(fname, known_hash)
    for alg in ("sha512", "md5"):
        known_hash = "{}:p98oh2dl2j2h2p8e9yfho3fi2e9fhd".format(alg)
        assert not hash_matches(fname, known_hash)
