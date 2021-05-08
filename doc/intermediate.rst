.. _intermediate:

Intermediate tricks
===================

This section covers intermediate configuration that, while not strictly
necessary, you might want to consider using on your project. In particular,
allowing users to **control the local storage location** and **registry files**
are **recommended** for most projects.


User-defined local storage location
-----------------------------------

In the above example, the location of the local storage in the users' computer
is hard-coded. There is no way for them to change it to something else. To
avoid being a tyrant, you can allow the user to define the ``path`` argument
using an environment variable:

.. code:: python

    POOCH = pooch.create(
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


Registry files (dealing with large registries)
----------------------------------------------

If your project has a large number of data files, it can be tedious to list
them in a dictionary. In these cases, it's better to store the file names and
hashes in a file and use :meth:`pooch.Pooch.load_registry` to read them:

.. code:: python

    import os
    import pkg_resources

    POOCH = pooch.create(
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
    POOCH.load_registry(registry_file)

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
    POOCH = pooch.create(
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
    POOCH = pooch.create(
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="master",
        registry=None,
    )
    # If custom URLs are present in the registry file, they will be set
    # automatically.
    POOCH.load_registry(os.path.join(os.path.dirname(__file__), "registry.txt"))


Download protocols
------------------

Pooch supports the HTTP, FTP, and SFTP protocols by default. It will detect the
correct protocol from the URL and use the appropriate download method. For
example, if our data were hosted on an FTP server instead of GitHub, we could
use the following setup:

.. code:: python

    POOCH = pooch.create(
        path=pooch.os_cache("plumbus"),
        # Use an FTP server instead of HTTP. The rest is all the same.
        base_url="ftp://garage-basement.org/{version}/",
        version=version,
        version_dev="master",
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
    )


    def fetch_c137():
        """
        Load the C-137 sample data as a pandas.DataFrame (over FTP this time).
        """
        fname = POOCH.fetch("c137.csv")
        data = pandas.read_csv(fname)
        return data

You can even specify custom functions for the download or login credentials for
authentication. See :ref:`downloaders` for more information.

.. note::

    To download files over SFTP, the package `paramiko
    <https://github.com/paramiko/paramiko>`__ needs to be installed.


Subdirectories
--------------

You can have data files in subdirectories of the remote data store. These files
will be saved to the same subdirectories in the local storage folder. Note,
however, that the names of these files in the registry **must use Unix-style
separators** (``'/'``) even on Windows. We will handle the appropriate
conversions.


.. _tqdm-progressbar:

Printing a download progress bar with ``tqdm``
----------------------------------------------

The :class:`~pooch.HTTPDownloader` can use `tqdm <https://github.com/tqdm/tqdm>`__
to print a download progress bar. This is turned off by default but can be
enabled using:

.. code:: python

    from pooch import HTTPDownloader


    def fetch_large_data():
        """
        Fetch a large file from a server and print a progress bar.
        """
        download = HTTPDownloader(progressbar=True)
        fname = POOCH.fetch("large-data-file.h5", downloader=download)
        data = h5py.File(fname, "r")
        return data

The resulting progress bar will be printed to stderr and should look something
like this:

.. code::

    100%|█████████████████████████████████████████| 336/336 [...]

.. note::

    ``tqdm`` is not installed by default with Pooch. You will have to install
    it separately in order to use this feature.


.. _custom-progressbar:

Using custom progress bars
--------------------------

.. note::

    At the moment, this feature is only available for
    :class:`pooch.HTTPDownloader`.

Alternatively, you can pass an arbitrary object that behaves like a progress
that implements the ``update``, ``reset``, and ``close`` methods. ``update``
should accept a single integer positional argument representing the current
completion (in bytes), while ``reset`` and ``update`` do not take any argument
beside ``self``. The object must also have a ``total`` attribute that can be set
from outside the class.
In other words, the custom progress bar needs to behave like a ``tqdm`` progress bar.
Here's a minimal working example of such a custom "progress display" class

.. code:: python

    import sys

    class MinimalProgressDisplay:
        def __init__(self, total):
            self.count = 0
            self.total = total

        def __repr__(self):
            return str(self.count) + "/" + str(self.total)

        def render(self):
            print(f"\r{self}", file=sys.stderr, end="")

        def update(self, i):
            self.count = i
            self.render()

        def reset(self):
            self.count = 0

        def close(self):
            print("", file=sys.stderr)


An instance of this class can now be passed to an ``HTTPDownloader`` as

.. code:: python

    pbar = MinimalProgressDisplay(total=None)
    download = HTTPDownloader(progressbar=pbar)
