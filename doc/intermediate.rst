Intermediate tricks
===================

This section covers intermediate configuration that, while not strictly
necessary, you might want to consider using on your project. In particular,
allowing users to **control the local storage location** and **registry files**
are **recommended** for most projects.




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
