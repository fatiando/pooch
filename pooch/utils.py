"""
Misc utilities
"""
import os
from pathlib import Path
import sys
import hashlib

from packaging.version import Version


def os_cache(project, platform=None):
    """
    Default cache location based on the operating system.

    Will insert the project name in the proper location of the path.

    Parameters
    ----------
    project : str
        The project name.
    platform : str or None
        The name of operating system as returned by ``sys.platform`` (``'darwin'`` for
        Mac, ``'win32'`` for Windows, and anything else will be treated as generic
        Linux/Unix. If None, will use the value of ``sys.platform``.

    Returns
    -------
    cache_path : :class:`pathlib.Path`
        The default location for the data cache. User directories (``'~'``) are not
        expanded.

    Examples
    --------

    >>> for os in ['darwin', 'win32', 'anything else']:
    ...     path = os_cache("myproject", platform=os)
    ...     print(path.parts)
    ('~', 'Library', 'Caches', 'myproject')
    ('~', 'AppData', 'Local', 'myproject', 'cache')
    ('~', '.cache', 'myproject')

    """
    if platform is None:
        platform = sys.platform
    if platform == "darwin":
        cache_path = Path("~", "Library", "Caches", project)
    elif platform == "win32":
        cache_path = Path("~", "AppData", "Local", project, "cache")
    else:  # *NIX
        cache_path = Path("~", ".cache", project)
    return cache_path


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
        while buff:
            hasher.update(buff)
            buff = fin.read(chunksize)
    return hasher.hexdigest()


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


def make_file_registry(directory, output, recursive=True):
    """
    Make a registry of files and hashes for the given directory.

    This is helpful if you have many files in your test dataset as it keeps you
    from needing to manually update the registry.

    Parameters
    ----------
    directory : str
        Directory of the test data to put in the registry.
    output : str
        File to write for the registry of files.
    recursive : bool
        If we should recursively follow subdirectories of directory.

    """
    if recursive:
        files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(directory)) for f in fn]
    else:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Get the hash of each of the files
    hashes = [file_hash(f) for f in files]

    # Write out the files and hashes to the desired file
    outfile = open(output, 'w')
    for f, h in zip(files, hashes):
        outfile.write('{} {}\n'.format(f, h))
    outfile.close()