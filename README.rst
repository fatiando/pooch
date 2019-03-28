Pooch
=====

    A friend to fetch your sample data files.

`Documentation <http://www.fatiando.org/pooch>`__ |
`Documentation (dev version) <http://www.fatiando.org/pooch/dev>`__ |
`Contact <https://gitter.im/fatiando/fatiando>`__ |
Part of the `Fatiando a Terra <https://www.fatiando.org>`__ project

🚨 **Python 2.7 will only be supported until the Fall of 2019.** 🚨

.. image:: http://img.shields.io/pypi/v/pooch.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.python.org/pypi/pooch
.. image:: http://img.shields.io/travis/fatiando/pooch/master.svg?style=flat-square&label=TravisCI
    :alt: TravisCI build status
    :target: https://travis-ci.org/fatiando/pooch
.. image:: http://img.shields.io/appveyor/ci/fatiando/pooch/master.svg?style=flat-square&label=AppVeyor
    :alt: AppVeyor build status
    :target: https://ci.appveyor.com/project/fatiando/pooch
.. image:: https://img.shields.io/azure-devops/build/fatiando/cb775164-4881-4854-81fd-7eaa170192e0/6/master.svg?label=Azure&style=flat-square
    :alt: Azure Pipelines build status
    :target: https://dev.azure.com/fatiando/pooch/_build
.. image:: https://img.shields.io/codecov/c/github/fatiando/pooch/master.svg?style=flat-square
    :alt: Test coverage status
    :target: https://codecov.io/gh/fatiando/pooch
.. image:: https://img.shields.io/pypi/pyversions/pooch.svg?style=flat-square
    :alt: Compatible Python versions.
    :target: https://pypi.python.org/pypi/pooch
.. image:: https://img.shields.io/gitter/room/fatiando/fatiando.svg?style=flat-square
    :alt: Chat room on Gitter
    :target: https://gitter.im/fatiando/fatiando



TL;DR
-----

.. code:: python

    """
    Module mypackage/datasets.py
    """
    import pooch

    # Get the version string from your project. You have one of these, right?
    from . import version


    # Create a new friend to manage your sample data storage
    GOODBOY = pooch.create(
        # Folder where the data will be stored. For a sensible default, use the default
        # cache folder for your OS.
        path=pooch.os_cache("mypackage"),
        # Base URL of the remote data store. Will call .format on this string to insert
        # the version (see below).
        base_url="https://github.com/myproject/mypackage/raw/{version}/data/",
        # Pooches are versioned so that you can use multiple versions of a package
        # simultaneously. Use PEP440 compliant version number. The version will be
        # appended to the path.
        version=version,
        # If a version as a "+XX.XXXXX" suffix, we'll assume that this is a dev version
        # and replace the version with this string.
        version_dev="master",
        # An environment variable that overwrites the path.
        env="MYPACKAGE_DATA_DIR",
        # The cache file registry. A dictionary with all files managed by this pooch.
        # Keys are the file names (relative to *base_url*) and values are their
        # respective SHA256 hashes. Files will be downloaded automatically when needed
        # (see fetch_gravity_data).
        registry={"gravity-data.csv": "89y10phsdwhs09whljwc09whcowsdhcwodcy0dcuhw"}
    )
    # You can also load the registry from a file. Each line contains a file name and
    # it's sha256 hash separated by a space. This makes it easier to manage large
    # numbers of data files. The registry file should be in the same directory as this
    # module.
    GOODBOY.load_registry("registry.txt")


    # Define functions that your users can call to get back some sample data in memory
    def fetch_gravity_data():
        """
        Load some sample gravity data to use in your docs.
        """
        # Fetch the path to a file in the local storae. If it's not there, we'll
        # download it.
        fname = GOODBOY.fetch("gravity-data.csv")
        # Load it with numpy/pandas/etc
        data = ...
        return data


About
-----

*Does your Python package include sample datasets? Are you shipping them with the code?
Are they getting too big?*

Pooch will manage downloading your sample data files over HTTP from a server and storing
them in a local directory:

* Download a file only if it's not in the local storage.
* Check the SHA256 hash to make sure the file is not corrupted or needs updating.
* If the hash is different from the registry, Pooch will download a new version of the
  file.
* If the hash still doesn't match, Pooch will raise an exception warning of possible
  data corruption.


Projects using Pooch
--------------------

* `MetPy <https://github.com/Unidata/MetPy>`__
* `Verde <https://github.com/fatiando/verde>`__
* `Harmonica <https://github.com/fatiando/harmonica>`__
* `RockHound <https://github.com/fatiando/rockhound>`__

*If you're using Pooch, send us a pull request adding your project to the list.*


Contacting Us
-------------

* Most discussion happens `on Github <https://github.com/fatiando/pooch>`__.
  Feel free to `open an issue
  <https://github.com/fatiando/pooch/issues/new>`__ or comment
  on any open issue or pull request.
* We have `chat room on Gitter <https://gitter.im/fatiando/fatiando>`__ where you can
  ask questions and leave comments.


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
Equality important contributions include:
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
of the **BSD 3-clause License**. A copy of this license is provided in
`LICENSE.txt <https://github.com/fatiando/pooch/blob/master/LICENSE.txt>`__.


Documentation for other versions
--------------------------------

* `Development <http://www.fatiando.org/pooch/dev>`__ (reflects the *master* branch on
  Github)
* `Latest release <http://www.fatiando.org/pooch/latest>`__
* `v0.3.0 <http://www.fatiando.org/pooch/v0.3.0>`__
* `v0.2.1 <http://www.fatiando.org/pooch/v0.2.1>`__
* `v0.2.0 <http://www.fatiando.org/pooch/v0.2.0>`__
* `v0.1.1 <http://www.fatiando.org/pooch/v0.1.1>`__
* `v0.1 <http://www.fatiando.org/pooch/v0.1>`__
