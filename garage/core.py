"""
Functions to download, verify, and update a sample dataset.
"""
import os
import shutil
from tempfile import NamedTemporaryFile
from warnings import warn

import requests

from .utils import file_hash


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

    """

    def __init__(self, path, base_url, registry):
        self._path = path
        self.base_url = base_url
        self.registry = registry

    @property
    def path(self):
        "Absolute path to the local garage"
        return os.path.abspath(self._path)

    def fetch(self, fname):
        """
        Get the full path to a file in the garage.

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
            The full path (including the file name) of the file in the local storage.

        """
        if fname not in self.registry:
            raise ValueError("File '{}' is not in the registry.".format(fname))
        full_path = os.path.join(self.path, fname)
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
        destination = os.path.join(self.path, fname)
        source = "".join([self.base_url, fname])
        if update:
            action = "Updating"
        else:
            action = "Downloading"
        warn(
            "{} data file '{}' from remote data store '{}' to '{}'.".format(
                action, fname, self.base_url, self.path
            )
        )
        response = requests.get(source, stream=True)
        response.raise_for_status()
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
