# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
The classes that actually handle the downloads.
"""
import sys
import ftplib

import requests

from .utils import parse_url

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

try:
    import paramiko
except ImportError:
    paramiko = None


def choose_downloader(url):
    """
    Choose the appropriate downloader for the given URL based on the protocol.

    Parameters
    ----------
    url : str
        A URL (including protocol).

    Returns
    -------
    downloader
        A downloader class (either :class:`pooch.HTTPDownloader`,
        :class:`pooch.FTPDownloader`, or :class: `pooch.SFTPDownloader`).

    Examples
    --------

    >>> downloader = choose_downloader("http://something.com")
    >>> print(downloader.__class__.__name__)
    HTTPDownloader
    >>> downloader = choose_downloader("https://something.com")
    >>> print(downloader.__class__.__name__)
    HTTPDownloader
    >>> downloader = choose_downloader("ftp://something.com")
    >>> print(downloader.__class__.__name__)
    FTPDownloader

    """
    known_downloaders = {
        "ftp": FTPDownloader,
        "https": HTTPDownloader,
        "http": HTTPDownloader,
        "sftp": SFTPDownloader,
    }

    parsed_url = parse_url(url)
    if parsed_url["protocol"] not in known_downloaders:
        raise ValueError(
            f"Unrecognized URL protocol '{parsed_url['protocol']}' in '{url}'. "
            f"Must be one of {known_downloaders.keys()}."
        )
    downloader = known_downloaders[parsed_url["protocol"]]()
    return downloader


class HTTPDownloader:  # pylint: disable=too-few-public-methods
    """
    Download manager for fetching files over HTTP/HTTPS.

    When called, downloads the given file URL into the specified local file.
    Uses the :mod:`requests` library to manage downloads.

    Use with :meth:`pooch.Pooch.fetch` or :func:`pooch.retrieve` to customize
    the download of files (for example, to use authentication or print a
    progress bar).

    Parameters
    ----------
    progressbar : bool or an arbitrary progress bar object
        If True, will print a progress bar of the download to standard error
        (stderr). Requires `tqdm <https://github.com/tqdm/tqdm>`__ to be
        installed. Alternatively, an arbitrary progress bar object can be
        passed. See :ref:`custom-progressbar` for details.
    chunk_size : int
        Files are streamed *chunk_size* bytes at a time instead of loading
        everything into memory at one. Usually doesn't need to be changed.
    **kwargs
        All keyword arguments given when creating an instance of this class
        will be passed to :func:`requests.get`.

    Examples
    --------

    Download one of the data files from the Pooch repository:

    >>> import os
    >>> from pooch import __version__, check_version
    >>> url = "https://github.com/fatiando/pooch/raw/{}/data/tiny-data.txt"
    >>> url = url.format(check_version(__version__))
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
    :func:`requests.get`. All arguments provided when creating an instance of
    the class are forwarded to :func:`requests.get`. We'll use
    ``auth=(username, password)`` to use basic HTTPS authentication. The
    https://httpbin.org website allows us to make a fake a login request using
    whatever username and password we provide to it:

    >>> user = "doggo"
    >>> password = "goodboy"
    >>> # httpbin will ask for the user and password we provide in the URL
    >>> url = f"https://httpbin.org/basic-auth/{user}/{password}"
    >>> # Trying without the login credentials causes an error
    >>> downloader = HTTPDownloader()
    >>> try:
    ...     downloader(url=url, output_file="tiny-data.txt", pooch=None)
    ... except Exception:
    ...     print("There was an error!")
    There was an error!
    >>> # Pass in the credentials to HTTPDownloader
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
        if self.progressbar is True and tqdm is None:
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
            total = int(response.headers.get("content-length", 0))
            if self.progressbar is True:
                # Need to use ascii characters on Windows because there isn't
                # always full unicode support
                # (see https://github.com/tqdm/tqdm/issues/454)
                use_ascii = bool(sys.platform == "win32")
                progress = tqdm(
                    total=total,
                    ncols=79,
                    ascii=use_ascii,
                    unit="B",
                    unit_scale=True,
                    leave=True,
                )
            elif self.progressbar:
                progress = self.progressbar
                progress.total = total
            for chunk in content:
                if chunk:
                    output_file.write(chunk)
                    output_file.flush()
                    if self.progressbar:
                        # Use the chunk size here because chunk may be much
                        # larger if the data are decompressed by requests after
                        # reading (happens with text files).
                        progress.update(self.chunk_size)
            # Make sure the progress bar gets filled even if the actual number
            # is chunks is smaller than expected. This happens when streaming
            # text files that are compressed by the server when sending (gzip).
            # Binary files don't experience this.
            if self.progressbar:
                progress.reset()
                progress.update(total)
                progress.close()
        finally:
            if ispath:
                output_file.close()


