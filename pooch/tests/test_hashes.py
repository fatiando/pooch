# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the hash calculation and checking functions.
"""
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from ..core import Pooch
from ..hashes import (
    make_registry,
    file_hash,
    hash_matches,
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
TINY_DATA_HASHES_HASHLIB = {
    "sha1": "c03148994acd89317915ea2f2d080d6dd127aa09",
    "sha256": "baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d",
    "md5": "70e2afd3fd7e336ae478b1e740a5f08e",
}
TINY_DATA_HASHES_XXH = {
    "xxh128": "0267d220db258fffb0c567c0ecd1b689",
    "xxh3_128": "0267d220db258fffb0c567c0ecd1b689",
    "xxh64": "f843815fe57948fa",
    "xxh3_64": "811e3f2a12aec53f",
    "xxh32": "98d6f1a2",
}
TINY_DATA_HASHES = TINY_DATA_HASHES_HASHLIB.copy()
TINY_DATA_HASHES.update(TINY_DATA_HASHES_XXH)


def test_make_registry():
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


def test_make_registry_recursive():
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


def test_file_hash_invalid_algorithm():
    "Test an invalid hashing algorithm"
    with pytest.raises(ValueError) as exc:
        file_hash(fname="something", alg="blah")
    assert "'blah'" in str(exc.value)


@pytest.mark.parametrize(
    "alg,expected_hash",
    list(TINY_DATA_HASHES.items()),
    ids=list(TINY_DATA_HASHES.keys()),
)
def test_file_hash(alg, expected_hash):
    "Test the hash calculation using hashlib and xxhash"
    if alg.startswith("xxh"):
        pytest.importorskip("xxhash")
    fname = os.path.join(DATA_DIR, "tiny-data.txt")
    check_tiny_data(fname)
    returned_hash = file_hash(fname, alg)
    assert returned_hash == expected_hash


@pytest.mark.parametrize(
    "alg,expected_hash",
    list(TINY_DATA_HASHES.items()),
    ids=list(TINY_DATA_HASHES.keys()),
)
def test_hash_matches(alg, expected_hash):
    "Make sure the hash checking function works"
    if alg.startswith("xxh"):
        pytest.importorskip("xxhash")
    fname = os.path.join(DATA_DIR, "tiny-data.txt")
    check_tiny_data(fname)
    # Check if the check passes
    known_hash = f"{alg}:{expected_hash}"
    assert hash_matches(fname, known_hash)
    # And also if it fails
    known_hash = f"{alg}:blablablabla"
    assert not hash_matches(fname, known_hash)


@pytest.mark.parametrize(
    "alg,expected_hash",
    list(TINY_DATA_HASHES_HASHLIB.items()),
    ids=list(TINY_DATA_HASHES_HASHLIB.keys()),
)
def test_hash_matches_strict(alg, expected_hash):
    "Make sure the hash checking function raises an exception if strict"
    fname = os.path.join(DATA_DIR, "tiny-data.txt")
    check_tiny_data(fname)
    # Check if the check passes
    known_hash = f"{alg}:{expected_hash}"
    assert hash_matches(fname, known_hash, strict=True)
    # And also if it fails
    bad_hash = f"{alg}:blablablabla"
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


@pytest.mark.parametrize(
    "alg,expected_hash",
    list(TINY_DATA_HASHES_HASHLIB.items()),
    ids=list(TINY_DATA_HASHES_HASHLIB.keys()),
)
def test_hash_matches_uppercase(alg, expected_hash):
    "Hash matching should be independent of upper or lower case"
    fname = os.path.join(DATA_DIR, "tiny-data.txt")
    check_tiny_data(fname)
    # Check if the check passes
    known_hash = f"{alg}:{expected_hash.upper()}"
    assert hash_matches(fname, known_hash, strict=True)
    # And also if it fails
    with pytest.raises(ValueError) as error:
        hash_matches(fname, known_hash[:-5], strict=True, source="Neverland")
    assert "Neverland" in str(error.value)
