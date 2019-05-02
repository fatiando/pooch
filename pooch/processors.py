# pylint: disable=line-too-long
"""
Post-processing hooks for Pooch.fetch
"""
import os

from zipfile import ZipFile
from warnings import warn


class Unzip:  # pylint: disable=too-few-public-methods
    """
    Processor that unpacks a zip archive and returns a list of all files.

    Use with :meth:`pooch.Pooch.fetch` to unzip a downloaded data file into a folder in
    the local data store. :meth:`~pooch.Pooch.fetch` will return a list with the names
    of the unzipped files instead of the zip archive.
    """

    def __call__(self, fname, action, pooch):
        """
        Extract all files from the given zip archive.

        The output folder is ``{fname}.unzip``.

        Parameters
        ----------
        fname : str
            Full path of the zipped file in local storage.
        action : str
            Indicates what action was taken by :meth:`pooch.Pooch.fetch`. One of:

            * ``"download"``: The file didn't exist locally and was downloaded
            * ``"update"``: The local file was outdated and was re-download
            * ``"fetch"``: The file exists and is updated so it wasn't downloaded

        pooch : :class:`pooch.Pooch`
            The instance of :class:`pooch.Pooch` that is calling this.

        Returns
        -------
        fnames : list of str
            A list of the full path to all files in the unzipped archive.

        """
        unzipped = fname + ".unzip"
        if action in ("update", "download") or not os.path.exists(unzipped):
            warn("Unzipping contents of '{}' to '{}'".format(fname, unzipped))
            # Make sure that the folder with the unzipped files exists
            if not os.path.exists(unzipped):
                os.makedirs(unzipped)
            with ZipFile(fname, "r") as zip_file:
                # Unpack all files from the archive into our new folder
                zip_file.extractall(path=unzipped)
        # Get a list of all file names (including subdirectories) in our folder of
        # unzipped files.
        fnames = [
            os.path.join(path, fname)
            for path, _, files in os.walk(unzipped)
            for fname in files
        ]
        return fnames


class UnzipSingle:  # pylint: disable=too-few-public-methods
    """
    Processor that unpacks a single file from the downloaded zip archive.

    Use with :meth:`pooch.Pooch.fetch` to unpack a single file from a downloaded zip
    archive. :meth:`~pooch.Pooch.fetch` will return the path to the unzipped file
    instead of the zip archive.

    Parameters
    ----------
    member : str
        Name of the file to extract from the zip archive.

    """

    def __init__(self, member=None):
        self.member = member

    def __call__(self, fname, action, pooch):
        """
        Extract a single *member* from the given zip archive.

        The output file name is ``{fname}-{member}.unzip``.

        Parameters
        ----------
        fname : str
            Full path of the zipped file in local storage.
        action : str
            Indicates what action was taken by :meth:`pooch.Pooch.fetch`. One of:

            * ``"download"``: The file didn't exist locally and was downloaded
            * ``"update"``: The local file was outdated and was re-download
            * ``"fetch"``: The file exists and is updated so it wasn't downloaded

        pooch : :class:`pooch.Pooch`
            The instance of :class:`pooch.Pooch` that is calling this.

        Returns
        -------
        fname : str
            The full path to the unzipped file.

        """
        unzipped = "{}-{}.unzip".format(fname, self.member)
        if action in ("update", "download") or not os.path.exists(unzipped):
            warn(
                "Unzipping '{}' from '{}' to '{}'".format(self.member, fname, unzipped)
            )
            with ZipFile(fname, "r") as zip_file:
                # Extract the data file from within the archive
                with zip_file.open(self.member) as data_file:
                    # Save it to our desired file name
                    with open(unzipped, "wb") as output:
                        output.write(data_file.read())
        return unzipped
