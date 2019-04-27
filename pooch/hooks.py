# pylint: disable=line-too-long
"""
Download and post-processing hooks for Pooch.fetch
"""
from __future__ import print_function

import os
from zipfile import ZipFile

import requests


class HTTPDownloader:  # pylint: disable=too-few-public-methods
    """
    Download manager for fetching files over HTTP/HTTPS.

    When called, downloads the given file URL into the specified local file. Uses the
    :mod:`requests` library to manage downloads.

    All keyword arguments given when creating an instance of this class will be passed
    to :func:`requests.get`.

    Use with :meth:`pooch.Pooch.fetch` to customize the download of files (for example,
    to use authentication).

    Parameters
    ----------
    url : str
        The URL to the file you want to download.
    output_file : str or file-like object
        Path (and file name) to which the file will be downloaded.
    pooch : :class:`~pooch.Pooch`
        The instance of :class:`~pooch.Pooch` that is calling this method.

    Examples
    --------

    Download one of the data files from the Pooch repository:

    >>> import os
    >>> from pooch import version, check_version
    >>> url = "https://github.com/fatiando/pooch/raw/{}/data/tiny-data.txt".format(
    ...     check_version(version.full_version))
    >>> downloader = HTTPDownloader()
    >>> # Not using with Pooch.fetch so no need to pass an instance of Pooch
    >>> downloader(url=url, output_file="tiny-data.txt", pooch=None)
    >>> os.path.exists("tiny-data.txt")
    True
    >>> with open("tiny-data.txt") as f:
    ...     print(f.read().strip())
    # A tiny data file for test purposes only
    1  2  3  4  5  6
    >>> os.remove("tiny-data.txt")

    Authentication can be handled by passing a user name and password to
    :func:`requests.get`. All arguments provided when creating an instance of the class
    are forwarded to :func:`requests.get`. We'll use ``auth=(username, password)`` to
    use basic HTTPS authentication. The https://httpbin.org website allows us to make a
    fake a login request using whatever username and password we provide to it:

    >>> user = "doggo"
    >>> password = "goodboy"
    >>> # httpbin will ask for the user and password we provide in the URL
    >>> url = "https://httpbin.org/basic-auth/{}/{}".format(user, password)
    >>> # Trying without the login credentials causes an error
    >>> downloader = HTTPDownloader()
    >>> try:
    ...     downloader(url=url, output_file="tiny-data.txt", pooch=None)
    ... except Exception:
    ...     print("There was an error!")
    There was an error!
    >>> # Pass in the credentials to HTTPDownloader and it will forward to requests.get
    >>> downloader = HTTPDownloader(auth=(user, password))
    >>> downloader(url=url, output_file="tiny-data.txt", pooch=None)
    >>> with open("tiny-data.txt") as f:
    ...     for line in f:
    ...         print(line.rstrip())
    {
      "authenticated": true,
      "user": "doggo"
    }
    >>> os.remove("tiny-data.txt")

    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, url, output_file, pooch):
        """
        Download the URL to the given output file.
        """
        kwargs = self.kwargs.copy()
        kwargs.setdefault("stream", True)
        ispath = not hasattr(output_file, "write")
        if ispath:
            output_file = open(output_file, "w+b")
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    output_file.write(chunk)
        finally:
            if ispath:
                output_file.close()


class UnzipProcessor:  # pylint: disable=too-few-public-methods
    """
    Processing hook to unpack a zip archive and return a list of all files.

    Use with :meth:`pooch.Pooch.fetch` to unzip a downloaded data file and return the
    names of the unzipped files instead of the zip archive.

    Parameters
    ----------
    folder_name : str or None
        Name (path) of the folder where the files will be unpacked. If None, will use
        the original file name plus ``.unzipped``.

    Examples
    --------


    """

    def __init__(self, folder_name=None):
        self.folder_name = folder_name

    def __call__(self, fname, action, pooch):
        """
        Extract all files from the given zip archive.

        The output folder is determined by the ``folder_name`` attribute (defaults to
        ``fname + ".unzipped"``.

        Parameters
        ----------
        fname : str
           Full path of the zipped file in local storage.
        action : str
           One of "download" (file doesn't exist and will download),
           "update" (file is outdated and will download), and
           "fetch" (file exists and is updated so no download).
       pooch : :class:`pooch.Pooch`
           The instance of :class:`pooch.Pooch` that is calling this.

        Returns
        -------
        fnames : list of str
           A list of the full path to all files in the unzipped archive.

        """
        if self.folder_name is not None:
            unzipped = self.folder_name
        else:
            unzipped = fname + ".unzipped"
        if action in ("update", "download") or not os.path.exists(unzipped):
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
