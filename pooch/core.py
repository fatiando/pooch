"""
Functions to download, verify, and update a sample dataset.
"""
import os
import sys
from pathlib import Path
import shutil
import tempfile
from warnings import warn

import requests

from .utils import file_hash, check_version


# PermissionError was introduced in Python 3.3. This can be deleted when dropping 2.7
if sys.version_info[0] < 3:
    PermissionError = OSError  # pylint: disable=redefined-builtin,invalid-name


def create(
    path,
    base_url,
    version=None,
    version_dev="master",
    env=None,
    registry=None,
    urls=None,
):
    """
    Create a new :class:`~pooch.Pooch` with sensible defaults to fetch data files.

    If a version string is given, the Pooch will be versioned, meaning that the local
    storage folder and the base URL depend on the projection version. This is necessary
    if your users have multiple versions of your library installed (using virtual
    environments) and you updated the data files between versions. Otherwise, every time
    a user switches environments would trigger a re-download of the data. The version
    string will be appended to the local storage path (for example,
    ``~/.mypooch/cache/v0.1``) and inserted into the base URL (for example,
    ``https://github.com/fatiando/pooch/raw/v0.1/data``). If the version string contains
    ``+XX.XXXXX``, it will be interpreted as a development version.

    Parameters
    ----------
    path : str, PathLike, list or tuple
        The path to the local data storage folder. If this is a list or tuple, we'll
        join the parts with the appropriate separator. The *version* will be appended to
        the end of this path. Use :func:`pooch.os_cache` for a sensible default.
    base_url : str
        Base URL for the remote data source. All requests will be made relative to this
        URL. The string should have a ``{version}`` formatting mark in it. We will call
        ``.format(version=version)`` on this string. If the URL is a directory path, it
        must end in a ``'/'`` because we will not include it.
    version : str or None
        The version string for your project. Should be PEP440 compatible. If None is
        given, will not attempt to format *base_url* and no subfolder will be appended
        to *path*.
    version_dev : str
        The name used for the development version of a project. If your data is hosted
        on Github (and *base_url* is a Github raw link), then ``"master"`` is a good
        choice (default). Ignored if *version* is None.
    env : str or None
        An environment variable that can be used to overwrite *path*. This allows users
        to control where they want the data to be stored. We'll append *version* to the
        end of this value as well.
    registry : dict or None
        A record of the files that are managed by this Pooch. Keys should be the file
        names and the values should be their SHA256 hashes. Only files in the registry
        can be fetched from the local storage. Files in subdirectories of *path* **must
        use Unix-style separators** (``'/'``) even on Windows.
    urls : dict or None
        Custom URLs for downloading individual files in the registry. A dictionary with
        the file names as keys and the custom URLs as values. Not all files in
        *registry* need an entry in *urls*. If a file has an entry in *urls*, the
        *base_url* will be ignored when downloading it in favor of ``urls[fname]``.


    Returns
    -------
    pooch : :class:`~pooch.Pooch`
        The :class:`~pooch.Pooch` initialized with the given arguments.

    Examples
    --------

    Create a :class:`~pooch.Pooch` for a release (v0.1):

    >>> pup = create(path="myproject",
    ...              base_url="http://some.link.com/{version}/",
    ...              version="v0.1",
    ...              registry={"data.txt": "9081wo2eb2gc0u..."})
    >>> print(pup.path.parts)  # The path is a pathlib.Path
    ('myproject', 'v0.1')
    >>> print(pup.base_url)
    http://some.link.com/v0.1/
    >>> print(pup.registry)
    {'data.txt': '9081wo2eb2gc0u...'}

    If this is a development version (12 commits ahead of v0.1), then the
    ``version_dev`` will be used (defaults to ``"master"``):

    >>> pup = create(path="myproject",
    ...              base_url="http://some.link.com/{version}/",
    ...              version="v0.1+12.do9iwd")
    >>> print(pup.path.parts)
    ('myproject', 'master')
    >>> print(pup.base_url)
    http://some.link.com/master/

    Versioning is optional (but highly encouraged):

    >>> pup = create(path="myproject",
    ...              base_url="http://some.link.com/",
    ...              registry={"data.txt": "9081wo2eb2gc0u..."})
    >>> print(pup.path.parts)  # The path is a pathlib.Path
    ('myproject',)
    >>> print(pup.base_url)
    http://some.link.com/

    To place the storage folder at a subdirectory, pass in a list and we'll join the
    path for you using the appropriate separator for your operating system:

    >>> pup = create(path=["myproject", "cache", "data"],
    ...              base_url="http://some.link.com/{version}/",
    ...              version="v0.1")
    >>> print(pup.path.parts)
    ('myproject', 'cache', 'data', 'v0.1')

    The user can overwrite the storage path by setting an environment variable:

    >>> # The variable is not set so we'll use *path*
    >>> pup = create(path=["myproject", "not_from_env"],
    ...              base_url="http://some.link.com/{version}/",
    ...              version="v0.1",
    ...              env="MYPROJECT_DATA_DIR")
    >>> print(pup.path.parts)
    ('myproject', 'not_from_env', 'v0.1')
    >>> # Set the environment variable and try again
    >>> import os
    >>> os.environ["MYPROJECT_DATA_DIR"] = os.path.join("myproject", "from_env")
    >>> pup = create(path=["myproject", "not_from_env"],
    ...              base_url="http://some.link.com/{version}/",
    ...              version="v0.1",
    ...              env="MYPROJECT_DATA_DIR")
    >>> print(pup.path.parts)
    ('myproject', 'from_env', 'v0.1')

    """
    if isinstance(path, (list, tuple)):
        path = os.path.join(*path)
    if env is not None and env in os.environ and os.environ[env]:
        path = os.environ[env]
    if version is not None:
        version = check_version(version, fallback=version_dev)
        path = os.path.join(str(path), version)
        base_url = base_url.format(version=version)
    path = os.path.expanduser(str(path))
    # Check that the data directory is writable
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            tempfile.NamedTemporaryFile(dir=path)
    except PermissionError:
        message = (
            "Cannot write to data cache '{}'. "
            "Will not be able to download remote data files. ".format(path)
        )
        if env is not None:
            message = (
                message
                + "Use environment variable '{}' to specify another directory.".format(
                    env
                )
            )
        warn(message)
    pup = Pooch(path=Path(path), base_url=base_url, registry=registry, urls=urls)
    return pup


