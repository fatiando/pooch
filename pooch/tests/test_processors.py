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


@pytest.mark.network
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


@pytest.mark.network
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


@pytest.mark.network
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


@pytest.mark.network
@pytest.mark.parametrize(
    "target_path", [None, "some_custom_path"], ids=["default_path", "custom_path"]
)
@pytest.mark.parametrize(
    "archive,members",
    [
        ("store", None),  # all files in an archive
        ("tiny-data", ["tiny-data.txt"]),  # 1 compressed file
        ("store", ["store/subdir/tiny-data.txt"]),  # 1 file in a subdir
        ("store", ["store/subdir"]),  # whole subdir
    ],
    ids=["all_files", "single_file", "subdir_file", "subdir_whole"],
)
@pytest.mark.parametrize(
    "processor_class,extension",
    [(Unzip, ".zip"), (Untar, ".tar.gz")],
    ids=["Unzip", "Untar"],
)
def test_unpacking(processor_class, extension, target_path, archive, members):
    "Tests the behaviour of processors for unpacking archives (Untar, Unzip)"
    processor = processor_class(members=members, extract_dir=target_path)
    if target_path is None:
        target_path = archive + extension + processor.suffix
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        # Generate the appropriate expected paths and log message depending on
        # the parameters for the test
        if archive == "tiny-data":
            true_paths = {str(path / target_path / "tiny-data.txt")}
            log_line = "Extracting 'tiny-data.txt'"
        elif archive == "store" and members is None:
            true_paths = {
                str(path / target_path / "store" / "tiny-data.txt"),
                str(path / target_path / "store" / "subdir" / "tiny-data.txt"),
            }
            name = processor_class.__name__
            log_line = f"{name}{name[-1]}ing contents"
        elif archive == "store" and members is not None:
            true_paths = {
                str(path / target_path / Path(*members[0].split("/"))),
            }
            log_line = f"Extracting '{members[0]}'"
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Capture logs and check for the right processor message
        with capture_log() as log_file:
            fnames = pup.fetch(archive + extension, processor=processor)
            assert set(fnames) == true_paths
            lines = log_file.getvalue().splitlines()
            assert len(lines) == 2
            assert lines[0].split()[0] == "Downloading"
            assert lines[-1].startswith(log_line)
        for fname in fnames:
            check_tiny_data(fname)
        # Check that processor doesn't execute when not downloading
        with capture_log() as log_file:
            fnames = pup.fetch(archive + extension, processor=processor)
            assert set(fnames) == true_paths
            assert log_file.getvalue() == ""
        for fname in fnames:
            check_tiny_data(fname)
