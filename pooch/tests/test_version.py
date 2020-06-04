"""
Test the version.
"""
import pooch


def test_version():
    "Check there's a usable version number in the usual __version__"
    assert pooch.__version__.startswith("v")
