.. _beginner:

Beginner tricks
===============

This section covers the minimal setup required to use Pooch to manage your data
collection. We highly recommend looking at the :ref:`intermediate` tutorial as
well after you're done with this one.

.. note::

    If you're only looking to download a single file, see :ref:`retrieve`
    instead.


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

We'll set up Pooch to solve your data distribution needs.
In this example, we'll work with the follow assumptions:

1. Your sample data are in a folder of your GitHub repository.
2. You use git tags to mark releases of your project in the history.
3. Your project has a variable that defines the version string.
4. The version string contains an indicator that the current commit is not a
   release (like ``'v1.2.3+12.d908jdl'`` or ``'v0.1+dev'``).

Other use cases can also be handled (see :ref:`intermediate`).
For now, let's say that this is the layout of your repository on GitHub:

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


    POOCH = pooch.create(
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
        fname = POOCH.fetch("c137.csv")
        # The "fetch" method returns the full path to the downloaded data file.
        # All we need to do now is load it with our standard Python tools.
        data = pandas.read_csv(fname)
        return data


    def fetch_cronen():
        """
        Load the Cronenberg sample data as a pandas.DataFrame.
        """
        fname = POOCH.fetch("cronen.csv")
        data = pandas.read_csv(fname)
        return data


The ``POOCH`` returned by :func:`pooch.create` is an instance of the
:class:`~pooch.Pooch` class. The class contains the data registry (files, URLs,
hashes, etc) and handles downloading files from the registry using the
:meth:`~pooch.Pooch.fetch` method.

When the user calls ``plumbus.datasets.fetch_c137()`` for the first time, the
data file will be downloaded and stored in the local storage. In this case,
we're using :func:`pooch.os_cache` to set the local folder to the default cache
location for your OS. You could also provide any other path if you prefer. The
download is only performed once and after that Pooch knows to only return the
path to the already downloaded file.

The setup shown here is the minimum required to use Pooch if your package
follows the assumptions laid out above. Pooch also supports downloading files
from multiple sources (including FTP), and more. See the :ref:`intermediate`
tutorial and the documentation for :func:`pooch.create` and :func:`pooch.Pooch`
for more options.


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


Where to go from here
---------------------

Pooch has more features for handling different download protocols, handling
large registries, downloading from multiple sources, and more. Check out the
:ref:`intermediate` and :ref:`advanced` for more information.

You can also customize the download itself (adding authentication, progress
bars, etc) and apply post-download steps (unzipping an archive, decompressing a
file, etc) through its :ref:`downloaders` and :ref:`processors`.

If you any questions, please feel free to ask on our
`Slack chatroom <http://contact.fatiando.org/>`__ or by opening an
`issue on GitHub <https://github.com/fatiando/pooch/issues>`__.
