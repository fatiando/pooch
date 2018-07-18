"""
Functions to download, verify, and update a sample dataset.
"""
import os

from .utils import file_hash


class Garage():
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
        self.path = path
        self.base_url = base_url
        self.registry = registry

    def fetch(self, fname):
        """
        Get the full path to a file in the garage.

        If it's not in the local storage, it will be downloaded. If the hash of file in
        local storage doesn't match the one in the registry, will download a new copy of
        the file. If the hash of the downloaded file doesn't match the one in the
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
        full_path = os.path.abspath(os.path.join(self.path, fname))
        if os.path.exists(full_path):
            if file_hash(full_path) != self.registry[full_path]:
                self._download_file(fname)

        return full_path

    def _download_file(self, fname):
        """
        """
        pass

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
                    raise ValueError("Expected 2 elements in line {} but got {}."
                                     .format(linenum, len(elements)))
                file_name, file_hash = elements
                self.registry[file_name] = file_hash
