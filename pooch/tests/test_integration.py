# pylint: disable=redefined-outer-name
"""
Test the entire process of creating a Pooch and using it.
"""
import os
import shutil
from pathlib import Path

import pytest

from .. import create, os_cache
from ..version import full_version
from .utils import check_tiny_data, capture_log


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
        with capture_log() as log_file:
            fname = pup.fetch(target)
            assert log_file.getvalue().split()[0] == "Downloading"
        check_tiny_data(fname)
        # Now modify the file to trigger an update on the next fetch
        with open(fname, "w") as fin:
            fin.write("The data is now different")
        with capture_log() as log_file:
            fname = pup.fetch(target)
            assert log_file.getvalue().split()[0] == "Updating"
        check_tiny_data(fname)
