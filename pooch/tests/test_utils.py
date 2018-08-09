"""
Test the utility functions.
"""
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from ..utils import make_registry

DATA_DIR = str(Path(os.path.dirname(__file__), "data", "store").expanduser().resolve())
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
    finally:
        os.remove(outfile.name)
