Intermediate tricks
===================

This section covers intermediate configuration that, while not strictly
necessary, you might want to consider using on your project. In particular,
allowing users to **control the local storage location** and **registry files**
are **recommended** for most projects.


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
