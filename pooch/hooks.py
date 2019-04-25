"""
Download and post-processing hooks for Pooch.fetch
"""
import requests


class HTTPDownloader:  # pylint: disable=too-few-public-methods
    """
    Download manager for fetching files over HTTP/HTTPS.

    When called, downloads the given file URL into the specified local file. Uses the
    :mod:`requests` library to manage downloads.

    All keyword arguments passed to this class will be passed to :func:`requests.get`.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, url, output_file, pooch):
        """
        Download the URL to the given output file.

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
        isfilename = not hasattr(output_file, "write")
        if isfilename:
            output_file = open(output_file, "w+b")
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    output_file.write(chunk)
        finally:
            if isfilename:
                output_file.close()
