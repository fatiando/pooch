Intermediate tricks
===================

This section covers intermediate configuration that, while not strictly
necessary, you might want to consider using on your project. In particular,
allowing users to **control the local storage location** and **registry files**
are **recommended** for most projects.


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
