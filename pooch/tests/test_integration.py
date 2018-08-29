# pylint: disable=redefined-outer-name
"""
Test the entire process of creating a Pooch and using it.
"""
import os
import shutil
from pathlib import Path
import warnings

import pytest

from .. import create, os_cache
from ..version import full_version
from .utils import check_tiny_data


@pytest.fixture
def pup():
    "Create a pooch the way most projects would."
    doggo = create(
        path=os_cache("pooch"),
        base_url="https://github.com/fatiando/pooch/raw/{version}/data/",
        version=full_version,
        version_dev="master",
        env="POOCH_DATA_DIR",
    )
    # The str conversion is needed in Python 3.5
    doggo.load_registry(str(Path(os.path.dirname(__file__), "data", "registry.txt")))
    if os.path.exists(str(doggo.abspath)):
        shutil.rmtree(str(doggo.abspath))
    yield doggo
    shutil.rmtree(str(doggo.abspath))


def test_fetch(pup):
    "Fetch a data file from the local storage"
    # Make sure the storage has been cleaned up before running the tests
    assert not pup.abspath.exists()
    for target in ["tiny-data.txt", "subdir/tiny-data.txt"]:
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch(target)
            assert len(warn) == 1
            assert issubclass(warn[-1].category, UserWarning)
            assert str(warn[-1].message).split()[0] == "Downloading"
        check_tiny_data(fname)
        # Now modify the file to trigger an update on the next fetch
        with open(fname, "w") as fin:
            fin.write("The data is now different")
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch(target)
            assert len(warn) == 1
            assert issubclass(warn[-1].category, UserWarning)
            assert str(warn[-1].message).split()[0] == "Updating"
        check_tiny_data(fname)
