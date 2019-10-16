"""
Test the core class and factory function.
"""
import os
import sys
from pathlib import Path
import tempfile

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory
import warnings

import pytest

try:
    import tqdm
except ImportError:
    tqdm = None

from .. import Pooch, create
from ..utils import file_hash
from ..downloaders import HTTPDownloader

from .utils import (
    pooch_test_url,
    pooch_test_registry,
    check_tiny_data,
    check_large_data,
)


# PermissionError was introduced in Python 3.3. This can be deleted when dropping 2.7
if sys.version_info[0] < 3:
    PermissionError = OSError  # pylint: disable=redefined-builtin,invalid-name


DATA_DIR = str(Path(__file__).parent / "data")
REGISTRY = pooch_test_registry()
BASEURL = pooch_test_url()
REGISTRY_CORRUPTED = {
    # The same data file but I changed the hash manually to a wrong one
    "tiny-data.txt": "098h0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d"
}


def test_pooch_local():
    "Setup a pooch that already has the local data and test the fetch."
    pup = Pooch(path=DATA_DIR, base_url="some bogus URL", registry=REGISTRY)
    true = os.path.join(DATA_DIR, "tiny-data.txt")
    fname = pup.fetch("tiny-data.txt")
    assert true == fname
    check_tiny_data(fname)


def test_pooch_custom_url():
    "Have pooch download the file from URL that is not base_url"
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        urls = {"tiny-data.txt": BASEURL + "tiny-data.txt"}
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url="", registry=REGISTRY, urls=urls)
        # Check that the warning says that the file is being updated
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("tiny-data.txt")
            assert len(warn) == 1
            assert issubclass(warn[-1].category, UserWarning)
            assert str(warn[-1].message).split()[0] == "Downloading"
            assert str(warn[-1].message).split()[-1] == "'{}'.".format(path)
        check_tiny_data(fname)
        # Check that no warnings happen when not downloading
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("tiny-data.txt")
            assert not warn


def test_pooch_download():
    "Setup a pooch that has no local data and needs to download"
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        true_path = str(path / "tiny-data.txt")
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Check that the warning says that the file is being downloaded
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("tiny-data.txt")
            assert len(warn) == 1
            assert issubclass(warn[-1].category, UserWarning)
            assert str(warn[-1].message).split()[0] == "Downloading"
            assert str(warn[-1].message).split()[-1] == "'{}'.".format(path)
        # Check that the downloaded file has the right content
        assert true_path == fname
        check_tiny_data(fname)
        assert file_hash(fname) == REGISTRY["tiny-data.txt"]
        # Check that no warnings happen when not downloading
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("tiny-data.txt")
            assert not warn


def test_pooch_update():
    "Setup a pooch that already has the local data but the file is outdated"
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        # Create a dummy version of tiny-data.txt that is different from the one in the
        # remote storage
        true_path = str(path / "tiny-data.txt")
        with open(true_path, "w") as fin:
            fin.write("different data")
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Check that the warning says that the file is being updated
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("tiny-data.txt")
            assert len(warn) == 1
            assert issubclass(warn[-1].category, UserWarning)
            assert str(warn[-1].message).split()[0] == "Updating"
            assert str(warn[-1].message).split()[-1] == "'{}'.".format(path)
        # Check that the updated file has the right content
        assert true_path == fname
        check_tiny_data(fname)
        assert file_hash(fname) == REGISTRY["tiny-data.txt"]
        # Check that no warnings happen when not downloading
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("tiny-data.txt")
            assert not warn


def test_pooch_corrupted():
    "Raise an exception if the hash of downloaded file doesn't match the registry"
    # Test the case where the file wasn't in the directory
    with TemporaryDirectory() as local_store:
        path = os.path.abspath(local_store)
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY_CORRUPTED)
        with warnings.catch_warnings(record=True) as warn:
            with pytest.raises(ValueError):
                pup.fetch("tiny-data.txt")
            assert len(warn) == 1
            assert issubclass(warn[-1].category, UserWarning)
            assert str(warn[-1].message).split()[0] == "Downloading"
            assert str(warn[-1].message).split()[-1] == "'{}'.".format(path)
    # and the case where the file exists but hash doesn't match
    pup = Pooch(path=DATA_DIR, base_url=BASEURL, registry=REGISTRY_CORRUPTED)
    with warnings.catch_warnings(record=True) as warn:
        with pytest.raises(ValueError):
            pup.fetch("tiny-data.txt")
        assert len(warn) == 1
        assert issubclass(warn[-1].category, UserWarning)
        assert str(warn[-1].message).split()[0] == "Updating"
        assert str(warn[-1].message).split()[-1] == "'{}'.".format(DATA_DIR)


def test_pooch_file_not_in_registry():
    "Should raise an exception if the file is not in the registry."
    pup = Pooch(
        path="it shouldn't matter", base_url="this shouldn't either", registry=REGISTRY
    )
    with pytest.raises(ValueError):
        pup.fetch("this-file-does-not-exit.csv")


def test_pooch_load_registry():
    "Loading the registry from a file should work"
    pup = Pooch(path="", base_url="")
    pup.load_registry(os.path.join(DATA_DIR, "registry.txt"))
    assert pup.registry == REGISTRY
    assert pup.registry_files.sort() == list(REGISTRY).sort()


