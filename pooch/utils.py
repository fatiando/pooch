"""
Misc utilities
"""
import logging
import os
import tempfile
from pathlib import Path
import hashlib
from urllib.parse import urlsplit
from contextlib import contextmanager

import appdirs
from packaging.version import Version


LOGGER = logging.Logger("pooch")
LOGGER.addHandler(logging.StreamHandler())


def get_logger():
    r"""
    Get the default event logger.

    The logger records events like downloading files, unzipping archives, etc.
    Use the method :meth:`logging.Logger.setLevel` of this object to adjust the
    verbosity level from Pooch.

    Returns
    -------
    logger : :class:`logging.Logger`
        The logger object for Pooch
    """
    return LOGGER


def os_cache(project):
    r"""
    Default cache location based on the operating system.

    The folder locations are defined by the ``appdirs``  package
    using the ``user_cache_dir`` function.
    Usually, the locations will be following (see the
    `appdirs documentation <https://github.com/ActiveState/appdirs>`__):

    * Mac: ``~/Library/Caches/<AppName>``
    * Unix: ``~/.cache/<AppName>`` or the value of the ``XDG_CACHE_HOME``
      environment variable, if defined.
    * Windows: ``C:\Users\<user>\AppData\Local\<AppAuthor>\<AppName>\Cache``

    Parameters
    ----------
    project : str
        The project name.

    Returns
    -------
    cache_path : :class:`pathlib.Path`
        The default location for the data cache. User directories (``'~'``) are
        not expanded.

    """
    return Path(appdirs.user_cache_dir(project))


def file_hash(fname, alg="sha256"):
    """
    Calculate the hash of a given file.

    Useful for checking if a file has changed or been corrupted.

    Parameters
    ----------
    fname : str
        The name of the file.
    alg : str
        The type of the hashing algorithm

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
    if alg not in hashlib.algorithms_available:
        raise ValueError("Algorithm '{}' not available in hashlib".format(alg))
    # Calculate the hash in chunks to avoid overloading the memory
    chunksize = 65536
    hasher = hashlib.new(alg)
    with open(fname, "rb") as fin:
        buff = fin.read(chunksize)
        while buff:
            hasher.update(buff)
            buff = fin.read(chunksize)
    return hasher.hexdigest()


def check_version(version, fallback="master"):
    """
    Check if a version is PEP440 compliant and there are no unreleased changes.

    For example, ``version = "0.1"`` will be returned as is but ``version =
    "0.1+10.8dl8dh9"`` will return the fallback. This is the convention used by
    `versioneer <https://github.com/warner/python-versioneer>`__ to mark that
    this version is 10 commits ahead of the last release.

    Parameters
    ----------
    version : str
        A version string.
    fallback : str
        What to return if the version string has unreleased changes.

    Returns
    -------
    version : str
        If *version* is PEP440 compliant and there are unreleased changes, then
        return *version*. Otherwise, return *fallback*.

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
        Directory of the test data to put in the registry. All file names in
        the registry will be relative to this directory.
    output : str
        Name of the output registry file.
    recursive : bool
        If True, will recursively look for files in subdirectories of
        *directory*.

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
            # Only use Unix separators for the registry so that we don't go
            # insane dealing with file paths.
            outfile.write("{} {}\n".format(fname.replace("\\", "/"), fhash))


def parse_url(url):
    """
    Parse a URL into 3 components:

    <protocol>://<netloc>/<path>

    Parameters
    ----------
    url : str
        URL (e.g.: http://127.0.0.1:8080/test.nc, ftp://127.0.0.1:8080/test.nc)

    Returns
    -------
    parsed_url : dict
        Three components of a URL (e.g., {'protocol': 'http', 'netloc':
        '127.0.0.1:8080', 'path': '/test.nc'})

    """
    parsed_url = urlsplit(url)
    protocol = parsed_url.scheme or "file"
    return {"protocol": protocol, "netloc": parsed_url.netloc, "path": parsed_url.path}


