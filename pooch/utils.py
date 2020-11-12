# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
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
        raise ValueError(f"Algorithm '{alg}' not available in hashlib")
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


def cache_location(path, env=None, version=None):
    """
    Location of the cache given a base path and optional configuration.

    Checks for the environment variable to overwrite the path of the local
    cache. Optionally add *version* to the path if given.

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
    return Path(path)


def make_local_storage(path, env=None):
    """
    Create the local cache directory and make sure it's writable.

    Parameters
    ----------
    path : str or PathLike
        The path to the local data storage folder.
    env : str or None
        An environment variable that can be used to overwrite *path*. Only used
        in the error message in case the folder is not writable.
    """
    path = str(path)
    # Check that the data directory is writable
    try:
        if not os.path.exists(path):
            action = "create"
            # When running in parallel, it's possible that multiple jobs will
            # try to create the path at the same time. Use exist_ok to avoid
            # raising an error.
            os.makedirs(path, exist_ok=True)
        else:
            action = "write to"
            with tempfile.NamedTemporaryFile(dir=path):
                pass
    except PermissionError as error:
        message = [
            str(error),
            f"| Pooch could not {action} data cache folder '{path}'.",
            "Will not be able to download data files.",
        ]
        if env is not None:
            message.append(
                f"Use environment variable '{env}' to specify a different location."
            )
        raise PermissionError(" ".join(message)) from error


def hash_algorithm(hash_string):
    """
    Parse the name of the hash method from the hash string.

    The hash string should have the following form ``algorithm:hash``, where
    algorithm can be the name of any algorithm known to :mod:`hashlib`.

    If the algorithm is omitted or the hash string is None, will default to
    ``"sha256"``.

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
    >>> print(hash_algorithm("SHA256:qouuwhwd2j192y1lb1iwgowdj2898wd2d9"))
    sha256
    >>> print(hash_algorithm(None))
    sha256

    """
    default = "sha256"
    if hash_string is None:
        algorithm = default
    elif ":" not in hash_string:
        algorithm = default
    else:
        algorithm = hash_string.split(":")[0]
    return algorithm.lower()


def hash_matches(fname, known_hash, strict=False, source=None):
    """
    Check if the hash of a file matches a known hash.

    If the *known_hash* is None, will always return True.

    Coverts hashes to lowercase before comparison to avoid system specific
    mismatches between hashes in the registry and computed hashes.

    Parameters
    ----------
    fname : str or PathLike
        The path to the file.
    known_hash : str
        The known hash. Optionally, prepend ``alg:`` to the hash to specify the
        hashing algorithm. Default is SHA256.
    strict : bool
        If True, will raise a :class:`ValueError` if the hash does not match
        informing the user that the file may be corrupted.
    source : str
        The source of the downloaded file (name or URL, for example). Will be
        used in the error message if *strict* is True. Has no other use other
        than reporting to the user where the file came from in case of hash
        mismatch. If None, will default to *fname*.

    Returns
    -------
    is_same : bool
        True if the hash matches, False otherwise.

    """
    if known_hash is None:
        return True
    algorithm = hash_algorithm(known_hash)
    new_hash = file_hash(fname, alg=algorithm)
    matches = new_hash.lower() == known_hash.split(":")[-1].lower()
    if strict and not matches:
        if source is None:
            source = str(fname)
        raise ValueError(
            f"{algorithm.upper()} hash of downloaded file ({source}) does not match"
            f" the known hash: expected {known_hash} but got {new_hash}. Deleted"
            " download for safety. The downloaded file may have been corrupted or"
            " the known hash may be outdated."
        )
    return matches


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
    fname : str
        The path to the temporary file.

    """
    tmp = tempfile.NamedTemporaryFile(delete=False, dir=path)
    # Close the temp file so that it can be opened elsewhere
    tmp.close()
    try:
        yield tmp.name
    finally:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)


def unique_file_name(url):
    """
    Create a unique file name based on the given URL.

    The file name will be unique to the URL by prepending the name with the MD5
    hash (hex digest) of the URL. The name will also include the last portion
    of the URL.

    The format will be: ``{md5}-{filename}.{ext}``

    The file name will be cropped so that the entire name (including the hash)
    is less than 255 characters long (the limit on most file systems).

    Parameters
    ----------
    url : str
        The URL with a file name at the end.

    Returns
    -------
    fname : str
        The file name, unique to this URL.

    Examples
    --------

    >>> print(unique_file_name("https://www.some-server.org/2020/data.txt"))
    02ddee027ce5ebb3d7059fb23d210604-data.txt
    >>> print(unique_file_name("https://www.some-server.org/2019/data.txt"))
    9780092867b497fca6fc87d8308f1025-data.txt
    >>> print(unique_file_name("https://www.some-server.org/2020/data.txt.gz"))
    181a9d52e908219c2076f55145d6a344-data.txt.gz

    """
    md5 = hashlib.md5(url.encode()).hexdigest()
    fname = parse_url(url)["path"].split("/")[-1]
    # Crop the start of the file name to fit 255 characters including the hash
    # and the :
    fname = fname[-(255 - len(md5) - 1) :]
    unique_name = f"{md5}-{fname}"
    return unique_name
