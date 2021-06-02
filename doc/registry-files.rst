.. _registryfiles:

Registry files
==============

Usage
-----

If your project has a large number of data files, it can be tedious to list
them in a dictionary. In these cases, it's better to store the file names and
hashes in a file and use :meth:`pooch.Pooch.load_registry` to read them.

.. code:: python

    import os
    import pkg_resources

    POOCH = pooch.create(
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="main",
        # We'll load it from a file later
        registry=None,
    )
    # Get registry file from package_data
    registry_file = pkg_resources.resource_stream("plumbus", "registry.txt")
    # Load this registry file
    POOCH.load_registry(registry_file)

In this case, the ``registry.txt`` file is in the ``plumbus/`` package
directory and should be shipped with the package (see below for instructions).
We use `pkg_resources <https://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access>`__
to access the ``registry.txt``, giving it the name of our Python package.

Registry file format
--------------------

Registry files are light-weight text files that specify a file's name and hash.
In our example, the contents of ``registry.txt`` are:

.. code-block:: none

    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w

A specific hashing algorithm can be enforced, if a checksum for a file is
prefixed with ``alg:``:

.. code-block:: none

    c137.csv sha1:e32b18dab23935bc091c353b308f724f18edcb5e
    cronen.csv md5:b53c08d3570b82665784cedde591a8b0

From Pooch v1.2.0 the registry file can also contain line comments, prepended
with a ``#``:

.. code-block:: none

    # C-137 sample data
    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    # Cronenberg sample data
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w

.. attention::

    Make sure you set the Pooch version in your ``setup.py`` to >=1.2.0 when
    using comments as earlier versions cannot handle them:
    ``install_requires = [..., "pooch>=1.2.0", ...]``


Packaging registry files
------------------------

To make sure the registry file is shipped with your package, include the
following in your ``MANIFEST.in`` file:

.. code-block:: none

    include plumbus/registry.txt

And the following entry in the ``setup`` function of your ``setup.py`` file:

.. code:: python

    setup(
        ...
        package_data={"plumbus": ["registry.txt"]},
        ...
    )


Creating a registry file
------------------------

If you have many data files, creating the registry and keeping it updated can
be a challenge. Function :func:`pooch.make_registry` will create a registry
file with all contents of a directory. For example, we can generate the
registry file for our fictitious project from the command-line:

.. code:: bash

   $ python -c "import pooch; pooch.make_registry('data', 'plumbus/registry.txt')"


Create registry file from remote files
--------------------------------------

If you want to create a registry file for a large number of data files that are
available for download but you don't have their hashes or any local copies,
you must download them first. Manually downloading each file
can be tedious. However, we can automate the process using
:func:`pooch.retrieve`. Below, we'll explore two different scenarios.

If the data files share the same base url, we can use :func:`pooch.retrieve`
to download them and then use :func:`pooch.make_registry` to create the
registry:

.. code:: python

    import os

    # Names of the data files
    filenames = ["c137.csv", "cronen.csv", "citadel.csv"]

    # Base url from which the data files can be downloaded from
    base_url = "https://www.some-data-hosting-site.com/files/"

    # Create a new directory where all files will be downloaded
    directory = "data_files"
    os.makedirs(directory)

    # Download each data file to data_files
    for fname in filenames:
        path = pooch.retrieve(
            url=base_url + fname, known_hash=None, fname=fname, path=directory
        )

    # Create the registry file from the downloaded data files
    pooch.make_registry("data_files", "registry.txt")

If each data file has its own url, the registry file can be manually created
after downloading each data file through :func:`pooch.retrieve`:

.. code:: python

    import os

    # Names and urls of the data files. The file names are used for naming the
    # downloaded files. These are the names that will be included in the registry.
    fnames_and_urls = {
        "c137.csv": "https://www.some-data-hosting-site.com/c137/data.csv",
        "cronen.csv": "https://www.some-data-hosting-site.com/cronen/data.csv",
        "citadel.csv": "https://www.some-data-hosting-site.com/citadel/data.csv",
    }

    # Create a new directory where all files will be downloaded
    directory = "data_files"
    os.makedirs(directory)

    # Create a new registry file
    with open("registry.txt", "w") as registry:
        for fname, url in fnames_and_urls.items():
            # Download each data file to the specified directory
            path = pooch.retrieve(
                url=url, known_hash=None, fname=fname, path=directory
            )
            # Add the name, hash, and url of the file to the new registry file
            registry.write(
                f"{fname} {pooch.file_hash(path)} {url}\n"
            )

.. warning::

    Notice that there are **no checks for download integrity** (since we don't
    know the file hashes before hand). Only do this for trusted data sources
    and over a secure connection. If you have access to file hashes/checksums,
    **we highly recommend using them** to set the ``known_hash`` argument.
