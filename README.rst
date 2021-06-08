.. image:: https://github.com/fatiando/pooch/raw/master/doc/_static/readme-banner.png
    :alt: Pooch

`Documentation <https://www.fatiando.org/pooch>`__ |
`Documentation (dev version) <https://www.fatiando.org/pooch/dev>`__ |
`Contact <http://contact.fatiando.org>`__ |
Part of the `Fatiando a Terra <https://www.fatiando.org>`__ project

.. image:: https://img.shields.io/pypi/v/pooch.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.org/project/pooch/
.. image:: https://img.shields.io/conda/vn/conda-forge/pooch.svg?style=flat-square
    :alt: Latest version on conda-forge
    :target: https://github.com/conda-forge/pooch-feedstock
.. image:: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Ffatiando%2Fpooch%2Fbadge%3Fref%3Dmaster&style=flat-square&logo=none
    :alt: GitHub Actions workflow status
    :target: https://github.com/fatiando/pooch/actions
.. image:: https://img.shields.io/codecov/c/github/fatiando/pooch/master.svg?style=flat-square
    :alt: Test coverage status
    :target: https://codecov.io/gh/fatiando/pooch
.. image:: https://img.shields.io/pypi/pyversions/pooch.svg?style=flat-square
    :alt: Compatible Python versions.
    :target: https://pypi.org/project/pooch/
.. image:: https://img.shields.io/badge/doi-10.21105%2Fjoss.01943-blue.svg?style=flat-square
    :alt: Digital Object Identifier for the JOSS paper
    :target: https://doi.org/10.21105/joss.01943


About
-----

*Does your Python package include sample datasets? Are you shipping them with the code?
Are they getting too big?*

Pooch is here to help! It will manage a data *registry* by downloading your data files
from a server only when needed and storing them locally in a data *cache* (a folder on
your computer).

Here are Pooch's main features:

* Pure Python and minimal dependencies.
* Download a file only if necessary (it's not in the data cache or needs to be updated).
* Verify download integrity through SHA256 hashes (also used to check if a file needs to
  be updated).
* Designed to be extended: plug in custom download (FTP, scp, etc) and post-processing
  (unzip, decompress, rename) functions.
* Includes utilities to unzip/decompress the data upon download to save loading time.
* Can handle basic HTTP authentication (for servers that require a login) and printing
  download progress bars.
* Easily set up an environment variable to overwrite the data cache location.

*Are you a scientist or researcher? Pooch can help you too!*

* Automatically download your data files so you don't have to keep them in your GitHub
  repository.
* Make sure everyone running the code has the same version of the data files (enforced
  through the SHA256 hashes).


Example
-------

For a **scientist downloading a data file** for analysis:

.. code:: python

    from pooch import retrieve


    # Download the file and save it locally. Running this again will not cause
    # a download. Pooch will check the hash (checksum) of the downloaded file
    # against the given value to make sure it's the right file (not corrupted
    # or outdated).
    fname = retrieve(
        url="https://some-data-server.org/a-data-file.nc",
        known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
    )


For **package developers** including sample data in their projects:

.. code:: python

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
        version_dev="master",
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


Projects using Pooch
--------------------

* `scikit-image <https://github.com/scikit-image/scikit-image>`__
* `MetPy <https://github.com/Unidata/MetPy>`__
* `Verde <https://github.com/fatiando/verde>`__
* `Harmonica <https://github.com/fatiando/harmonica>`__
* `RockHound <https://github.com/fatiando/rockhound>`__
* `icepack <https://github.com/icepack/icepack>`__
* `histolab <https://github.com/histolab/histolab>`__
* `seaborn-image <https://github.com/SarthakJariwala/seaborn-image>`__

*If you're using Pooch, send us a pull request adding your project to the list.*


Contacting Us
-------------

* Most discussion happens `on Github <https://github.com/fatiando/pooch>`__.
  Feel free to `open an issue
  <https://github.com/fatiando/pooch/issues/new>`__ or comment
  on any open issue or pull request.
* We have `chat room on Slack <http://contact.fatiando.org>`__ where you can
  ask questions and leave comments.


Citing Pooch
------------

This is research software **made by scientists** (see
`AUTHORS.md <https://github.com/fatiando/pooch/blob/master/AUTHORS.md>`__). Citations
help us justify the effort that goes into building and maintaining this project. If you
used Pooch for your research, please consider citing us.

See our `CITATION.rst file <https://github.com/fatiando/pooch/blob/master/CITATION.rst>`__
to find out more.


Contributing
------------

Code of conduct
+++++++++++++++

Please note that this project is released with a
`Contributor Code of Conduct <https://github.com/fatiando/pooch/blob/master/CODE_OF_CONDUCT.md>`__.
By participating in this project you agree to abide by its terms.

Contributing Guidelines
+++++++++++++++++++++++

Please read our
`Contributing Guide <https://github.com/fatiando/pooch/blob/master/CONTRIBUTING.md>`__
to see how you can help and give feedback.

Imposter syndrome disclaimer
++++++++++++++++++++++++++++

**We want your help.** No, really.

There may be a little voice inside your head that is telling you that you're
not ready to be an open source contributor; that your skills aren't nearly good
enough to contribute.
What could you possibly offer?

We assure you that the little voice in your head is wrong.

**Being a contributor doesn't just mean writing code**.
Equally important contributions include:
writing or proof-reading documentation, suggesting or implementing tests, or
even giving feedback about the project (including giving feedback about the
contribution process).
If you're coming to the project with fresh eyes, you might see the errors and
assumptions that seasoned contributors have glossed over.
If you can write any code at all, you can contribute code to open source.
We are constantly trying out new skills, making mistakes, and learning from
those mistakes.
That's how we all improve and we are happy to help others learn.

*This disclaimer was adapted from the*
`MetPy project <https://github.com/Unidata/MetPy>`__.


License
-------

This is free software: you can redistribute it and/or modify it under the terms
of the `BSD 3-clause License <https://github.com/fatiando/pooch/blob/master/LICENSE.txt>`__.
A copy of this license is provided with distributions of the software.
