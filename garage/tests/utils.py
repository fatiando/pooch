"""
Utilities for testing code.
"""
from .. import __version__
from ..utils import check_version


def garage_test_url():
    """
    Get the base URL for the test data used in garage itself.

    The URL is a github raw link to the ``garage/tests/data`` directory from the
    `Github repository <https://github.com/fatiando/garage>`__. It matches the garage
    version specified in ``garage.__version__``.

    Returns
    -------
    url
        The versioned URL for garage's test data.

    """
    url = "https://github.com/fatiando/garage/raw/{version}/garage/tests/data/".format(
        version=check_version(__version__)
    )
    return url


def garage_test_registry():
    """
    Get a registry for the test data used in garage itself.

    Returns
    -------
    registry
        Dictionary with garage's test data files and their hashes.

    """
    sha256 = "baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d"
    registry = {"tiny-data.txt": sha256}
    return registry
