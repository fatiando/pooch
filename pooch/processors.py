# pylint: disable=line-too-long
"""
Post-processing hooks for Pooch.fetch
"""
import os
import sys
import gzip
import shutil
from zipfile import ZipFile
from tarfile import TarFile
from warnings import warn

# Try getting the 2.7 backports of lzma and bz2. Can be deleted when dropping 2.7
if sys.version_info[0] < 3:
    try:
        import bz2file as bz2
    except ImportError:
        bz2 = None
else:
    import bz2
try:
    import lzma
except ImportError:
    try:
        from backports import lzma
    except ImportError:
        # Make this an optional dependency
        lzma = None


class ExtractorProcessor:  # pylint: disable=too-few-public-methods
    """
    Base class for extractions from compressed archives.

    Subclasses can be used with :meth:`pooch.Pooch.fetch` to unzip a downloaded
    data file into a folder in the local data store. :meth:`~pooch.Pooch.fetch`
    will return a list with the names of the extracted files instead of the
    archive.

    Parameters
    ----------
    members : list or None
        If None, will unpack all files in the archive. Otherwise, *members*
        must be a list of file names to unpack from the archive. Only these
        files will be unpacked.

    """

    suffix = None  # String appended to unpacked archive. To be implemented in subclass

    def __init__(self, members=None):
        self.members = members

    def __call__(self, fname, action, pooch):
        """
        Extract all files from the given archive.

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
            A list of the full path to all files in the extracted archive.

        """
        if self.suffix is None:
            raise NotImplementedError(
                "Derived classes must define the 'suffix' attribute."
            )
        extract_dir = fname + self.suffix
        if action in ("update", "download") or not os.path.exists(extract_dir):
            # Make sure that the folder with the extracted files exists
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)
            self._extract_file(fname, extract_dir)
        # Get a list of all file names (including subdirectories) in our folder of
        # unzipped files.
        fnames = [
            os.path.join(path, fname)
            for path, _, files in os.walk(extract_dir)
            for fname in files
        ]
        return fnames

    def _extract_file(self, fname, extract_dir):
        """
        This method receives an argument for the archive to extract and the
        destination path. MUST BE IMPLEMENTED BY CHILD CLASSES.
        """
        raise NotImplementedError


class Unzip(ExtractorProcessor):  # pylint: disable=too-few-public-methods
    """
    Processor that unpacks a zip archive and returns a list of all files.

    Use with :meth:`pooch.Pooch.fetch` to unzip a downloaded data file into a folder in
    the local data store. :meth:`~pooch.Pooch.fetch` will return a list with the names
    of the unzipped files instead of the zip archive.

    The output folder is ``{fname}.unzip``.

    Parameters
    ----------
    members : list or None
        If None, will unpack all files in the zip archive. Otherwise, *members* must be
        a list of file names to unpack from the archive. Only these files will be
        unpacked.

    """

    suffix = ".unzip"

    def _extract_file(self, fname, extract_dir):
        """
        This method receives an argument for the archive to extract and the
        destination path.
        """
        with ZipFile(fname, "r") as zip_file:
            if self.members is None:
                warn("Unzipping contents of '{}' to '{}'".format(fname, extract_dir))
                # Unpack all files from the archive into our new folder
                zip_file.extractall(path=extract_dir)
            else:
                for member in self.members:
                    warn(
                        "Extracting '{}' from '{}' to '{}'".format(
                            member, fname, extract_dir
                        )
                    )
                    # Extract the data file from within the archive
                    with zip_file.open(member) as data_file:
                        # Save it to our desired file name
                        with open(os.path.join(extract_dir, member), "wb") as output:
                            output.write(data_file.read())


