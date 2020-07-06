"""
Test the version.
"""
from packaging.version import Version

import pooch


def test_version():
    "Check there's a usable version number in the usual __version__"
    assert pooch.__version__.startswith("v")
    # Check that it's PEP440 compliant (will raise an exception otherwise)
    Version(pooch.__version__)
