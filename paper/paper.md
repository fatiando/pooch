---
title: "Pooch: A friend to fetch your data files"
tags:
  - python
authors:
  - name: Leonardo Uieda
    orcid: 0000-0001-6123-9515
    affiliation: 1
  - name: Santiago Rubén Soler
    orcid: 0000-0001-9202-5317
    affiliation: "2,3"
  - name: Rémi Rampin
    orcid: 0000-0002-0524-2282
    affiliation: 4
  - name: Hugo van Kemenade
    orcid: 0000-0001-5715-8632
    affiliation: 5
  - name: Matthew Turk
    orcid: 0000-0002-5294-0198
    affiliation: 6
  - name: Daniel Shapero
    orcid: 0000-0002-3651-0649
    affiliation: 7
  - name: Anderson Banihirwe
    orcid: 0000-0001-6583-571X
    affiliation: 8
  - name: John Leeman
    orcid: 0000-0002-3624-1821
    affiliation: 9
affiliations:
 - name: Department of Earth, Ocean and Ecological Sciences, School of Environmental Sciences, University of Liverpool, UK
   index: 1
 - name: Instituto Geofísico Sismológico Volponi, Universidad Nacional de San Juan, Argentina
   index: 2
 - name: CONICET, Argentina
   index: 3
 - name: New York University, USA
   index: 4
 - name: Independent (Non-affiliated)
   index: 5
 - name: University of Illinois at Urbana-Champaign, USA
   index: 6
 - name: Polar Science Center, University of Washington Applied Physics Lab, USA
   index: 7
 - name: The US National Center for Atmospheric Research, USA
   index: 8
 - name: Leeman Geophysical, USA
   index: 9
date: 02 December 2019
bibliography: paper.bib
---

# Summary

Scientific software is usually created to acquire, analyze, model, and visualize data.
As such, many software libraries include sample datasets in their distributions
for use in documentation, tests, benchmarks, and workshops.
A common approach is to include smaller datasets in the GitHub repository
directly and package them with the source and binary distributions
(e.g., scikit-learn [@scikit-learn] and scikit-image [@scikit-image] do this).
As data files increase in size, it becomes unfeasible to store them in GitHub
repositories.
Thus, larger datasets require writing code to download the files from a remote server
to the user's computer.
The same problem is faced by scientists using version control to manage their
research projects.
While downloading a data file over HTTPS can be done easily with modern Python
libraries, it is not trivial to manage a set of files, keep them updated, and
check for corruption.
For example, scikit-learn [@scikit-learn], Cartopy [@cartopy], and PyVista
[@pyvista] all include code dedicated to this particular task.
Instead of scientists and library authors recreating the same code, it would be
best to have a minimalistic and easy to set up tool for fetching and maintaining
data files.

Pooch is a Python library that fills this gap.
It manages a data *registry* (containing file names, SHA-256 cryptographic hashes, and
download URLs) by downloading files from one or more remote servers and storing
them in a local data cache.
Pooch is written in pure Python and has minimal dependencies.
It can be easily installed from the Python Package Index (PyPI) and conda-forge
on a wide range of Python versions: 2.7 (up to Pooch 0.6.0) and from 3.5 to 3.8.
The integrity of downloads is verified by comparing the file's SHA-256 hash with
the one stored in the data registry.
This is also the mechanism used to detect if a file needs to be re-downloaded
due to an update in the registry.
Pooch is meant to be a drop-in replacement for the custom download code that
users have already written (or are planning to write).
In the ideal scenario, the end-user of a software package should not need to know that
Pooch is being used.
Setup is as easy as calling a single function (`pooch.create`), including
setting up an environment variable for overwriting the data cache path and
versioning the downloads so that multiple versions of the same package can
coexist in the same machine.
For example, this is the code required to set up a module
`datasets.py` that uses Pooch to manage data downloads:

```python
import pooch

# Get the version string from the project
from . import version

# Create a new instance of pooch.Pooch
GOODBOY = pooch.create(
    # Cache path using the default for the operating system
    path=pooch.os_cache("myproject"),
    # Base URL of the remote data server (for example, on GitHub)
    base_url="https://github.com/me/myproject/raw/{version}/data/",
    # PEP 440 compliant version number (added to path and base_url)
    version=version,
    # An environment variable that overwrites the path
    env="MYPROJECT_DATA_DIR",
)
# Load the registry from a simple text file.
# Each line has: file_name sha256 [url]
GOODBOY.load_registry("registry.txt")

def fetch_some_data():
    # Get the path to the data file in the local cache
    # If it's not there or needs updating, download it
    fname = GOODBOY.fetch("some-data.csv")
    # Load it with NumPy/pandas/xarray/etc.
    data = pandas.read_csv(fname)
    return data
```

Pooch is designed to be extended: users can plug in custom download functions
and post-download processing functions.
For example, a custom download function could fetch files from a
password-protected FTP server (the default is HTTP/HTTPS or anonymous FTP) and
a processing function could decrypt a file using a user-defined password once
the download is completed.
We include ready-made download functions for HTTP and FTP (including basic
authentication) as well as processing functions for unpacking archives (zip or
tar) and decompressing files (gzip, lzma, and bzip2).

To the best of the authors' awareness, the only other Python software with some
overlapping functionality are [Intake](https://github.com/intake/intake) and
[fsspec](https://github.com/intake/filesystem_spec) (which is used by Intake).
The fsspec library provides a unified interface for defining file systems and
opening files, regardless of where the files are located (local system,
HTTPS/FTP servers, Amazon S3, Google Cloud Storage, etc).
fsspec implements similar download and caching functionality to
the one in Pooch, but has a wider range of download methods available.
In the future, fsspec could be used as a backend to expand Pooch's download
capabilities beyond HTTPS and FTP.
Intake manages data catalogues (with download locations and extensive
metadata), data download and caching, data loading, visualization, and
browsing.
It has built-in capabilities for loading data into standard containers,
including NumPy, pandas, and xarray.
While Intake and fsspec are powerful and highly configurable tools,
we argue that Pooch's strong points are its simplicity, straight-forward
documentation, and focus on solving a single problem.

The Pooch API is stable and has been field-tested by other projects:
MetPy [@metpy], Verde [@verde], RockHound [@rockhound], predictatops
[@predictatops], and icepack [@icepack].
Pooch is also being implemented as the download manager for scikit-image
([GitHub pull request number 3945](https://github.com/scikit-image/scikit-image/pull/3945)),
which will allow the project to use larger sample data while simultaneously
reducing the download size of source and binary distributions.


# Acknowledgements

We would like to thank all of the volunteers who have dedicated their time and
energy to build the open-source ecosystem on which our work relies.
The order of authors is based on number of commits to the GitHub repository.
A full list of all contributors to the project can be found on the
[GitHub repository](https://github.com/fatiando/pooch/graphs/contributors).


# References
