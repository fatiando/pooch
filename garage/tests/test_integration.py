# pylint: disable=redefined-outer-name
"""
Test the entire process of creating a garage and using it.
"""
import os
import shutil
from pathlib import Path
import warnings

import pytest

from .. import create, os_cache, __version__
from .utils import check_tiny_data


@pytest.fixture(scope="module")
def garage():
    "Create a garage the way most projects would."
    gar = create(
        path=os_cache("garage"),
        base_url="https://github.com/fatiando/garage/raw/{version}/data/",
        version=__version__,
        version_dev="master",
        env="GARAGE_DATA_DIR",
    )
    gar.load_registry(Path(os.path.dirname(__file__), "data", "registry.txt"))
    yield gar
    shutil.rmtree(gar.abspath)


def test_fetch(garage):
    "Fetch a data file from the garage"
    # Make sure the garage exists and is empty to begin
    assert garage.abspath.exists()
    assert not os.listdir(garage.abspath)
    with warnings.catch_warnings(record=True) as warn:
        fname = garage.fetch("tiny-data.txt")
        assert len(warn) == 1
        assert issubclass(warn[-1].category, UserWarning)
        assert str(warn[-1].message).split()[0] == "Downloading"
    check_tiny_data(fname)
    # Now modify the file to trigger an update on the next fetch
    with open(fname, "w") as fin:
        fin.write("The data is now different")
    with warnings.catch_warnings(record=True) as warn:
        fname = garage.fetch("tiny-data.txt")
        assert len(warn) == 1
        assert issubclass(warn[-1].category, UserWarning)
        assert str(warn[-1].message).split()[0] == "Updating"
    check_tiny_data(fname)
