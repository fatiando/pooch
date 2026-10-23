# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)

"""Regression tests for archive member selection boundaries."""

from io import BytesIO
from pathlib import Path
from tarfile import TarFile, TarInfo
from zipfile import ZipFile

import pytest

from ..processors import Untar, Unzip

FILES = {
    "selected/ok.txt": b"ok",
    "selected/nested/a.txt": b"nested",
    "selected/ok.txt.bak": b"backup",
    "selected-extra/unexpected.txt": b"unexpected",
    "selectedfile.txt": b"unexpected",
    "other/keep.txt": b"other",
}

SELECTED = {
    "selected/ok.txt",
    "selected/nested/a.txt",
    "selected/ok.txt.bak",
}


def make_archive(path):
    """Create a small ZIP or TAR archive locally."""
    if path.suffix == ".zip":
        with ZipFile(path, "w") as archive:
            for name, data in FILES.items():
                archive.writestr(name, data)
    else:
        with TarFile.open(path, "w") as archive:
            for name, data in FILES.items():
                info = TarInfo(name)
                info.size = len(data)
                archive.addfile(info, BytesIO(data))


@pytest.mark.parametrize(
    ("processor_class", "extension"),
    [(Unzip, ".zip"), (Untar, ".tar")],
    ids=["zip", "tar"],
)
@pytest.mark.parametrize(
    ("members", "expected"),
    [
        (["selected"], SELECTED),
        (["selected/"], SELECTED),
        (["./selected"], SELECTED),
        (["selected/nested"], {"selected/nested/a.txt"}),
        (["selected/ok.txt"], {"selected/ok.txt"}),
        (["selectedfile.txt"], {"selectedfile.txt"}),
        (
            ["selected/ok.txt", "other/keep.txt"],
            {"selected/ok.txt", "other/keep.txt"},
        ),
        (["missing"], set()),
        (None, set(FILES)),
    ],
)
def test_member_selection_boundaries(
    tmp_path, processor_class, extension, members, expected
):
    """Only the requested members should be extracted and returned."""
    archive = tmp_path / f"sample{extension}"
    make_archive(archive)

    processor = processor_class(members=members)
    returned = processor(str(archive), "download", None)
    output = Path(str(archive) + processor.suffix)

    actual = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    }
    returned_paths = {Path(path).relative_to(output).as_posix() for path in returned}

    assert actual == expected
    assert returned_paths == expected


@pytest.mark.parametrize(
    ("processor_class", "extension"),
    [(Unzip, ".zip"), (Untar, ".tar")],
    ids=["zip", "tar"],
)
def test_existing_extraction_filters_returned_files(
    tmp_path, processor_class, extension
):
    """Existing files with similar prefixes must not be returned."""
    archive = tmp_path / f"sample{extension}"
    make_archive(archive)

    processor_class()(str(archive), "download", None)

    processor = processor_class(members=["selected/ok.txt"])
    returned = processor(str(archive), "fetch", None)
    output = Path(str(archive) + processor.suffix)

    returned_paths = {Path(path).relative_to(output).as_posix() for path in returned}

    assert returned_paths == {"selected/ok.txt"}
    assert (output / "selected/ok.txt.bak").exists()
