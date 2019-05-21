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
        "tiny-data.zip": "0d49e94f07bc1866ec57e7fd1b93a351fba36842ec9b13dd50bf94e8dfa35cbb",
        "store.zip": "0498d2a001e71051bbd2acd2346f38da7cbd345a633cb7bf0f8a20938714b51a",
        "tiny-data.tar.gz": "41503f083814f43a01a8e9a30c28d7a9fe96839a99727a7fdd0acf7cd5bab63b",
        "store.tar.gz": "088c7f4e0f1859b1c769bb6065de24376f366374817ede8691a6ac2e49f29511",
        "tiny-data.txt.bz2": "753663687a4040c90c8578061867d1df623e6aa8011c870a5dbd88ee3c82e306",
        "tiny-data.txt.gz": "2e2da6161291657617c32192dba95635706af80c6e7335750812907b58fd4b52",
        "tiny-data.txt.xz": "99dcb5c32a6e916344bacb4badcbc2f2b6ee196977d1d8187610c21e7e607765",
    }
    return registry
