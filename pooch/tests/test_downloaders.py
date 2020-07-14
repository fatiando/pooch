"""
Test the downloader classes and functions separately from the Pooch core.
"""
import os
import sys
from tempfile import TemporaryDirectory

import pytest

try:
    import tqdm
except ImportError:
    tqdm = None

from ..downloaders import HTTPDownloader, FTPDownloader, choose_downloader
from .utils import pooch_test_url, check_large_data, check_tiny_data, data_over_ftp


BASEURL = pooch_test_url()


def test_unsupported_protocol():
    "Should raise ValueError when protocol not in {'https', 'http', 'ftp'}"
    with pytest.raises(ValueError):
        choose_downloader("httpup://some-invalid-url.com")


def test_ftp_downloader(ftpserver):
    "Test ftp downloader"
    with data_over_ftp(ftpserver, "tiny-data.txt") as url:
        with TemporaryDirectory() as local_store:
            downloader = FTPDownloader(port=ftpserver.server_port)
            outfile = os.path.join(local_store, "tiny-data.txt")
            downloader(url, outfile, None)
            check_tiny_data(outfile)


@pytest.mark.skipif(tqdm is not None, reason="tqdm must be missing")
@pytest.mark.parametrize("downloader", [HTTPDownloader, FTPDownloader])
def test_downloader_progressbar_fails(downloader):
    "Make sure an error is raised if trying to use progressbar without tqdm"
    with pytest.raises(ValueError):
        downloader(progressbar=True)


@pytest.mark.skipif(tqdm is None, reason="requires tqdm")
def test_downloader_progressbar(capsys):
    "Setup a downloader function that prints a progress bar for fetch"
    download = HTTPDownloader(progressbar=True)
    with TemporaryDirectory() as local_store:
        fname = "large-data.txt"
        url = BASEURL + fname
        outfile = os.path.join(local_store, "large-data.txt")
        download(url, outfile, None)
        # Read stderr and make sure the progress bar is printed only when told
        captured = capsys.readouterr()
        printed = captured.err.split("\r")[-1].strip()
        assert len(printed) == 79
        if sys.platform == "win32":
            progress = "100%|####################"
        else:
            progress = "100%|████████████████████"
        # Bar size is not always the same so can't reliably test the whole bar.
        assert printed[:25] == progress
        # Check that the downloaded file has the right content
        check_large_data(outfile)


@pytest.mark.skipif(tqdm is None, reason="requires tqdm")
def test_downloader_progressbar_ftp(capsys, ftpserver):
    "Setup an FTP downloader function that prints a progress bar for fetch"
    with data_over_ftp(ftpserver, "tiny-data.txt") as url:
        download = FTPDownloader(progressbar=True, port=ftpserver.server_port)
        with TemporaryDirectory() as local_store:
            outfile = os.path.join(local_store, "tiny-data.txt")
            download(url, outfile, None)
            # Read stderr and make sure the progress bar is printed only when
            # told
            captured = capsys.readouterr()
            printed = captured.err.split("\r")[-1].strip()
            assert len(printed) == 79
            if sys.platform == "win32":
                progress = "100%|####################"
            else:
                progress = "100%|████████████████████"
            # Bar size is not always the same so can't reliably test the whole
            # bar.
            assert printed[:25] == progress
            # Check that the file was actually downloaded
            check_tiny_data(outfile)
