# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the processor hooks
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import warnings

import pytest

from .. import Pooch
from ..processors import Unzip, Untar, ExtractorProcessor, Decompress

from .utils import pooch_test_url, pooch_test_registry, check_tiny_data, capture_log


REGISTRY = pooch_test_registry()
BASEURL = pooch_test_url()


@pytest.mark.parametrize(
    "method,ext,name",
    [
        ("auto", "xz", None),
        ("lzma", "xz", None),
        ("xz", "xz", None),
        ("bzip2", "bz2", None),
        ("gzip", "gz", None),
        ("gzip", "gz", "different-name.txt"),
    ],
    ids=["auto", "lzma", "xz", "bz2", "gz", "name"],
)
def test_decompress(method, ext, name):
    "Check that decompression after download works for all formats"
    processor = Decompress(method=method, name=name)
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        if name is None:
            true_path = str(path / ".".join(["tiny-data.txt", ext, "decomp"]))
        else:
            true_path = str(path / name)
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Check the logs when downloading and from the processor
        with capture_log() as log_file:
            fname = pup.fetch("tiny-data.txt." + ext, processor=processor)
            logs = log_file.getvalue()
            lines = logs.splitlines()
            assert len(lines) == 2
            assert lines[0].split()[0] == "Downloading"
            assert lines[-1].startswith("Decompressing")
            assert method in lines[-1]
        assert fname == true_path
        check_tiny_data(fname)
        # Check that processor doesn't execute when not downloading
        with capture_log() as log_file:
            fname = pup.fetch("tiny-data.txt." + ext, processor=processor)
            assert log_file.getvalue() == ""
        assert fname == true_path
        check_tiny_data(fname)


def test_decompress_fails():
    "Should fail if method='auto' and no extension is given in the file name"
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Invalid extension
        with pytest.raises(ValueError) as exception:
            with warnings.catch_warnings():
                pup.fetch("tiny-data.txt", processor=Decompress(method="auto"))
        assert exception.value.args[0].startswith("Unrecognized file extension '.txt'")
        assert "pooch.Unzip/Untar" not in exception.value.args[0]
        # Should also fail for a bad method name
        with pytest.raises(ValueError) as exception:
            with warnings.catch_warnings():
                pup.fetch("tiny-data.txt", processor=Decompress(method="bla"))
        assert exception.value.args[0].startswith("Invalid compression method 'bla'")
        assert "pooch.Unzip/Untar" not in exception.value.args[0]
        # Point people to Untar and Unzip
        with pytest.raises(ValueError) as exception:
            with warnings.catch_warnings():
                pup.fetch("tiny-data.txt", processor=Decompress(method="zip"))
        assert exception.value.args[0].startswith("Invalid compression method 'zip'")
        assert "pooch.Unzip/Untar" in exception.value.args[0]
        with pytest.raises(ValueError) as exception:
            with warnings.catch_warnings():
                pup.fetch("store.zip", processor=Decompress(method="auto"))
        assert exception.value.args[0].startswith("Unrecognized file extension '.zip'")
        assert "pooch.Unzip/Untar" in exception.value.args[0]


def test_extractprocessor_fails():
    "The base class should be used and should fail when passed to fecth"
    with TemporaryDirectory() as local_store:
        # Setup a pooch in a temp dir
        pup = Pooch(path=Path(local_store), base_url=BASEURL, registry=REGISTRY)
        processor = ExtractorProcessor()
        with pytest.raises(NotImplementedError) as exception:
            pup.fetch("tiny-data.tar.gz", processor=processor)
        assert "'suffix'" in exception.value.args[0]
        processor.suffix = "tar.gz"
        with pytest.raises(NotImplementedError) as exception:
            pup.fetch("tiny-data.tar.gz", processor=processor)
        assert not exception.value.args


@pytest.mark.parametrize(
    "proc_cls,ext", [(Unzip, ".zip"), (Untar, ".tar.gz")], ids=["Unzip", "Untar"]
)
def test_processors(proc_cls, ext):
    "Setup a hook and make sure it's only executed when downloading"
    processor = proc_cls(members=["tiny-data.txt"])
    suffix = proc_cls.suffix
    extract_dir = "tiny-data" + ext + suffix
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        true_path = str(path / extract_dir / "tiny-data.txt")
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Check the logs when downloading and from the processor
        with capture_log() as log_file:
            fnames = pup.fetch("tiny-data" + ext, processor=processor)
            fname = fnames[0]
            assert len(fnames) == 1
            logs = log_file.getvalue()
            lines = logs.splitlines()
            assert len(lines) == 2
            assert lines[0].split()[0] == "Downloading"
            assert lines[-1].startswith("Extracting 'tiny-data.txt'")

        assert fname == true_path
        check_tiny_data(fname)
        # Check that processor doesn't execute when not downloading
        with capture_log() as log_file:
            fnames = pup.fetch("tiny-data" + ext, processor=processor)
            fname = fnames[0]
            assert len(fnames) == 1
            assert log_file.getvalue() == ""
        assert fname == true_path
        check_tiny_data(fname)


@pytest.mark.parametrize(
    "proc_cls,ext,msg",
    [(Unzip, ".zip", "Unzipping"), (Untar, ".tar.gz", "Untarring")],
    ids=["Unzip", "Untar"],
)
def test_processor_multiplefiles(proc_cls, ext, msg):
    "Setup a processor to unzip/untar a file and return multiple fnames"
    processor = proc_cls()
    suffix = proc_cls.suffix
    extract_dir = "store" + ext + suffix
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        true_paths = {
            str(path / extract_dir / "store" / "tiny-data.txt"),
            str(path / extract_dir / "store" / "subdir" / "tiny-data.txt"),
        }
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Check the logs when downloading and from the processor
        with capture_log() as log_file:
            fnames = pup.fetch("store" + ext, processor=processor)
            logs = log_file.getvalue()
            lines = logs.splitlines()
            assert len(lines) == 2
            assert lines[0].split()[0] == "Downloading"
            assert lines[-1].startswith(f"{msg} contents")
            assert len(fnames) == 2
            assert true_paths == set(fnames)
            for fname in fnames:
                check_tiny_data(fname)
        # Check that processor doesn't execute when not downloading
        with capture_log() as log_file:
            fnames = pup.fetch("store" + ext, processor=processor)
            assert log_file.getvalue() == ""
            assert len(fnames) == 2
            assert true_paths == set(fnames)
            for fname in fnames:
                check_tiny_data(fname)
