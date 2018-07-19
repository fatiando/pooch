"""
Functions to download, verify, and update a sample dataset.
"""
import os
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile
from warnings import warn

import requests

from .utils import file_hash


def create(path, base_url, version, version_dev, env_variable=None, registry=None):
    """
    Create a new (versioned) Garage with sensible defaults.

    The Garage will be versioned, meaning that the local storage folder and the base URL
    depend on the projection version. This is necessary if your users have multiple
    versions of your library installed (using virtual environments) and you updated the
    data files between versions. If the Garage was not versioned, every time a user
    switches environments would trigger a re-download of the data.

    The version string will be appended to the local storage path (for example,
    ``~/.mygarage/cache/v0.1``) and inserted into the base URL (for example,
    ``https://github.com/fatiando/garage/raw/v0.1/data``). If the version string
    contains ``+XX.XXXXX``, it will be interpreted as a development version.

    Parameters
    ----------
    path : str or PathLike
        The path to the local data storage folder. If this is a list or tuple, we'll
        call :func:`os.path.join` on it. The *version* will be appended to the end of
        this path. Use :func:`garage.os_cache` for a sensible default.
    base_url : str
        Base URL for the remote data source. All requests will be made relative to this
        URL. The string should have a ``{version}`` formatting mark in it. We will call
        ``.format(version=version)`` on this string.
    version : str
        The version string for your project. Should be PEP440 compatible.
    version_dev : str
        The name used for the development version of a project. If your data is hosted
        on Github (and *base_url* is a Github raw link), then ``"master"`` is a good
        choice.
    env_variable : str
        An environment variable that can be used to overwrite *path*. This allows users
        to control where they want the data to be stored. We'll append *version* to the
        end of this value as well.
    registry : dict
        A record of the files that exist in this garage. Keys should be the file names
        and the values should be their SHA256 hashes. Only files in the registry can be
        fetched from the garage.

    Returns
    -------
    garage : :class:`~garage.Garage`
        The Garage initialized with the given arguments.

    Examples
    --------

    >>> garage = create(path="mygarage", base_url="http://some.link.com/{version}",
    ...                 version="v0.1", version_dev="master")
    >>> print(garage.path.parts)
    ('mygarage', 'v0.1')
    >>> print(garage.base_url)
    http://some.link.com/v0.1
    >>> print(garage.registry)
    {}
    >>> garage = create(path="mygarage", base_url="http://some.link.com/{version}",
    ...                 version="v0.1+12.do9iwd", version_dev="master")
    >>> print(garage.path.parts)
    ('mygarage', 'master')
    >>> print(garage.base_url)
    http://some.link.com/master

    """
    path = Path(path)
    if registry is None:
        registry = dict()
    garage = Garage(path=Path(path, version),
                    base_url=base_url.format(version=version),
                    registry=registry)
    return garage


class Garage:
    """
    Manager for a local data storage that can fetch from a remote source.

    Parameters
    ----------
    path : str
        The path to the local data storage folder.
    base_url : str
        Base URL for the remote data source. All requests will be made relative to this
        URL.
    registry : dict
        A record of the files that exist in this garage. Keys should be the file names
        and the values should be their SHA256 hashes. Only files in the registry can be
        fetched from the garage.

    Examples
    --------

    >>> import warnings
    >>> warnings.simplefilter("ignore")  # disable warnings to stop printing status
    >>> import os
    >>> from tempfile import TemporaryDirectory
    >>> from garage.tests.utils import garage_test_url, garage_test_registry
    >>> # Setup a garage in a temporary directory for this example
    >>> store = TemporaryDirectory()
    >>> os.listdir(store.name)
    []
    >>> # Use our test base url and registry
    >>> garage = Garage(path=store.name, base_url=garage_test_url(),
    ...                 registry=garage_test_registry())
    >>> # Fetch a data file from the garage. Since it's not in our local storage, it
    >>> # will be downloaded
    >>> fname = garage.fetch('tiny-data.txt')
    >>> os.listdir(store.name)
    ['tiny-data.txt']
    >>> with open(fname) as f:
    ...     print(f.read().strip())
    # A tiny data file for test purposes only
    1  2  3  4  5  6
    >>> # If the data file is corrupted or outdated, Garage will download a new version
    >>> with open(fname, "w") as f:
    ...     __ = f.write("This is no longer the same file content.")
    >>> fname = garage.fetch('tiny-data.txt')
    >>> with open(fname) as f:
    ...     print(f.read().strip())
    # A tiny data file for test purposes only
    1  2  3  4  5  6
    >>> store.cleanup()

    """

    def __init__(self, path, base_url, registry):
        self.path = path
        self.base_url = base_url
        self.registry = dict(registry)

    @property
    def abspath(self):
        "Absolute path to the local garage"
        return os.path.abspath(os.path.expanduser(self.path))

    def fetch(self, fname):
        """
        Get the absolute path to a file in the garage.

        If it's not in the local storage, it will be downloaded. If the hash of file in
        local storage doesn't match the one in the registry, will download a new copy of
        the file. This is considered a sign that the file was updated in the remote
        storage. If the hash of the downloaded file doesn't match the one in the
        registry, will raise an exception to warn of possible file corruption.

        Parameters
        ----------
        fname : str
            The file name (relative to the *base_url* of the remote data storage) to
            fetch from the garage.

        Returns
        -------
        full_path : str
            The absolute path (including the file name) of the file in the local garage.

        """
        if fname not in self.registry:
            raise ValueError("File '{}' is not in the registry.".format(fname))
        full_path = os.path.join(self.abspath, fname)
        in_garage = os.path.exists(full_path)
        update = in_garage and file_hash(full_path) != self.registry[fname]
        download = not in_garage
        if update or download:
            self._download_file(fname, update)
        return full_path

    def _download_file(self, fname, update):
        """
        Download a file from the remote data storage to the local garage.

        Parameters
        ----------
        fname : str
            The file name (relative to the *base_url* of the remote data storage) to
            fetch from the garage.
        update : bool
            True if the file already exists in the garage but needs an update.

        Raises
        ------
        ValueError
            If the hash of the downloaded file doesn't match the hash in the registry.

        """
        destination = os.path.join(self.abspath, fname)
        source = "".join([self.base_url, fname])
        if update:
            action = "Updating"
        else:
            action = "Downloading"
        warn(
            "{} data file '{}' from remote data store '{}' to '{}'.".format(
                action, fname, self.base_url, self.abspath
            )
        )
        response = requests.get(source, stream=True)
        response.raise_for_status()
        # Stream the file to a temporary so that we can safely check its hash before
        # overwriting the original
        with NamedTemporaryFile(delete=False) as fout:
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
        shutil.move(fout.name, destination)

    def load_registry(self, fname):
        """
        Load entries form a file and add them to the registry.

        Use this if you are managing a garage with many files.

        Each line of the file should have file name and its SHA256 hash separate by a
        space. Only one file per line is allowed.

        Parameters
        ----------
        fname : str
            File name and path to the registry file.

        """
        with open(fname) as fin:
            for linenum, line in enumerate(fin):
                elements = line.strip().split()
                if len(elements) != 2:
                    raise ValueError(
                        "Expected 2 elements in line {} but got {}.".format(
                            linenum, len(elements)
                        )
                    )
                file_name, file_sha256 = elements
                self.registry[file_name] = file_sha256