class Untar(ExtractorProcessor):  # pylint: disable=too-few-public-methods
    """
    Processor that unpacks a tar archive and returns a list of all files.

    Use with :meth:`pooch.Pooch.fetch` to untar a downloaded data file into a folder in
    the local data store. :meth:`~pooch.Pooch.fetch` will return a list with the names
    of the extracted files instead of the archive.

    The output folder is ``{fname}.untar``.


    Parameters
    ----------
    members : list or None
        If None, will unpack all files in the archive. Otherwise, *members* must be
        a list of file names to unpack from the archive. Only these files will be
        unpacked.
    """

    suffix = ".untar"

    def _extract_file(self, fname, extract_dir):
        """
        This method receives an argument for the archive to extract and the
        destination path.
        """
        with TarFile.open(fname, "r") as tar_file:
            if self.members is None:
                warn("Untarring contents of '{}' to '{}'".format(fname, extract_dir))
                # Unpack all files from the archive into our new folder
                tar_file.extractall(path=extract_dir)
            else:
                for member in self.members:
                    warn(
                        "Extracting '{}' from '{}' to '{}'".format(
                            member, fname, extract_dir
                        )
                    )
                    # Extract the data file from within the archive
                    # Python 2.7: extractfile doesn't return a context manager
                    data_file = tar_file.extractfile(member)
                    try:
                        # Save it to our desired file name
                        with open(os.path.join(extract_dir, member), "wb") as output:
                            output.write(data_file.read())
                    finally:
                        data_file.close()


class Decompress:  # pylint: disable=too-few-public-methods
    """
    Processor that decompress a file and returns the decompressed version.

    Use with :meth:`pooch.Pooch.fetch` to decompress a downloaded data file so that it
    can be easily opened. Useful for data files that take a long time to decompress
    (exchanging disk space for speed).

    The output file is ``{fname}.decomp``.

    Supported decompression methods are LZMA (``.xz``), bzip2 (``.bz2``), and gzip
    (``.gz``).

    File names with the standard extensions (see above) can use ``method="auto"`` to
    automatically determine the compression method. This can be overwritten by setting
    the *method* argument.

    .. warning::

        With **Python 2.7**, methods "lzma"/"xz" and "bzip2" require extra dependencies
        to be installed: ``backports.lzma`` for "lzma" and ``bz2file`` for "bzip2".

    Parameters
    ----------
    method : str
        Name of the compression method. Can be "auto", "lzma", "xz", "bzip2", or "gzip".

    """

    modules = {"lzma": lzma, "xz": lzma, "gzip": gzip, "bzip2": bz2}

    def __init__(self, method="auto"):
        self.method = method

    def __call__(self, fname, action, pooch):
        """
        Decompress the given file.

        The output file will be ``fname`` with ``.decomp`` appended to it.

        Parameters
        ----------
        fname : str
            Full path of the compressed file in local storage.
        action : str
            Indicates what action was taken by :meth:`pooch.Pooch.fetch`. One of:

            - ``"download"``: The file didn't exist locally and was downloaded
            - ``"update"``: The local file was outdated and was re-download
            - ``"fetch"``: The file exists and is updated so it wasn't downloaded

        pooch : :class:`pooch.Pooch`
            The instance of :class:`pooch.Pooch` that is calling this.

        Returns
        -------
        fname : str
            The full path to the decompressed file.
        """
        decompressed = fname + ".decomp"
        if action in ("update", "download") or not os.path.exists(decompressed):
            warn(
                "Decompressing '{}' to '{}' using method '{}'.".format(
                    fname, decompressed, self.method
                )
            )
            module = self._compression_module(fname)
            with open(decompressed, "w+b") as output:
                with module.open(fname) as compressed:
                    shutil.copyfileobj(compressed, output)
        return decompressed

    def _compression_module(self, fname):
        """
        Get the Python compression module compatible with fname and the chosen method.

        If the *method* attribute is "auto", will select a method based on the
        extension. If no recognized extension is in the file name, will raise a
        ValueError.
        """
        method = self.method
        if method == "auto":
            ext = os.path.splitext(fname)[-1]
            valid_methods = {".xz": "lzma", ".gz": "gzip", ".bz2": "bzip2"}
            if ext not in valid_methods:
                raise ValueError(
                    "Unrecognized extension '{}'. Must be one of '{}'.".format(
                        ext, list(valid_methods.keys())
                    )
                )
            method = valid_methods[ext]
        if method not in self.modules:
            raise ValueError(
                "Invalid compression method '{}'. Must be one of '{}'.".format(
                    method, list(self.modules.keys())
                )
            )
        # Check for Python 2.7 extra dependencies
        if method in ["lzma", "xz"] and self.modules["lzma"] is None:
            raise ValueError(
                "LZMA/xz support requires the 'backports.lzma' package in Python 2.7"
            )
        if method == "bzip2" and self.modules["bzip2"] is None:
            raise ValueError(
                "bzip2 support requires the 'bz2file' package in Python 2.7"
            )
        return self.modules[method]