class FTPDownloader:  # pylint: disable=too-few-public-methods
    """
    Download manager for fetching files over FTP.

    When called, downloads the given file URL into the specified local file.
    Uses the :mod:`ftplib` module to manage downloads.

    Use with :meth:`pooch.Pooch.fetch` or :func:`pooch.retrieve` to customize
    the download of files (for example, to use authentication or print a
    progress bar).

    Parameters
    ----------
    port : int
        Port used for the FTP connection.
    username : str
        User name used to login to the server. Only needed if the server
        requires authentication (i.e., no anonymous FTP).
    password : str
        Password used to login to the server. Only needed if the server
        requires authentication (i.e., no anonymous FTP). Use the empty string
        to indicate no password is required.
    account : str
        Some servers also require an "account" name for authentication.
    timeout : int
        Timeout in seconds for ftp socket operations, use None to mean no
        timeout.
    progressbar : bool
        If True, will print a progress bar of the download to standard error
        (stderr). Requires `tqdm <https://github.com/tqdm/tqdm>`__ to be
        installed. **Custom progress bars are not yet supported.**
    chunk_size : int
        Files are streamed *chunk_size* bytes at a time instead of loading
        everything into memory at one. Usually doesn't need to be changed.

    """

    def __init__(
        self,
        port=21,
        username="anonymous",
        password="",
        account="",
        timeout=None,
        progressbar=False,
        chunk_size=1024,
    ):

        self.port = port
        self.username = username
        self.password = password
        self.account = account
        self.timeout = timeout
        self.progressbar = progressbar
        self.chunk_size = chunk_size
        if self.progressbar is True and tqdm is None:
            raise ValueError("Missing package 'tqdm' required for progress bars.")

    def __call__(self, url, output_file, pooch):
        """
        Download the given URL over FTP to the given output file.

        Parameters
        ----------
        url : str
            The URL to the file you want to download.
        output_file : str or file-like object
            Path (and file name) to which the file will be downloaded.
        pooch : :class:`~pooch.Pooch`
            The instance of :class:`~pooch.Pooch` that is calling this method.
        """

        parsed_url = parse_url(url)
        ftp = ftplib.FTP(timeout=self.timeout)
        ftp.connect(host=parsed_url["netloc"], port=self.port)
        ispath = not hasattr(output_file, "write")
        if ispath:
            output_file = open(output_file, "w+b")
        try:
            ftp.login(user=self.username, passwd=self.password, acct=self.account)
            command = f"RETR {parsed_url['path']}"
            if self.progressbar:
                # Make sure the file is set to binary mode, otherwise we can't
                # get the file size. See: https://stackoverflow.com/a/22093848
                ftp.voidcmd("TYPE I")
                size = int(ftp.size(parsed_url["path"]))
                use_ascii = bool(sys.platform == "win32")
                progress = tqdm(
                    total=size,
                    ncols=79,
                    ascii=use_ascii,
                    unit="B",
                    unit_scale=True,
                    leave=True,
                )
                with progress:

                    def callback(data):
                        "Update the progress bar and write to output"
                        progress.update(len(data))
                        output_file.write(data)

                    ftp.retrbinary(command, callback, blocksize=self.chunk_size)
            else:
                ftp.retrbinary(command, output_file.write, blocksize=self.chunk_size)
        finally:
            ftp.quit()
            if ispath:
                output_file.close()


class SFTPDownloader:  # pylint: disable=too-few-public-methods
    """
    Download manager for fetching files over SFTP.

    When called, downloads the given file URL into the specified local file.
    Requires `paramiko <https://github.com/paramiko/paramiko>`__ to be
    installed.

    Use with :meth:`pooch.Pooch.fetch` or :func:`pooch.retrieve` to customize
    the download of files (for example, to use authentication or print a
    progress bar).

    Parameters
    ----------
    port : int
        Port used for the SFTP connection.
    username : str
        User name used to login to the server. Only needed if the server
        requires authentication (i.e., no anonymous SFTP).
    password : str
        Password used to login to the server. Only needed if the server
        requires authentication (i.e., no anonymous SFTP). Use the empty
        string to indicate no password is required.
    timeout : int
        Timeout in seconds for sftp socket operations, use None to mean no
        timeout.
    progressbar : bool or an arbitrary progress bar object
        If True, will print a progress bar of the download to standard
        error (stderr). Requires `tqdm <https://github.com/tqdm/tqdm>`__ to
        be installed.

    """

    def __init__(
        self,
        port=22,
        username="anonymous",
        password="",
        account="",
        timeout=None,
        progressbar=False,
    ):
        self.port = port
        self.username = username
        self.password = password
        self.account = account
        self.timeout = timeout
        self.progressbar = progressbar
        # Collect errors and raise only once so that both missing packages are
        # captured. Otherwise, the user is only warned of one of them at a
        # time (and we can't test properly when they are both missing).
        errors = []
        if self.progressbar and tqdm is None:
            errors.append("Missing package 'tqdm' required for progress bars.")
        if paramiko is None:
            errors.append("Missing package 'paramiko' required for SFTP downloads.")
        if errors:
            raise ValueError(" ".join(errors))

    def __call__(self, url, output_file, pooch):
        """
        Download the given URL over SFTP to the given output file.

        The output file must be given as a string (file name/path) and not an
        open file object! Otherwise, paramiko cannot save to that file.

        Parameters
        ----------
        url : str
            The URL to the file you want to download.
        output_file : str
            Path (and file name) to which the file will be downloaded. **Cannot
            be a file object**.
        pooch : :class:`~pooch.Pooch`
            The instance of :class:`~pooch.Pooch` that is calling this method.
        """
        parsed_url = parse_url(url)
        connection = paramiko.Transport(sock=(parsed_url["netloc"], self.port))
        sftp = None
        try:
            connection.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(connection)
            sftp.get_channel().settimeout = self.timeout
            if self.progressbar:
                size = int(sftp.stat(parsed_url["path"]).st_size)
                use_ascii = bool(sys.platform == "win32")
                progress = tqdm(
                    total=size,
                    ncols=79,
                    ascii=use_ascii,
                    unit="B",
                    unit_scale=True,
                    leave=True,
                )
            if self.progressbar:
                with progress:

                    def callback(current, total):
                        "Update the progress bar and write to output"
                        progress.total = int(total)
                        progress.update(int(current - progress.n))

                    sftp.get(parsed_url["path"], output_file, callback=callback)
            else:
                sftp.get(parsed_url["path"], output_file)
        finally:
            connection.close()
            if sftp is not None:
                sftp.close()
