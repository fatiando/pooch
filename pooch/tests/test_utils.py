"""
Test the utility functions.
"""
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from ..core import Pooch
from ..utils import make_registry
from .utils import check_tiny_data

DATA_DIR = str(Path(__file__).parent / "data" / "store")
REGISTRY = (
    "tiny-data.txt baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d\n"
)
REGISTRY_RECURSIVE = (
    "subdir/tiny-data.txt baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d\n"
    "tiny-data.txt baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d\n"
)


def test_registry_builder():
    "Check that the registry builder creates the right file names and hashes"
    outfile = NamedTemporaryFile(delete=False)
    # Need to close the file before writing to it.
    outfile.close()
    try:
        make_registry(DATA_DIR, outfile.name, recursive=False)
        with open(outfile.name) as fout:
            registry = fout.read()
        assert registry == REGISTRY
        # Check that the registry can be used.
        pup = Pooch(path=DATA_DIR, base_url="some bogus URL", registry={})
        pup.load_registry(outfile.name)
        true = os.path.join(DATA_DIR, "tiny-data.txt")
        fname = pup.fetch("tiny-data.txt")
        assert true == fname
        check_tiny_data(fname)
    finally:
        os.remove(outfile.name)


def test_registry_builder_recursive():
    "Check that the registry builder works in recursive mode"
    outfile = NamedTemporaryFile(delete=False)
    # Need to close the file before writing to it.
    outfile.close()
    try:
        make_registry(DATA_DIR, outfile.name, recursive=True)
        with open(outfile.name) as fout:
            registry = fout.read()
        assert registry == REGISTRY_RECURSIVE
        # Check that the registry can be used.
        pup = Pooch(path=DATA_DIR, base_url="some bogus URL", registry={})
        pup.load_registry(outfile.name)
        assert os.path.join(DATA_DIR, "tiny-data.txt") == pup.fetch("tiny-data.txt")
        check_tiny_data(pup.fetch("tiny-data.txt"))
        true = os.path.join(DATA_DIR, "subdir", "tiny-data.txt")
        assert true == pup.fetch("subdir/tiny-data.txt")
        check_tiny_data(pup.fetch("subdir/tiny-data.txt"))
    finally:
        os.remove(outfile.name)
