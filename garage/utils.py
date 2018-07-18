"""
Misc utilities
"""
from packaging.version import Version
import hashlib


def file_hash(fname):
    """
    Calculate the SHA256 hash of a given file.

    Useful for checking if a file has changed or been corrupted.

    Parameters
    ----------
    fname : str
        The name of the file.

    Returns
    -------
    hash : str
        The hash of the file.

    Examples
    --------

    >>> fname = "test-file-for-hash.txt"
    >>> with open(fname, "w") as f:
    ...     __ = f.write("content of the file")
    >>> print(file_hash(fname))
    0fc74468e6a9a829f103d069aeb2bb4f8646bad58bf146bb0e3379b759ec4a00
    >>> import os
    >>> os.remove(fname)

    """
    # Calculate the hash in chunks to avoid overloading the memory
    chunksize = 65536
    hasher = hashlib.sha256()
    with open(fname, "rb") as fin:
        buff = fin.read(chunksize)
        while len(buff) > 0:
            hasher.update(buff)
            buff = fin.read(chunksize)
    file_hash = hasher.hexdigest()
    return file_hash


def check_version(version, fallback="master"):
    """
    Check that a version string is PEP440 compliant and there are no unreleased changes.

    For example, ``version = "0.1"`` will be returned as is but
    ``version = "0.1+10.8dl8dh9"`` will return the fallback. This is the convention used
    by `versioneer <https://github.com/warner/python-versioneer>`__ to mark that this
    version is 10 commits ahead of the last release.

    Parameters
    ----------
    version : str
        A version string.
    fallback : str
        What to return if the version string has unreleased changes.

    Returns
    -------
    version : str
        If *version* is PEP440 compliant and there are unreleased changes, then return
        *version*. Otherwise, return *fallback*.

    Raises
    ------
    InvalidVersion
        If *version* is not PEP440 compliant.

    Examples
    --------

    >>> check_version("0.1")
    '0.1'
    >>> check_version("0.1a10")
    '0.1a10'
    >>> check_version("0.1+111.9hdg36")
    'master'
    >>> check_version("0.1+111.9hdg36", fallback="dev")
    'dev'
    >>> check_version("not compliant")
    Traceback (most recent call last):
        ...
    packaging.version.InvalidVersion: Invalid version: 'not compliant'

    """
    parse = Version(version)
    if parse.local is not None:
        return fallback
    return version
