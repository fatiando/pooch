.. _intermediate:

Intermediate tricks
===================


User-defined local storage location
-----------------------------------

In the above example, the location of the local storage in the users' computer
is hard-coded. There is no way for them to change it to something else. To
avoid being a tyrant, you can allow the user to define the ``path`` argument
using an environment variable:

.. code:: python

    GOODBOY = pooch.create(
        # This is still the default
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="master",
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
        # The name of an environment variable that can overwrite the path
        env="PLUMBUS_DATA_DIR",
    )

In this case, if the user defines the ``PLUMBUS_DATA_DIR`` environment
variable, we'll use its value instead of ``path``. Pooch will still append the
value of ``version`` to the path, so the value of ``PLUMBUS_DATA_DIR`` should
not include a version number.


Subdirectories
--------------

You can have data files in subdirectories of the remote data store. These files
will be saved to the same subdirectories in the local storage folder. Note,
however, that the names of these files in the registry **must use Unix-style
separators** (``'/'``) even on Windows. We will handle the appropriate
conversions.


Registry files (dealing with large registries)
----------------------------------------------

If your project has a large number of data files, it can be tedious to list
them in a dictionary. In these cases, it's better to store the file names and
hashes in a file and use :meth:`pooch.Pooch.load_registry` to read them:

.. code:: python

    import os
    import pkg_resources

    GOODBOY = pooch.create(
        # Use the default cache folder for the OS
        path=pooch.os_cache("plumbus"),
        # The remote data is on Github
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        # If this is a development version, get the data from the master branch
        version_dev="master",
        # We'll load it from a file later
        registry=None,
    )
    # Get registry file from package_data
    registry_file = pkg_resources.resource_stream("plumbus", "registry.txt")
    # Load this registry file
    GOODBOY.load_registry(registry_file)

In this case, the ``registry.txt`` file is in the ``plumbus/`` package
directory and should be shipped with the package (see below for instructions).
We use `pkg_resources <https://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access>`__
to access the ``registry.txt``, giving it the name of our Python package.

The contents of ``registry.txt`` are:

.. code-block:: none

    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w

A specific hashing algorithm can be enforced, if a checksum for a file is
prefixed with ``alg:``, e.g.

.. code-block:: none

    c137.csv sha1:e32b18dab23935bc091c353b308f724f18edcb5e
    cronen.csv md5:b53c08d3570b82665784cedde591a8b0


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

From Pooch v1.2.0 the registry file can also contain line comments, prepended
with a ``#``, e.g.:

.. code-block:: none

    # C-137 sample data
    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    # Cronenberg sample data
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w

.. note::

    Make sure you set the Pooch version in your ``setup.py`` to >=1.2.0 when
    using comments as earlier versions cannot handle them:
    ``install_requires = [..., "pooch>=1.2.0", ...]``


Creating a registry file
------------------------

If you have many data files, creating the registry and keeping it updated can
be a challenge. Function :func:`pooch.make_registry` will create a registry
file with all contents of a directory. For example, we can generate the
registry file for our fictitious project from the command-line:

.. code:: bash

   $ python -c "import pooch; pooch.make_registry('data', 'plumbus/registry.txt')"


File-specific URLs
------------------

You can set a custom download URL for individual files with the ``urls``
argument of :func:`pooch.create` or :class:`pooch.Pooch`. It should be a
dictionary with the file names as keys and the URLs for downloading the files
as values. For example, say we have a ``citadel.csv`` file that we want to
download from ``https://www.some-data-hosting-site.com`` instead:

.. code:: python

    # The basic setup is the same
    GOODBOY = pooch.create(
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="master",
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
            # Still include the file in the registry
            "citadel.csv": "893yprofwjndcwhx9c0ehp3ue9gcwoscjwdfgh923e0hwhcwiyc",
        },
        # Now specify custom URLs for some of the files in the registry.
        urls={
            "citadel.csv": "https://www.some-data-hosting-site.com/files/citadel.csv",
        },
    )

Notice that versioning of custom URLs is not supported (since they are assumed
to be data files independent of your project) and the file name will not be
appended automatically to the URL (in case you want to change the file name in
local storage).

Custom URLs can be used along side ``base_url`` or you can omit ``base_url``
entirely by setting it to an empty string (``base_url=""``). However, doing so
requires setting a custom URL for every file in the registry.

You can also include custom URLs in a registry file by adding the URL for a
file to end of the line (separated by a space):

.. code-block:: none

    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w
    citadel.csv 893yprofwjndcwhx9c0ehp3ue9gcwoscjwdfgh923e0hwhcwiyc https://www.some-data-hosting-site.com/files/citadel.csv

:meth:`pooch.Pooch.load_registry` will automatically populate the ``urls``
attribute. This way, custom URLs don't need to be set in the code. In fact, the
module code doesn't change at all:

.. code:: python

    # Define the Pooch exactly the same (urls is None by default)
    GOODBOY = pooch.create(
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="master",
        registry=None,
    )
    # If custom URLs are present in the registry file, they will be set
    # automatically.
    GOODBOY.load_registry(os.path.join(os.path.dirname(__file__), "registry.txt"))