def test_pooch_load_registry_custom_url():
    "Load the registry from a file with a custom URL inserted"
    pup = Pooch(path="", base_url="")
    pup.load_registry(os.path.join(DATA_DIR, "registry-custom-url.txt"))
    assert pup.registry == REGISTRY
    assert pup.urls == {"tiny-data.txt": "https://some-site/tiny-data.txt"}


def test_pooch_load_registry_invalid_line():
    "Should raise an exception when a line doesn't have two elements"
    pup = Pooch(path="", base_url="", registry={})
    with pytest.raises(IOError):
        pup.load_registry(os.path.join(DATA_DIR, "registry-invalid.txt"))


def test_create_makedirs_permissionerror(monkeypatch):
    "Should warn the user when can't create the local data dir"

    def mockmakedirs(path):  # pylint: disable=unused-argument
        "Raise an exception to mimic permission issues"
        raise PermissionError("Fake error")

    data_cache = os.path.join(os.curdir, "test_permission")
    assert not os.path.exists(data_cache)

    monkeypatch.setattr(os, "makedirs", mockmakedirs)

    with warnings.catch_warnings(record=True) as warn:
        pup = create(
            path=data_cache,
            base_url="",
            version="1.0",
            version_dev="master",
            env="SOME_VARIABLE",
            registry={"afile.txt": "ahash"},
        )
        assert len(warn) == 1
        assert issubclass(warn[-1].category, UserWarning)
        assert str(warn[-1].message).startswith("Cannot write to data cache")
        assert "'SOME_VARIABLE'" in str(warn[-1].message)

    with pytest.raises(PermissionError):
        pup.fetch("afile.txt")


def test_create_newfile_permissionerror(monkeypatch):
    "Should warn the user when can't write to the local data dir"
    # This is a separate function because there should be a warning if the data dir
    # already exists but we can't write to it.

    def mocktempfile(**kwargs):  # pylint: disable=unused-argument
        "Raise an exception to mimic permission issues"
        raise PermissionError("Fake error")

    with TemporaryDirectory() as data_cache:
        os.makedirs(os.path.join(data_cache, "1.0"))
        assert os.path.exists(data_cache)

        monkeypatch.setattr(tempfile, "NamedTemporaryFile", mocktempfile)

        with warnings.catch_warnings(record=True) as warn:
            pup = create(
                path=data_cache,
                base_url="",
                version="1.0",
                version_dev="master",
                env="SOME_VARIABLE",
                registry={"afile.txt": "ahash"},
            )
            assert len(warn) == 1
            assert issubclass(warn[-1].category, UserWarning)
            assert str(warn[-1].message).startswith("Cannot write to data cache")
            assert "'SOME_VARIABLE'" in str(warn[-1].message)

            with pytest.raises(PermissionError):
                pup.fetch("afile.txt")


def test_check_availability():
    "Should correctly check availability of existing and non existing files"
    # Check available remote file
    pup = Pooch(path=DATA_DIR, base_url=BASEURL, registry=REGISTRY)
    assert pup.is_available("tiny-data.txt")
    # Check non available remote file
    pup = Pooch(path=DATA_DIR, base_url=BASEURL + "wrong-url/", registry=REGISTRY)
    assert not pup.is_available("tiny-data.txt")
    # Wrong file name
    registry = {"not-a-real-data-file.txt": "notarealhash"}
    registry.update(REGISTRY)
    pup = Pooch(path=DATA_DIR, base_url=BASEURL, registry=registry)
    assert not pup.is_available("not-a-real-data-file.txt")


def test_downloader(capsys):
    "Setup a downloader function for fetch"

    def download(url, output_file, pup):  # pylint: disable=unused-argument
        "Download through HTTP and warn that we're doing it"
        warnings.warn("downloader executed")
        HTTPDownloader()(url, output_file, pup)

    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Check that the warning says that the file is being downloaded
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("large-data.txt", downloader=download)
            assert len(warn) == 2
            assert all(issubclass(w.category, UserWarning) for w in warn)
            assert str(warn[-2].message).split()[0] == "Downloading"
            assert str(warn[-1].message) == "downloader executed"
        # Read stderr and make sure no progress bar was printed by default
        assert not capsys.readouterr().err
        # Check that the downloaded file has the right content
        check_large_data(fname)
        # Check that no warnings happen when not downloading
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("large-data.txt")
            assert not warn


@pytest.mark.skipif(tqdm is not None, reason="tqdm must be missing")
def test_downloader_progressbar_fails():
    "Make sure an error is raised if trying to use progressbar without tqdm"
    with pytest.raises(ValueError):
        HTTPDownloader(progressbar=True)


@pytest.mark.skipif(tqdm is None, reason="requires tqdm")
def test_downloader_progressbar(capsys):
    "Setup a downloader function that prints a progress bar for fetch"
    download = HTTPDownloader(progressbar=True)
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        fname = pup.fetch("large-data.txt", downloader=download)
        # Read stderr and make sure the progress bar is printed only when told to
        captured = capsys.readouterr()
        if sys.platform == "win32":
            progress = "100%|#########################################| 336/336"
        else:
            progress = "100%|█████████████████████████████████████████| 336/336"
        printed = captured.err.split("\r")[-1].strip()
        assert len(printed) == 79
        assert printed[:55] == progress
        # Check that the downloaded file has the right content
        check_large_data(fname)
