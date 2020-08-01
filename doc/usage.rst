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

You can generate hashes for your data files using ``openssl`` in the terminal:

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
