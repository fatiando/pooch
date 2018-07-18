"""
Test the Garage class.
"""
import os

import pytest

from .. import Garage

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
REGISTRY = {
    "tiny-data.txt": "baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d"
}


def test_garage_local():
    "Setup a garage that already has the local data and test the fetch."
    garage = Garage(path=DATA_DIR, base_url="some bogus URL", registry=REGISTRY)
    true = os.path.join(os.path.abspath(DATA_DIR), "tiny-data.txt")
    fname = garage.fetch("tiny-data.txt")
    assert true == fname
    assert os.path.exists(fname)
    with open(fname) as tinydata:
        content = tinydata.read()
    true_content = "\n".join(
        ["# A tiny data file for test purposes only", "1  2  3  4  5  6"]
    )
    assert content.strip() == true_content


def test_garage_file_not_in_registry():
    "Should raise an exception if the file is not in the registry."
    garage = Garage(
        path="it shouldn't matter", base_url="this shouldn't either", registry=REGISTRY
    )
    with pytest.raises(ValueError):
        garage.fetch("this-file-does-not-exit.csv")


def test_garage_load_registry():
    "Loading the registry from a file should work"
    garage = Garage(path="", base_url="", registry={})
    garage.load_registry(os.path.join(DATA_DIR, "registry.txt"))
    assert garage.registry == REGISTRY


def test_garage_load_registry_invalid_line():
    "Should raise an exception when a line doesn't have two elements"
    garage = Garage(path="", base_url="", registry={})
    with pytest.raises(ValueError):
        garage.load_registry(os.path.join(DATA_DIR, "registry-invalid.txt"))