def make_local_storage(path, env=None, version=None):
    """
    Create the local cache directory and make sure it's writable.

    If the directory doesn't exist, it will be created.

    Parameters
    ----------
    path : str, PathLike, list or tuple
        The path to the local data storage folder. If this is a list or tuple,
        we'll join the parts with the appropriate separator. Use
        :func:`pooch.os_cache` for a sensible default.
    version : str or None
        The version string for your project. Will be appended to given path if
        not None.
    env : str or None
        An environment variable that can be used to overwrite *path*. This
        allows users to control where they want the data to be stored. We'll
        append *version* to the end of this value as well.

    Returns
    -------
    local_path : PathLike
        The path to the local directory.

    """
    if env is not None and env in os.environ and os.environ[env]:
        path = os.environ[env]
    if isinstance(path, (list, tuple)):
        path = os.path.join(*path)
    if version is not None:
        path = os.path.join(str(path), version)
    path = os.path.expanduser(str(path))
    # Check that the data directory is writable
    try:
        if not os.path.exists(path):
            action = "create"
            os.makedirs(path)
        else:
            action = "write to"
            with tempfile.NamedTemporaryFile(dir=path):
                pass
    except PermissionError:
        message = (
            "Cannot %s data cache folder '%s'. "
            "Will not be able to download remote data files. "
        )
        args = [action, path]
        if env is not None:
            message += "Use environment variable '%s' to specify another directory."
            args += [env]

        get_logger().warning(message, *args)
    return Path(path)


def hash_algorithm(hash_string):
    """
    Parse the name of the hash method from the hash string.

    The hash string should have the following form ``algorithm:hash``, where
    algorithm can be the name of any algorithm known to :mod:`hashlib`.

    If the algorithm is omitted, will default to ``"sha256"``.

    Parameters
    ----------
    hash_string : str
        The hash string with optional algorithm prepended.

    Returns
    -------
    hash_algorithm : str
        The name of the algorithm.

    Examples
    --------

    >>> print(hash_algorithm("qouuwhwd2j192y1lb1iwgowdj2898wd2d9"))
    sha256
    >>> print(hash_algorithm("md5:qouuwhwd2j192y1lb1iwgowdj2898wd2d9"))
    md5
    >>> print(hash_algorithm("sha256:qouuwhwd2j192y1lb1iwgowdj2898wd2d9"))
    sha256

    """
    parts = hash_string.split(":")
    if len(parts) == 1:
        algorithm = "sha256"
    else:
        algorithm = parts[0]
    return algorithm


def hash_matches(fname, known_hash):
    """
    Check if the hash of a file matches a known hash.

    Parameters
    ----------
    fname : str or PathLike
        The path to the file.
    known_hash : str
        The known hash. Optionally, prepend ``alg:`` to the hash to specify the
        hashing algorithm. Default is SHA256.

    Returns
    -------
    is_same : bool
        True if the hash matches, False otherwise.

    """
    new_hash = file_hash(fname, alg=hash_algorithm(known_hash))
    return new_hash == known_hash.split(":")[-1]


@contextmanager
def temporary_file(path=None):
    """
    Create a closed and named temporary file and make sure it's cleaned up.

    Using :class:`tempfile.NamedTemporaryFile` will fail on Windows if trying
    to open the file a second time (when passing its name to Pooch function,
    for example). This context manager creates the file, closes it, yields the
    file path, and makes sure it's deleted in the end.

    Parameters
    ----------
    path : str or PathLike
        The directory in which the temporary file will be created.

    Yields
    ------
    fname : PathLike
        A :mod:`pathlib` object with the path to the temporary file.

    """
    tmp = tempfile.NamedTemporaryFile(delete=False, dir=path)
    # Close the temp file so that it can be opened elsewhere
    tmp.close()
    try:
        yield Path(tmp.name)
    finally:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)
