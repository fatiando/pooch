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
date: 23 October 2019
bibliography: paper.bib
---

# Summary

Scientific software are usually created to analyze, model, and/or visualize
data.
As such, many software libraries include sample datasets in their distributions
for use in documentation, tests, benchmarks, and workshops.
Prominent examples in Python include scikit-learn [@scikit-learn] and
scikit-image [@scikit-image].
The usual approach is to include smaller datasets in the GitHub repository
directly and package them with the source and binary distributions.
Larger datasets require writing code to download the files from a remote server
to the users computer.
The same problem is faced by scientists using version control to manage their
research projects.
As data files increase in size, it becomes unfeasible to store them on GitHub
repositories.
While downloading a data file over HTTP can be done easily with modern Python
libraries, it is not trivial to manage a set of files, keep them updated, and
check for corruption.
Instead of scientists and library authors recreating the same code, it would be
best to have a minimalistic and easy to setup tool for fetching and maintaining
data files.

Pooch is a Python library that fills this gap.
It manages a data *registry* by downloading files from one or more remote
servers and storing them in a local data cache.
Pooch is written in pure Python and has minimal dependencies.
The integrity of downloads is verified by comparing the file's SHA256 hash with
the one stored in the data registry.
This is also the mechanism used to detect if a file needs to be re-downloaded
due to an update in the registry.
Pooch is meant to be a drop-in replacement for the custom download code that
users have already written (or are planning to write).
In the ideal scenario, the end user of a software should not need to know that
Pooch is being used.
Setup is as easy as calling a single function (`pooch.create`), including
setting up an environment variable for overwriting the data cache path and
versioning the downloads so that multiple versions of the same package can
coexist in the same machine.
For example, this is the code required to setup a module
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
    # PEP440 compliant version number (added to path and base_url)
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
    # Load it with numpy/pandas/xarray/etc
    data = pandas.read_csv(fname)
    return data
```

Pooch is designed to be extended: users can plug-in custom download functions
and post-download processing functions.
For example, a custom download function could fetch files over FTP instead of
HTTP (the default) and a processing function could decrypt a file using a
user-defined password once the download is completed.
We include ready-made download functions for HTTP (including basic
authentication) and processing functions for unpacking archives (zip or tar)
and decompressing files (gzip, lzma, and bzip2).

To the best of the authors awareness, the only other Python software with some
overlapping functionality is [Intake](https://github.com/intake/intake).
While Intake is powerful and can be used to manage large data archives,
we argue that Pooch is has a simpler setup and meets the
specific needs of scientific software authors and individual scientists.
For example, Pooch does not require users to change their data loading code to
fit into its plug-in structure, instead only providing the file path for the
user.

How Pooch is already being used (cite relevant packages and mention
scikit-image PR).


# Acknowledgements

I would like to thank all of the volunteers who have dedicated their time and
energy to build the open-source ecosystem on which our work relies.
The order of authors is based on number of commits to the GitHub repository.
A full list of all contributors to the project can be found at
https://github.com/fatiando/pooch/graphs/contributors

# References
