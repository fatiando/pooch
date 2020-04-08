"""
The main Pooch class and a factory function for it.
"""
import contextlib
import os
from pathlib import Path
import shutil
import ftplib

import requests
from .utils import (
    check_version,
    parse_url,
    get_logger,
    make_local_storage,
    hash_matches,
    temporary_file,
    os_cache,
    unique_file_name,
    file_hash,
)
from .downloaders import choose_downloader


def retrieve(url, known_hash, fname=None, path=None, processor=None, downloader=None):
    """
    Download and cache a single file locally.

    Uses HTTP or FTP by default, depending on the protocol in the given *url*.
    Other download methods can be controlled through the *downloader* argument
    (see below).

    The file will be downloaded to a temporary location first and its hash will
    be compared to the given *known_hash*. This is done to ensure that the
    download happened correctly and securely. If the hash doesn't match, the
    file will be deleted and an exception will be raised.

    If the file already exists locally, its hash will be compared to
    *known_hash*. If they are not the same, this is interpreted as the file
    needing to be updated and it will be downloaded again.

    You can bypass these checks by passing ``known_hash=None``. If this is
    done, the SHA256 hash of the downloaded file will be logged to the screen.
    It is highly recommended that you copy and paste this hash as *known_hash*
    so that future downloads are guaranteed to be the exact same file. This is
    crucial for reproducible computations.

    If the file exists in the given *path* with the given *fname* and the hash
    matches, it will not be downloaded and the absolute path to the file will
    be returned.

    .. note::

        This function is meant for downloading single files. If you need to
        manage the download and caching of several files, with versioning, use
        :func:`pooch.create` and :class:`pooch.Pooch` instead.

    Parameters
    ----------
    url : str
        The URL to the file that is to be downloaded. Ideally, the URL should
        end in a file name.
    known_hash : str
        A known hash (checksum) of the file. Will be used to verify the
        download or check if an existing file needs to be updated. By default,
        will assume it's a SHA256 hash. To specify a different hashing method,
        prepend the hash with ``algorithm:``, for example
        ``md5:pw9co2iun29juoh`` or ``sha1:092odwhi2ujdp2du2od2odh2wod2``. If
        None, will NOT check the hash of the downloaded file or check if an
        existing file needs to be updated.
    fname : str or None
        The name that will be used to save the file. Should NOT include the
        full the path, just the file name (it will be appended to *path*). If
        None, will create a unique file name using a combination of the last
        part of the URL (assuming it's the file name) and the MD5 hash of the
        URL. For example, ``81whdo2d2e928yd1wi22:data-file.csv``. This ensures
        that files from different URLs never overwrite each other, even if they
        have the same name.
    path : str or PathLike or None
        The location of the cache folder on disk. This is where the file will
        be saved. If None, will save to a ``pooch`` folder in the default cache
        location for your operating system (see :func:`pooch.os_cache`).
    processor : None or callable
        If not None, then a function (or callable object) that will be called
        before returning the full path and after the file has been downloaded
        (if required). See :meth:`pooch.Pooch.fetch` for details.
    downloader : None or callable
        If not None, then a function (or callable object) that will be called
        to download a given URL to a provided local file name. By default,
        downloads are done through HTTP without authentication using
        :class:`pooch.HTTPDownloader`. See :meth:`pooch.Pooch.fetch` for
        details.

    Returns
    -------
    full_path : str
        The absolute path (including the file name) of the file in the local
        storage.

    Examples
    --------

    Download one of the data files from the Pooch repository on GitHub:

    >>> import os
    >>> from pooch import version, check_version, retrieve
    >>> # Make a URL for the version of pooch we have installed
    >>> url = "https://github.com/fatiando/pooch/raw/{}/data/tiny-data.txt"
    >>> url = url.format(check_version(version.full_version))
    >>> # Download the file and save it locally. Will check the MD5 checksum of
    >>> # the downloaded file against the given value to make sure it's the
    >>> # right file. You can use other hashes by specifying different
    >>> # algorithm names (sha256, sha1, etc).
    >>> fname = retrieve(
    ...     url, known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
    ... )
    >>> with open(fname) as f:
    ...     print(f.read().strip())
    # A tiny data file for test purposes only
    1  2  3  4  5  6
    >>> # Running again won't trigger a download and only return the path to
    >>> # the existing file.
    >>> fname2 = retrieve(
    ...     url, known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
    ... )
    >>> print(fname2 == fname)
    True
    >>> os.remove(fname)

    Files that are compressed with gzip, xz/lzma, or bzip2 can be automatically
    decompressed by passing using the :class:`pooch.Decompress` processor:

    >>> from pooch import Decompress
    >>> # URLs to a gzip compressed version of the data file.
    >>> url = ("https://github.com/fatiando/pooch/raw/{}/"
    ...        + "pooch/tests/data/tiny-data.txt.gz")
    >>> url = url.format(check_version(version.full_version))
    >>> # By default, you would have to decompress the file yourself
    >>> fname = retrieve(
    ...     url,
    ...     known_hash="md5:8812ba10b6c7778014fdae81b03f9def",
    ... )
    >>> print(os.path.splitext(fname)[1])
    .gz
    >>> # Use the processor to decompress after download automatically and
    >>> # return the path to the decompressed file instead.
    >>> fname2 = retrieve(
    ...     url,
    ...     known_hash="md5:8812ba10b6c7778014fdae81b03f9def",
    ...     processor=Decompress(),
    ... )
    >>> print(fname2 == fname)
    False
    >>> with open(fname2) as f:
    ...     print(f.read().strip())
    # A tiny data file for test purposes only
    1  2  3  4  5  6
    >>> os.remove(fname)
    >>> os.remove(fname2)

    When downloading archives (zip or tar), it can be useful to unpack them
    after download to avoid having to do that yourself. Use the processors
    :class:`pooch.Unzip` or :class:`pooch.Untar` to do this automatically:

    >>> from pooch import Unzip
    >>> # URLs to a zip archive with a single data file.
    >>> url = ("https://github.com/fatiando/pooch/raw/{}/"
    ...        + "pooch/tests/data/tiny-data.zip")
    >>> url = url.format(check_version(version.full_version))
    >>> # By default, you would get the path to the archive
    >>> fname = retrieve(
    ...     url,
    ...     known_hash="md5:e9592cb46cf3514a1079051f8a148148",
    ... )
    >>> print(os.path.splitext(fname)[1])
    .zip
    >>> os.remove(fname)
    >>> # Using the processor, the archive will be unzipped and a list with the
    >>> # path to every file will be returned instead of a single path.
    >>> fnames = retrieve(
    ...     url,
    ...     known_hash="md5:e9592cb46cf3514a1079051f8a148148",
    ...     processor=Unzip(),
    ... )
    >>> # There was only a single file in our archive.
    >>> print(len(fnames))
    1
    >>> with open(fnames[0]) as f:
    ...     print(f.read().strip())
    # A tiny data file for test purposes only
    1  2  3  4  5  6
    >>> for f in fnames:
    ...     os.remove(f)


    """
    if path is None:
        path = os_cache("pooch")
    if fname is None:
        fname = unique_file_name(url)
    # Create the local data directory if it doesn't already exist and make the
    # path absolute.
    path = make_local_storage(path, env=None, version=None).resolve()

    full_path = path / fname
    action, verb = download_action(full_path, known_hash)

    if action in ("download", "update"):
        get_logger().info(
            "%s data from '%s' to file '%s'.", verb, url, str(full_path),
        )

        if downloader is None:
            downloader = choose_downloader(url)

        stream_download(url, full_path, known_hash, downloader, pooch=None)

        if known_hash is None:
            get_logger().info(
                "SHA256 hash of downloaded file: %s\n"
                "Use this value as the 'known_hash' argument of 'pooch.retrieve'"
                " to ensure that the file hasn't changed if it is downloaded again"
                " in the future.",
                file_hash(str(full_path)),
            )

    if processor is not None:
        return processor(str(full_path), action, None)

    return str(full_path)


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
    Create a :class:`~pooch.Pooch` with sensible defaults to fetch data files.

    If a version string is given, the Pooch will be versioned, meaning that the
    local storage folder and the base URL depend on the project version. This
    is necessary if your users have multiple versions of your library installed
    (using virtual environments) and you updated the data files between
    versions. Otherwise, every time a user switches environments would trigger
    a re-download of the data. The version string will be appended to the local
    storage path (for example, ``~/.mypooch/cache/v0.1``) and inserted into the
    base URL (for example,
    ``https://github.com/fatiando/pooch/raw/v0.1/data``). If the version string
    contains ``+XX.XXXXX``, it will be interpreted as a development version.

    Parameters
    ----------
    path : str, PathLike, list or tuple
        The path to the local data storage folder. If this is a list or tuple,
        we'll join the parts with the appropriate separator. The *version* will
        be appended to the end of this path. Use :func:`pooch.os_cache` for a
        sensible default.
    base_url : str
        Base URL for the remote data source. All requests will be made relative
        to this URL. The string should have a ``{version}`` formatting mark in
        it. We will call ``.format(version=version)`` on this string. If the
        URL is a directory path, it must end in a ``'/'`` because we will not
        include it.
    version : str or None
        The version string for your project. Should be PEP440 compatible. If
        None is given, will not attempt to format *base_url* and no subfolder
        will be appended to *path*.
    version_dev : str
        The name used for the development version of a project. If your data is
        hosted on Github (and *base_url* is a Github raw link), then
        ``"master"`` is a good choice (default). Ignored if *version* is None.
    env : str or None
        An environment variable that can be used to overwrite *path*. This
        allows users to control where they want the data to be stored. We'll
        append *version* to the end of this value as well.
    registry : dict or None
        A record of the files that are managed by this Pooch. Keys should be
        the file names and the values should be their hashes. Only files
        in the registry can be fetched from the local storage. Files in
        subdirectories of *path* **must use Unix-style separators** (``'/'``)
        even on Windows.
    urls : dict or None
        Custom URLs for downloading individual files in the registry. A
        dictionary with the file names as keys and the custom URLs as values.
        Not all files in *registry* need an entry in *urls*. If a file has an
        entry in *urls*, the *base_url* will be ignored when downloading it in
        favor of ``urls[fname]``.

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
    >>> print(pup.registry_files)
    ['data.txt']

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

    To place the storage folder at a subdirectory, pass in a list and we'll
    join the path for you using the appropriate separator for your operating
    system:

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
    >>> os.environ["MYPROJECT_DATA_DIR"] = os.path.join("myproject", "env")
    >>> pup = create(path=["myproject", "not_env"],
    ...              base_url="http://some.link.com/{version}/",
    ...              version="v0.1",
    ...              env="MYPROJECT_DATA_DIR")
    >>> print(pup.path.parts)
    ('myproject', 'env', 'v0.1')

    """
    if version is not None:
        version = check_version(version, fallback=version_dev)
        base_url = base_url.format(version=version)
    path = make_local_storage(path, env, version)
    pup = Pooch(path=path, base_url=base_url, registry=registry, urls=urls)
    return pup


class Pooch:
    """
    Manager for a local data storage that can fetch from a remote source.

    Avoid creating ``Pooch`` instances directly. Use :func:`pooch.create`
    instead.

    Parameters
    ----------
    path : str
        The path to the local data storage folder. The path must exist in the
        file system.
    base_url : str
        Base URL for the remote data source. All requests will be made relative
        to this URL.
    registry : dict or None
        A record of the files that are managed by this good boy. Keys should be
        the file names and the values should be their hashes. Only files
        in the registry can be fetched from the local storage. Files in
        subdirectories of *path* **must use Unix-style separators** (``'/'``)
        even on Windows.
    urls : dict or None
        Custom URLs for downloading individual files in the registry. A
        dictionary with the file names as keys and the custom URLs as values.
        Not all files in *registry* need an entry in *urls*. If a file has an
        entry in *urls*, the *base_url* will be ignored when downloading it in
        favor of ``urls[fname]``.

    """

    def __init__(self, path, base_url, registry=None, urls=None):
        self.path = path
        self.base_url = base_url
        if registry is None:
            registry = dict()
        self.registry = registry
        if urls is None:
            urls = dict()
        self.urls = dict(urls)

    @property
    def abspath(self):
        "Absolute path to the local storage"
        return Path(os.path.abspath(os.path.expanduser(str(self.path))))

    @property
    def registry_files(self):
        "List of file names on the registry"
        return list(self.registry)

    def fetch(self, fname, processor=None, downloader=None):
        """
        Get the absolute path to a file in the local storage.

        If it's not in the local storage, it will be downloaded. If the hash of
        the file in local storage doesn't match the one in the registry, will
        download a new copy of the file. This is considered a sign that the
        file was updated in the remote storage. If the hash of the downloaded
        file still doesn't match the one in the registry, will raise an
        exception to warn of possible file corruption.

        Post-processing actions sometimes need to be taken on downloaded files
        (unzipping, conversion to a more efficient format, etc). If these
        actions are time or memory consuming, it would be best to do this only
        once when the file is actually downloaded. Use the *processor* argument
        to specify a function that is executed after the downloaded (if
        required) to perform these actions. See below.

        Custom file downloaders can be provided through the *downloader*
        argument. By default, files are downloaded over HTTP. If the server for
        a given file requires authentication (username and password) or if the
        file is served over FTP, use custom downloaders that support these
        features. Downloaders can also be used to print custom messages (like a
        progress bar), etc. See below for details.

        Parameters
        ----------
        fname : str
            The file name (relative to the *base_url* of the remote data
            storage) to fetch from the local storage.
        processor : None or callable
            If not None, then a function (or callable object) that will be
            called before returning the full path and after the file has been
            downloaded (if required). See below for details.
        downloader : None or callable
            If not None, then a function (or callable object) that will be
            called to download a given URL to a provided local file name. By
            default, downloads are done through HTTP without authentication
            using :class:`pooch.HTTPDownloader`. See below for details.

        Returns
        -------
        full_path : str
            The absolute path (including the file name) of the file in the
            local storage.

        Notes
        -----

        **Processor** functions should have the following format:

        .. code:: python

            def myprocessor(fname, action, pooch):
                '''
                Processes the downloaded file and returns a new file name.

                The function **must** take as arguments (in order):

                fname : str
                    The full path of the file in the local data storage
                action : str
                    Either: "download" (file doesn't exist and will be
                    downloaded), "update" (file is outdated and will be
                    downloaded), or "fetch" (file exists and is updated so no
                    download is necessary).
                pooch : pooch.Pooch
                    The instance of the Pooch class that is calling this
                    function.

                The return value can be anything but is usually a full path to
                a file (or list of files). This is what will be returned by
                *fetch* in place of the original file path.
                '''
                ...
                return full_path

        **Downloader** functions should have the following format:

        .. code:: python

            def mydownloader(url, output_file, pooch):
                '''
                Download a file from the given URL to the given local file.

                The function **must** take as arguments (in order):

                url : str
                    The URL to the file you want to download.
                output_file : str or file-like object
                    Path (and file name) to which the file will be downloaded.
                pooch : pooch.Pooch
                    The instance of the Pooch class that is calling this
                    function.

                No return value is required.
                '''
                ...

        **Authentication** through HTTP can be handled by
        :class:`pooch.HTTPDownloader`:

        .. code:: python

            authdownload = HTTPDownloader(auth=(username, password))
            mypooch.fetch("some-data-file.txt", downloader=authdownload)

        **Progress bar** for the download can be printed by
        :class:`pooch.HTTPDownloader` by passing the argument
        ``progressbar=True``:

        .. code:: python

            progress_download = HTTPDownloader(progressbar=True)
            mypooch.fetch("some-data-file.txt", downloader=progress_download)
            # Will print a progress bar to standard error like:
            # 100%|█████████████████████████████████████████| 336/336 [...]

        """
        self._assert_file_in_registry(fname)

        # Create the local data directory if it doesn't already exist
        os.makedirs(str(self.abspath), exist_ok=True)

        url = self.get_url(fname)
        full_path = self.abspath / fname
        known_hash = self.registry[fname]
        action, verb = download_action(full_path, known_hash)

        if action in ("download", "update"):
            get_logger().info(
                "%s file '%s' from '%s' to '%s'.", verb, fname, url, str(self.abspath),
            )

            if downloader is None:
                downloader = choose_downloader(url)

            stream_download(url, full_path, known_hash, downloader, pooch=self)

        if processor is not None:
            return processor(str(full_path), action, self)

        return str(full_path)

    def _assert_file_in_registry(self, fname):
        """
        Check if a file is in the registry and raise :class:`ValueError` if
        it's not.
        """
        if fname not in self.registry:
            raise ValueError("File '{}' is not in the registry.".format(fname))

    def get_url(self, fname):
        """
        Get the full URL to download a file in the registry.

        Parameters
        ----------
        fname : str
            The file name (relative to the *base_url* of the remote data
            storage) to fetch from the local storage.

        """
        self._assert_file_in_registry(fname)
        return self.urls.get(fname, "".join([self.base_url, fname]))

    def load_registry(self, fname):
        """
        Load entries from a file and add them to the registry.

        Use this if you are managing many files.

        Each line of the file should have file name and its hash separated by
        a space. Hash can specify checksum algorithm using "alg:hash" format.
        In case no algorithm is provided, SHA256 is used by default.
        Only one file per line is allowed. Custom download URLs for individual
        files can be specified as a third element on the line.

        Parameters
        ----------
        fname : str | fileobj
            Path (or open file object) to the registry file.

        """
        with contextlib.ExitStack() as stack:
            if hasattr(fname, "read"):
                # It's a file object
                fin = fname
            else:
                # It's a file path
                fin = stack.enter_context(open(fname))

            for linenum, line in enumerate(fin):
                if isinstance(line, bytes):
                    line = line.decode("utf-8")

                elements = line.strip().split()
                if not len(elements) in [0, 2, 3]:
                    raise OSError(
                        "Invalid entry in Pooch registry file '{}': "
                        "expected 2 or 3 elements in line {} but got {}. "
                        "Offending entry: '{}'".format(
                            fname, linenum + 1, len(elements), line
                        )
                    )
                if elements:
                    file_name = elements[0]
                    file_checksum = elements[1]
                    if len(elements) == 3:
                        file_url = elements[2]
                        self.urls[file_name] = file_url
                    self.registry[file_name] = file_checksum

    def is_available(self, fname):
        """
        Check availability of a remote file without downloading it.

        Use this method when working with large files to check if they are
        available for download.

        Parameters
        ----------
        fname : str
            The file name (relative to the *base_url* of the remote data
            storage) to fetch from the local storage.

        Returns
        -------
        status : bool
            True if the file is available for download. False otherwise.

        """
        self._assert_file_in_registry(fname)
        source = self.get_url(fname)
        parsed_url = parse_url(source)
        if parsed_url["protocol"] == "ftp":
            directory = os.path.dirname(parsed_url["path"])
            ftp = ftplib.FTP()
            ftp.connect(host=parsed_url["netloc"])
            try:
                ftp.login()
                available = parsed_url["path"] in ftp.nlst(directory)
            finally:
                ftp.close()
        else:
            response = requests.head(source, allow_redirects=True)
            available = bool(response.status_code == 200)
        return available


def download_action(path, known_hash):
    """
    Determine the action that is needed to get the file on disk.

    Parameters
    ----------
    path : PathLike
        The path to the file on disk.
    known_hash : str
        A known hash (checksum) of the file. Will be used to verify the
        download or check if an existing file needs to be updated. By default,
        will assume it's a SHA256 hash. To specify a different hashing method,
        prepend the hash with ``algorithm:``, for example
        ``md5:pw9co2iun29juoh`` or ``sha1:092odwhi2ujdp2du2od2odh2wod2``.

    Returns
    -------
    action, verb : str
        The action that must be taken and the English verb (infinitive form of
        *action*) used in the log:
        * ``'download'``: File does not exist locally and must be downloaded.
        * ``'update'``: File exists locally but needs to be updated.
        * ``'fetch'``: File exists locally and only need to inform its path.


    """
    if not path.exists():
        action = "download"
        verb = "Downloading"
    elif not hash_matches(str(path), known_hash):
        action = "update"
        verb = "Updating"
    else:
        action = "fetch"
        verb = "Fetching"
    return action, verb


def stream_download(url, fname, known_hash, downloader, pooch=None):
    """
    Stream the file and check that its hash matches the known one.

    The file is first downloaded to a temporary file name in the cache folder.
    It will be moved to the desired file name only if the hash matches the
    known hash. Otherwise, the temporary file is deleted.

    """
    # Ensure the parent directory exists in case the file is in a subdirectory.
    # Otherwise, move will cause an error.
    if not fname.parent.exists():
        os.makedirs(str(fname.parent))

    # Stream the file to a temporary so that we can safely check its hash
    # before overwriting the original.
    with temporary_file(path=str(fname.parent)) as tmp:
        downloader(url, tmp, pooch)
        hash_matches(tmp, known_hash, strict=True, source=str(fname.name))
        shutil.move(tmp, str(fname))
