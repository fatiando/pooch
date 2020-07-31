.. _usage:

Training your Pooch
===================

.. note::

    This section covers the standard use case for Pooch. You can also
    have :ref:`finner control over the download <downloaders>` (authentication,
    progress bars, etc) or specify
    :ref:`post-download processing actions <processors>` (unzip/tar archives,
    decompress files, etc). See :ref:`advanced` for more configuration options.


The problem
-----------

You develop a Python library called ``plumbus`` for analysing data emitted by
interdimensional portals. You want to distribute sample data so that your users
can easily try out the library by copying and pasting from the docs. You want
to have a ``plumbus.datasets`` module that defines functions like
``fetch_c137()`` that will return the data loaded as a
:class:`pandas.DataFrame` for convenient access.


Assumptions
-----------

We'll setup a :class:`~pooch.Pooch` to solve your data distribution needs.
In this example, we'll work with the follow assumptions:

1. Your sample data are in a folder of your Github repository.
2. You use git tags to mark releases of your project in the history.
3. Your project has a variable that defines the version string.
4. The version string contains an indicator that the current commit is not a
   release (like ``'v1.2.3+12.d908jdl'`` or ``'v0.1+dev'``).

Let's say that this is the layout of your repository on GitHub:

.. code-block:: none

    doc/
        ...
    data/
        README.md
        c137.csv
        cronen.csv
    plumbus/
        __init__.py
        ...
        datasets.py
    setup.py
    ...

The sample data are stored in the ``data`` folder of your repository.


Basic setup
-----------

Pooch can download and cache your data files to the users' computer
automatically. This is what the ``plumbus/datasets.py`` file would look like:

.. code:: python

    """
    Load sample data.
    """
    import pandas
    import pooch

    from . import version  # The version string of your project


    GOODBOY = pooch.create(
        # Use the default cache folder for the OS
        path=pooch.os_cache("plumbus"),
        # The remote data is on Github
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        # If this is a development version, get the data from the master branch
        version_dev="master",
        # The registry specifies the files that can be fetched
        registry={
            # The registry is a dict with file names and their SHA256 hashes
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
    )


    def fetch_c137():
        """
        Load the C-137 sample data as a pandas.DataFrame.
        """
        # The file will be downloaded automatically the first time this is run
        # returns the file path to the downloaded file. Afterwards, Pooch finds
        # it in the local cache and doesn't repeat the download.
        fname = GOODBOY.fetch("c137.csv")
        data = pandas.read_csv(fname)
        return data


    def fetch_cronen():
        """
        Load the Cronenberg sample data as a pandas.DataFrame.
        """
        fname = GOODBOY.fetch("cronen.csv")
        data = pandas.read_csv(fname)
        return data


When the user calls ``plumbus.datasets.fetch_c137()`` for the first time, the
data file will be downloaded and stored in the local storage. In this case,
we're using :func:`pooch.os_cache` to set the local folder to the default cache
location for your OS. You could also provide any other path if you prefer. See
the documentation for :func:`pooch.create` for more options.


Download protocols
------------------

Pooch supports the HTTP, FTP, and SFTP protocols by default. It will detect the
correct protocol from the URL and use the appropriate download method. For
example, if our data were hosted on an FTP server instead of GitHub, we could
use the following setup:

.. code:: python

    GOODBOY = pooch.create(
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
        fname = GOODBOY.fetch("c137.csv")
        data = pandas.read_csv(fname)
        return data

You can even specify custom functions for the download or login credentials for
authentication. See :ref:`downloaders` for more information.


Hashes
------

Pooch uses `SHA256 <https://en.wikipedia.org/wiki/SHA-2>`__ hashes by default
to check if files are up-to-date or possibly corrupted:

* If a file exists in the local folder, Pooch will check that its hash matches
  the one in the registry. If it doesn't, we'll assume that it needs to be
  updated.
* If a file needs to be updated or doesn't exist, Pooch will download it from
  the remote source and check the hash. If the hash doesn't match, an exception
  is raised to warn of possible file corruption.

You can generate hashes for your data files using ``openssl`` the terminal:

.. code:: bash

    $ openssl sha256 data/c137.csv
    SHA256(data/c137.csv)= baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d

Or using the :func:`pooch.file_hash` function (which is a convenient way of
calling Python's :mod:`hashlib`):

.. code:: python

    import pooch
    print(pooch.file_hash("data/c137.csv"))

Alternative hashing algorithms supported by :mod:`hashlib` can be used as well:

.. code:: python

    import pooch
    print(pooch.file_hash("data/c137.csv", alg="sha512"))

In this case, you can specify the hash algorithm in the registry by prepending
it to the hash, for example ``"md5:0hljc7298ndo2"`` or
``"sha512:803o3uh2pecb2p3829d1bwouh9d"``. Pooch will understand this and use
the appropriate method.


Versioning
----------

The files from different version of your project will be kept in separate
folders to make sure they don't conflict with each other. This way, you can
safely update data files while maintaining backward compatibility. For example,
if ``path=".plumbus"`` and ``version="v0.1"``, the data folder will be
``.plumbus/v0.1``.

When your project updates, Pooch will automatically setup a separate folder for
the new data files based on the given version string. The remote URL will also
be updated. Notice that there is a format specifier ``{version}`` in the URL
that Pooch substitutes for you.

Versioning is optional and can be ignored by omitting the ``version`` and
``version_dev`` arguments or setting them to ``None``.


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
