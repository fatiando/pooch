"""
Test the processor hooks
"""
from pathlib import Path

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory
import warnings

import pytest

from .. import Pooch
from ..processors import Unzip, Untar, ExtractorProcessor, Decompress

from .utils import pooch_test_url, pooch_test_registry, check_tiny_data


REGISTRY = pooch_test_registry()
BASEURL = pooch_test_url()


@pytest.mark.parametrize(
    "method,ext",
    [("auto", "xz"), ("lzma", "xz"), ("xz", "xz"), ("bzip2", "bz2"), ("gzip", "gz")],
    ids=["auto", "lzma", "xz", "bz2", "gz"],
)
def test_decompress(method, ext):
    "Check that decompression after download works for all formats"
    processor = Decompress(method=method)
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        true_path = str(path / ".".join(["tiny-data.txt", ext, "decomp"]))
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Check the warnings when downloading and from the processor
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("tiny-data.txt." + ext, processor=processor)
            assert len(warn) == 2
            assert all(issubclass(w.category, UserWarning) for w in warn)
            assert str(warn[-2].message).split()[0] == "Downloading"
            assert str(warn[-1].message).startswith("Decompressing")
            assert method in str(warn[-1].message)
        assert fname == true_path
        check_tiny_data(fname)
        # Check that processor doesn't execute when not downloading
        with warnings.catch_warnings(record=True) as warn:
            fname = pup.fetch("tiny-data.txt." + ext, processor=processor)
            assert not warn
        assert fname == true_path
        check_tiny_data(fname)


def test_decompress_fails():
    "Should fail if method='auto' and no extension is given in the file name"
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        with pytest.raises(ValueError) as exception:
            with warnings.catch_warnings():
                pup.fetch("tiny-data.txt", processor=Decompress(method="auto"))
        assert exception.value.args[0].startswith("Unrecognized extension '.txt'")
        # Should also fail for a bad method name
        with pytest.raises(ValueError) as exception:
            with warnings.catch_warnings():
                pup.fetch("tiny-data.txt", processor=Decompress(method="bla"))
        assert exception.value.args[0].startswith("Invalid compression method 'bla'")


@pytest.mark.parametrize(
    "method,ext", [("lzma", "xz"), ("bzip2", "bz2")], ids=["lzma", "bz2"]
)
def test_decompress_27_missing_dependencies(method, ext):
    "Raises an exception when missing extra dependencies for 2.7"
    decompress = Decompress(method=method)
    decompress.modules[method] = None
    with pytest.raises(ValueError) as exception:
        with warnings.catch_warnings():
            decompress(fname="meh.txt." + ext, action="download", pooch=None)
    assert method in exception.value.args[0]


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
    "Setup a post-download hook and make sure it's only executed when downloading"
    processor = proc_cls(members=["tiny-data.txt"])
    suffix = proc_cls.suffix
    extract_dir = "tiny-data" + ext + suffix
    with TemporaryDirectory() as local_store:
        path = Path(local_store)
        true_path = str(path / extract_dir / "tiny-data.txt")
        # Setup a pooch in a temp dir
        pup = Pooch(path=path, base_url=BASEURL, registry=REGISTRY)
        # Check the warnings when downloading and from the processor
        with warnings.catch_warnings(record=True) as warn:
            fnames = pup.fetch("tiny-data" + ext, processor=processor)
            fname = fnames[0]
            assert len(fnames) == 1
            assert len(warn) == 2
            assert all(issubclass(w.category, UserWarning) for w in warn)
            assert str(warn[-2].message).split()[0] == "Downloading"
            assert str(warn[-1].message).startswith("Extracting 'tiny-data.txt'")
        assert fname == true_path
        check_tiny_data(fname)
        # Check that processor doesn't execute when not downloading
        with warnings.catch_warnings(record=True) as warn:
            fnames = pup.fetch("tiny-data" + ext, processor=processor)
            fname = fnames[0]
            assert len(fnames) == 1
            assert not warn
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
        # Check the warnings when downloading and from the processor
        with warnings.catch_warnings(record=True) as warn:
            fnames = pup.fetch("store" + ext, processor=processor)
            assert len(warn) == 2
            assert all(issubclass(w.category, UserWarning) for w in warn)
            assert str(warn[-2].message).split()[0] == "Downloading"
            assert str(warn[-1].message).startswith("{} contents".format(msg))
            assert len(fnames) == 2
            assert true_paths == set(fnames)
            for fname in fnames:
                check_tiny_data(fname)
        # Check that processor doesn't execute when not downloading
        with warnings.catch_warnings(record=True) as warn:
            fnames = pup.fetch("store" + ext, processor=processor)
            assert not warn
            assert len(fnames) == 2
            assert true_paths == set(fnames)
            for fname in fnames:
                check_tiny_data(fname)
