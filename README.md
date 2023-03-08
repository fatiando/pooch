<img src="https://github.com/fatiando/pooch/raw/main/doc/_static/readme-banner.png" alt="Pooch: A friend to fetch your data files">

<p align="center">
<a href="https://www.fatiando.org/pooch"><strong>Documentation</strong> (latest)</a> •
<a href="https://www.fatiando.org/pooch/dev"><strong>Documentation</strong> (main branch)</a> •
<a href="https://github.com/fatiando/pooch/blob/main/CONTRIBUTING.md"><strong>Contributing</strong></a> •
<a href="https://www.fatiando.org/contact/"><strong>Contact</strong></a>
</p>

<p align="center">
Part of the <a href="https://www.fatiando.org"><strong>Fatiando a Terra</strong></a> project
</p>

<p align="center">
<a href="https://pypi.python.org/pypi/pooch"><img src="http://img.shields.io/pypi/v/pooch.svg?style=flat-square" alt="Latest version on PyPI"></a>
<a href="https://github.com/conda-forge/pooch-feedstock"><img src="https://img.shields.io/conda/vn/conda-forge/pooch.svg?style=flat-square" alt="Latest version on conda-forge"></a>
<a href="https://codecov.io/gh/fatiando/pooch"><img src="https://img.shields.io/codecov/c/github/fatiando/pooch/main.svg?style=flat-square" alt="Test coverage status"></a>
<a href="https://pypi.python.org/pypi/pooch"><img src="https://img.shields.io/pypi/pyversions/pooch.svg?style=flat-square" alt="Compatible Python versions."></a>
<a href="https://doi.org/10.21105/joss.01943"><img src="https://img.shields.io/badge/doi-10.21105%2Fjoss.01943-blue?style=flat-square" alt="DOI used to cite Pooch"></a>
</p>

## About

*Does your Python package include sample datasets?
Are you shipping them with the code?
Are they getting too big?*

**Pooch** is here to help! It will manage a data *registry* by downloading your
data files from a server only when needed and storing them locally in a data
*cache* (a folder on your computer).

Here are Pooch's main features:

* Pure Python and minimal dependencies.
* Download a file only if necessary (it's not in the data cache or needs to be
  updated).
* Verify download integrity through SHA256 hashes (also used to check if a file
  needs to be updated).
* Designed to be extended: plug in custom download (FTP, scp, etc) and
  post-processing (unzip, decompress, rename) functions.
* Includes utilities to unzip/decompress the data upon download to save loading
  time.
* Can handle basic HTTP authentication (for servers that require a login) and
  printing download progress bars.
* Easily set up an environment variable to overwrite the data cache location.

*Are you a scientist or researcher? Pooch can help you too!*

* Automatically download your data files so you don't have to keep them in your
  GitHub repository.
* Make sure everyone running the code has the same version of the data files
  (enforced through the SHA256 hashes).

## Example

For a **scientist downloading a data file** for analysis:

```python
import pooch
import pandas as pd

# Download a file and save it locally, returning the path to it.
# Running this again will not cause a download. Pooch will check the hash
# (checksum) of the downloaded file against the given value to make sure
# it's the right file (not corrupted or outdated).
fname_bathymetry = pooch.retrieve(
    url="https://github.com/fatiando-data/caribbean-bathymetry/releases/download/v1/caribbean-bathymetry.csv.xz",
    known_hash="md5:a7332aa6e69c77d49d7fb54b764caa82",
)

# Pooch can also download based on a DOI from certain providers.
fname_gravity = pooch.retrieve(
    url="doi:10.5281/zenodo.5882430/southern-africa-gravity.csv.xz",
    known_hash="md5:1dee324a14e647855366d6eb01a1ef35",
)

# Load the data with Pandas
data_bathymetry = pd.read_csv(fname_bathymetry)
data_gravity = pd.read_csv(fname_gravity)
```

For **package developers** including sample data in their projects:

