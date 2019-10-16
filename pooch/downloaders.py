"""
Download hooks for Pooch.fetch
"""
from __future__ import print_function
import sys

import requests

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


class HTTPDownloader:  # pylint: disable=too-few-public-methods
    """
    Download manager for fetching files over HTTP/HTTPS.

    When called, downloads the given file URL into the specified local file. Uses the
    :mod:`requests` library to manage downloads.

    Use with :meth:`pooch.Pooch.fetch` to customize the download of files (for example,
    to use authentication or print a progress bar).

    Parameters
    ----------
    progressbar : bool
        If True, will print a progress bar of the download to standard error (stderr).
        Requires `tqdm <https://github.com/tqdm/tqdm>`__ to be installed.
    chunk_size : int
        Files are streamed *chunk_size* bytes at a time instead of loading everything
        into memory at one. Usually doesn't need to be changed.
    **kwargs
        All keyword arguments given when creating an instance of this class will be
        passed to :func:`requests.get`.

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

    def __init__(self, progressbar=False, chunk_size=1024, **kwargs):
        self.kwargs = kwargs
        self.progressbar = progressbar
        self.chunk_size = chunk_size
        if self.progressbar and tqdm is None:
            raise ValueError("Missing package 'tqdm' required for progress bars.")

    def __call__(self, url, output_file, pooch):
        """
        Download the given URL over HTTP to the given output file.

        Uses :func:`requests.get`.

        Parameters
        ----------
        url : str
            The URL to the file you want to download.
        output_file : str or file-like object
            Path (and file name) to which the file will be downloaded.
        pooch : :class:`~pooch.Pooch`
            The instance of :class:`~pooch.Pooch` that is calling this method.

        """
        kwargs = self.kwargs.copy()
        kwargs.setdefault("stream", True)
        ispath = not hasattr(output_file, "write")
        if ispath:
            output_file = open(output_file, "w+b")
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            content = response.iter_content(chunk_size=self.chunk_size)
            if self.progressbar:
                total = int(response.headers.get("content-length", 0))
                # Need to use ascii characters on Windows because there isn't always
                # full unicode support (see https://github.com/tqdm/tqdm/issues/454)
                use_ascii = bool(sys.platform == "win32")
                progress = tqdm(
                    total=total,
                    ncols=79,
                    ascii=use_ascii,
                    unit="B",
                    unit_scale=True,
                    leave=True,
                )
            for chunk in content:
                if chunk:
                    output_file.write(chunk)
                    output_file.flush()
                    if self.progressbar:
                        # Use the chunk size here because chunk may be much larger if
                        # the data are decompressed by requests after reading (happens
                        # with text files).
                        progress.update(self.chunk_size)
            # Make sure the progress bar gets filled even if the actual number is
            # chunks is smaller than expected. This happens when streaming text files
            # that are compressed by the server when sending (gzip). Binary files don't
            # experience this.
            if self.progressbar:
                progress.reset()
                progress.update(total)
                progress.close()
        finally:
            if ispath:
                output_file.close()