class Pooch:
    """
    Manager for a local data storage that can fetch from a remote source.

    Parameters
    ----------
    path : str
        The path to the local data storage folder. The path must exist in the file
        system.
    base_url : str
        Base URL for the remote data source. All requests will be made relative to this
        URL.
    registry : dict or None
        A record of the files that are managed by this good boy. Keys should be the file
        names and the values should be their SHA256 hashes. Only files in the registry
        can be fetched from the local storage. Files in subdirectories of *path* **must
        use Unix-style separators** (``'/'``) even on Windows.
    urls : dict or None
        Custom URLs for downloading individual files in the registry. A dictionary with
        the file names as keys and the custom URLs as values. Not all files in
        *registry* need an entry in *urls*. If a file has an entry in *urls*, the
        *base_url* will be ignored when downloading it in favor of ``urls[fname]``.

    """

    def __init__(self, path, base_url, registry=None, urls=None):
        self.path = path
        self.base_url = base_url
        if registry is None:
            registry = dict()
        self.registry = dict(registry)
        if urls is None:
            urls = dict()
        self.urls = dict(urls)

    @property
    def abspath(self):
        "Absolute path to the local storage"
        return Path(os.path.abspath(os.path.expanduser(str(self.path))))

    def fetch(self, fname):
        """
        Get the absolute path to a file in the local storage.

        If it's not in the local storage, it will be downloaded. If the hash of the file
        in local storage doesn't match the one in the registry, will download a new copy
        of the file. This is considered a sign that the file was updated in the remote
        storage. If the hash of the downloaded file still doesn't match the one in the
        registry, will raise an exception to warn of possible file corruption.

        Parameters
        ----------
        fname : str
            The file name (relative to the *base_url* of the remote data storage) to
            fetch from the local storage.

        Returns
        -------
        full_path : str
            The absolute path (including the file name) of the file in the local
            storage.

        """
        if fname not in self.registry:
            raise ValueError("File '{}' is not in the registry.".format(fname))
        # Create the local data directory if it doesn't already exist
        if not self.abspath.exists():
            os.makedirs(str(self.abspath))
        full_path = self.abspath / fname
        in_storage = full_path.exists()
        if not in_storage:
            action = "Downloading"
        elif in_storage and file_hash(str(full_path)) != self.registry[fname]:
            action = "Updating"
        else:
            action = "Nothing"
        if action in ("Updating", "Downloading"):
            warn(
                "{} data file '{}' from remote data store '{}' to '{}'.".format(
                    action, fname, self.base_url, str(self.path)
                )
            )
            self._download_file(fname)
        return str(full_path)

    def _get_url(self, fname):
        """
        Compute the full URL to a file.

        Provided for easy override in subclasses.

        Parameters
        ----------
        fname : str
            The file name (relative to the *base_url* of the remote data storage) to
            fetch from the local storage.

        """
        return self.urls.get(fname, "".join([self.base_url, fname]))

    def _download_file(self, fname):
        """
        Download a file from the remote data storage to the local storage.

        Used by :meth:`~pooch.Pooch.fetch` to do the actual downloading.

        Parameters
        ----------
        fname : str
            The file name (relative to the *base_url* of the remote data storage) to
            fetch from the local storage.

        Raises
        ------
        ValueError
            If the hash of the downloaded file doesn't match the hash in the registry.

        """
        destination = self.abspath / fname
        source = self._get_url(fname)
        # Stream the file to a temporary so that we can safely check its hash before
        # overwriting the original
        fout = tempfile.NamedTemporaryFile(delete=False, dir=str(self.abspath))
        try:
            with fout:
                response = requests.get(source, stream=True)
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        fout.write(chunk)
            tmphash = file_hash(fout.name)
            if tmphash != self.registry[fname]:
                raise ValueError(
                    "Hash of downloaded file '{}' doesn't match the entry in the registry:"
                    " Expected '{}' and got '{}'.".format(
                        fout.name, self.registry[fname], tmphash
                    )
                )
            # Make sure the parent directory exists in case the file is in a subdirectory.
            # Otherwise, move will cause an error.
            if not os.path.exists(str(destination.parent)):
                os.makedirs(str(destination.parent))
            shutil.move(fout.name, str(destination))
        except:
            os.remove(fout.name)
            raise

    def load_registry(self, fname):
        """
        Load entries form a file and add them to the registry.

        Use this if you are managing many files.

        Each line of the file should have file name and its SHA256 hash separate by a
        space. Only one file per line is allowed. Custom download URLs for individual
        files can be specified as a third element on the line.

        Parameters
        ----------
        fname : str
            File name and path to the registry file.

        """
        with open(fname) as fin:
            for linenum, line in enumerate(fin):
                elements = line.strip().split()
                if len(elements) > 3 or len(elements) < 2:
                    raise IOError(
                        "Expected 2 or 3 elements in line {} but got {}.".format(
                            linenum, len(elements)
                        )
                    )
                file_name = elements[0]
                file_sha256 = elements[1]
                if len(elements) == 3:
                    file_url = elements[2]
                    self.urls[file_name] = file_url
                self.registry[file_name] = file_sha256