```python
"""
Module mypackage/datasets.py
"""
import pkg_resources
import pandas
import pooch

# Get the version string from your project. You have one of these, right?
from . import version

# Create a new friend to manage your sample data storage
GOODBOY = pooch.create(
    # Folder where the data will be stored. For a sensible default, use the
    # default cache folder for your OS.
    path=pooch.os_cache("mypackage"),
    # Base URL of the remote data store. Will call .format on this string
    # to insert the version (see below).
    base_url="https://github.com/myproject/mypackage/raw/{version}/data/",
    # Pooches are versioned so that you can use multiple versions of a
    # package simultaneously. Use PEP440 compliant version number. The
    # version will be appended to the path.
    version=version,
    # If a version as a "+XX.XXXXX" suffix, we'll assume that this is a dev
    # version and replace the version with this string.
    version_dev="main",
    # An environment variable that overwrites the path.
    env="MYPACKAGE_DATA_DIR",
    # The cache file registry. A dictionary with all files managed by this
    # pooch. Keys are the file names (relative to *base_url*) and values
    # are their respective SHA256 hashes. Files will be downloaded
    # automatically when needed (see fetch_gravity_data).
    registry={"gravity-data.csv": "89y10phsdwhs09whljwc09whcowsdhcwodcydw"}
)
# You can also load the registry from a file. Each line contains a file
# name and it's sha256 hash separated by a space. This makes it easier to
# manage large numbers of data files. The registry file should be packaged
# and distributed with your software.
GOODBOY.load_registry(
    pkg_resources.resource_stream("mypackage", "registry.txt")
)

# Define functions that your users can call to get back the data in memory
def fetch_gravity_data():
    """
    Load some sample gravity data to use in your docs.
    """
    # Fetch the path to a file in the local storage. If it's not there,
    # we'll download it.
    fname = GOODBOY.fetch("gravity-data.csv")
    # Load it with numpy/pandas/etc
    data = pandas.read_csv(fname)
    return data
```

## Projects using Pooch

* [SciPy](https://github.com/scipy/scipy)
* [scikit-image](https://github.com/scikit-image/scikit-image)
* [MetPy](https://github.com/Unidata/MetPy)
* [icepack](https://github.com/icepack/icepack)
* [histolab](https://github.com/histolab/histolab)
* [seaborn-image](https://github.com/SarthakJariwala/seaborn-image)
* [Ensaio](https://github.com/fatiando/ensaio)
* [Open AR-Sandbox](https://github.com/cgre-aachen/open_AR_Sandbox)
* [climlab](https://github.com/climlab/climlab)
* [napari](https://github.com/napari/napari)
* [mne-python](https://github.com/mne-tools/mne-python)
* [GemGIS](https://github.com/cgre-aachen/gemgis)

*If you're using Pooch, send us a pull request adding your project to the list.*

## Getting involved

🗨️ **Contact us:**
Find out more about how to reach us at
[fatiando.org/contact](https://www.fatiando.org/contact/).

👩🏾‍💻 **Contributing to project development:**
Please read our
[Contributing Guide](https://github.com/fatiando/pooch/blob/main/CONTRIBUTING.md)
to see how you can help and give feedback.

🧑🏾‍🤝‍🧑🏼 **Code of conduct:**
This project is released with a
[Code of Conduct](https://github.com/fatiando/community/blob/main/CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.

> **Imposter syndrome disclaimer:**
> We want your help. **No, really.** There may be a little voice inside your
> head that is telling you that you're not ready, that you aren't skilled
> enough to contribute. We assure you that the little voice in your head is
> wrong. Most importantly, **there are many valuable ways to contribute besides
> writing code**.
>
> *This disclaimer was adapted from the*
> [MetPy project](https://github.com/Unidata/MetPy).

## License

This is free software: you can redistribute it and/or modify it under the terms
of the **BSD 3-clause License**. A copy of this license is provided in
[`LICENSE.txt`](https://github.com/fatiando/pooch/blob/main/LICENSE.txt).
