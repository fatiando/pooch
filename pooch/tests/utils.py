"""
Utilities for testing code.
"""
import os

from ..version import full_version
from ..utils import check_version


def check_tiny_data(fname):
    """
    Load the tiny-data.txt file and check that the contents are correct.
    """
    assert os.path.exists(fname)
    with open(fname) as tinydata:
        content = tinydata.read()
    true_content = "\n".join(
        ["# A tiny data file for test purposes only", "1  2  3  4  5  6"]
    )
    assert content.strip() == true_content


def pooch_test_url():
    """
    Get the base URL for the test data used in Pooch itself.

    The URL is a github raw link to the ``pooch/tests/data`` directory from the
    `Github repository <https://github.com/fatiando/pooch>`__. It matches the pooch
    version specified in ``pooch.version.full_version``.

    Returns
    -------
    url
        The versioned URL for pooch's test data.

    """
    url = "https://github.com/fatiando/pooch/raw/{version}/pooch/tests/data/".format(
        version=check_version(full_version)
    )
    return url


def pooch_test_registry():
    """
    Get a registry for the test data used in Pooch itself.

    Returns
    -------
    registry
        Dictionary with pooch's test data files and their hashes.

    """
    registry = {
        "tiny-data.txt": "baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d",
        "subdir/tiny-data.txt": "baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d",
    }
    return registry
