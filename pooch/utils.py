"""
Misc utilities
"""
from pathlib import Path
import hashlib

import appdirs
from packaging.version import Version


def os_cache(project):
    r"""
    Default cache location based on the operating system.

    The folder locations are defined by the ``appdirs``  package.
    Usually, the locations will be following (see the
    `appdirs documentation <https://github.com/ActiveState/appdirs>`__):

    * Mac: ``~/Library/Application Support/<project>``
    * Unix: ``~/.local/share/<project>`` or the value of the ``XDG_DATA_HOME``
      environment variable, if defined.
    * Windows: ``C:\Users\<user>\AppData\Roaming\<project>\<project>``

    Parameters
    ----------
    project : str
        The project name.

    Returns
    -------
    cache_path : :class:`pathlib.Path`
        The default location for the data cache. User directories (``'~'``) are not
        expanded.

    """
    return Path(appdirs.user_cache_dir(project))


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

    """
    parse = Version(version)
    if parse.local is not None:
        return fallback
    return version


def make_registry(directory, output, recursive=True):
    """
    Make a registry of files and hashes for the given directory.

    This is helpful if you have many files in your test dataset as it keeps you
    from needing to manually update the registry.

    Parameters
    ----------
    directory : str
        Directory of the test data to put in the registry. All file names in the
        registry will be relative to this directory.
    output : str
        Name of the output registry file.
    recursive : bool
        If True, will recursively look for files in subdirectories of *directory*.

    """
    directory = Path(directory)
    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"

    files = sorted(
        [
            str(path.relative_to(directory))
            for path in directory.glob(pattern)
            if path.is_file()
        ]
    )

    hashes = [file_hash(str(directory / fname)) for fname in files]

    with open(output, "w") as outfile:
        for fname, fhash in zip(files, hashes):
            # Only use Unix separators for the registry so that we don't go insane
            # dealing with file paths.
            outfile.write("{} {}\n".format(fname.replace("\\", "/"), fhash))
