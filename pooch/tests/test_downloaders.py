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
from .utils import pooch_test_url, check_large_data


# FTP doesn't work on Travis CI so need to be able to skip tests there
ON_TRAVIS = bool(os.environ.get("TRAVIS", None))
BASEURL = pooch_test_url()


def test_unsupported_protocol():
    "Should raise ValueError when protocol not in {'https', 'http', 'ftp'}"
    with pytest.raises(ValueError):
        choose_downloader("httpup://some-invalid-url.com")


# https://blog.travis-ci.com/2018-07-23-the-tale-of-ftp-at-travis-ci
@pytest.mark.skipif(ON_TRAVIS, reason="FTP is not allowed on Travis CI")
def test_ftp_downloader():
    "Test ftp downloader"
    with TemporaryDirectory() as local_store:
        downloader = FTPDownloader()
        url = "ftp://speedtest.tele2.net/100KB.zip"
        outfile = os.path.join(local_store, "100KB.zip")
        downloader(url, outfile, None)
        assert os.path.exists(outfile)


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
@pytest.mark.skipif(ON_TRAVIS, reason="FTP is not allowed on Travis CI")
def test_downloader_progressbar_ftp(capsys):
    "Setup an FTP downloader function that prints a progress bar for fetch"
    download = FTPDownloader(progressbar=True)
    with TemporaryDirectory() as local_store:
        url = "ftp://speedtest.tele2.net/100KB.zip"
        outfile = os.path.join(local_store, "100KB.zip")
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
        # Check that the file was actually downloaded
        assert os.path.exists(outfile)
