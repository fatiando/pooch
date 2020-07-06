# pylint: disable=missing-docstring,import-outside-toplevel
# Import functions/classes to make the API
from . import version
from .core import Pooch, create, retrieve
from .utils import os_cache, file_hash, make_registry, check_version, get_logger
from .downloaders import HTTPDownloader, FTPDownloader, SFTPDownloader
from .processors import Unzip, Untar, Decompress


__version__ = version.full_version


def test(doctest=True, verbose=True, coverage=False):
    """
    Run the test suite.

    Uses `py.test <http://pytest.org/>`__ to discover and run the tests.

    Parameters
    ----------

    doctest : bool
        If ``True``, will run the doctests as well (code examples that start
        with a ``>>>`` in the docs).
    verbose : bool
        If ``True``, will print extra information during the test run.
    coverage : bool
        If ``True``, will run test coverage analysis on the code as well.
        Requires ``pytest-cov``.

    Raises
    ------

    AssertionError
        If pytest returns a non-zero error code indicating that some tests have
        failed.

    """
    import pytest

    package = __name__
    args = []
    if verbose:
        args.append("-vv")
    if coverage:
        args.append("--cov={}".format(package))
        args.append("--cov-report=term-missing")
    if doctest:
        args.append("--doctest-modules")
    args.append("--pyargs")
    args.append(package)
    status = pytest.main(args)
    assert status == 0, "Some tests have failed."
