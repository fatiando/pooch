.. _progressbars:

Printing progress bars
======================

.. _tqdm-progressbar:

Using ``tqdm`` progress bars
----------------------------

Pooch uses `tqdm <https://github.com/tqdm/tqdm>`__ to print a download progress
bar. This is turned off by default but can be enabled using
``progressbar=True`` in :func:`pooch.retrieve`:

.. code:: python

    fname = retrieve(
        url="https://some-data-server.org/a-data-file.nc",
        known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
        progressbar=True,
    )


The resulting progress bar will be printed to the standard error stream
(STDERR) and should look something like this:

.. code::

    100%|█████████████████████████████████████████| 336/336 [...]


You can also do the same with :meth:`pooch.Pooch.fetch`:

.. code:: python

    POOCH = pooch.create(
        ...
    )

    fname = POOCH.fetch(
        "large-data-file.h5",
        progressbar=True,
    )

Alternatively, you can pass ``progressbar=True`` directly into one of our
:ref:`downloaders <downloaders>`:

.. code:: python

    # Using fetch
    fname = POOCH.fetch(
        "large-data-file.h5",
        downloader=pooch.HTTPDownloader(progressbar=True),
    )

    # Using retrieve
    fname = retrieve(
        url="https://some-data-server.org/a-data-file.nc",
        known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
        downloader=pooch.HTTPDownloader(progressbar=True),
    )

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
that implements the ``update``, ``reset``, and ``close`` methods:

* ``update`` should accept a single integer positional argument representing
  the current completion (in bytes).
* ``reset`` and ``close`` do not take any argument beside ``self``.

The object must also have a ``total`` attribute that can be set from outside
the class.
In other words, the custom progress bar needs to behave like a ``tqdm``
progress bar.

Here's a minimal working example of such a custom "progress display" class:

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


An instance of this class can now be passed to an ``HTTPDownloader`` as:

.. code:: python

    # Assuming you have a pooch.Pooch instance setup
    POOCH = pooch.create(
        ...
    )

    minimal_progress = MinimalProgressDisplay(total=None)

    fname = POOCH.fetch(
        "large-data-file.h5",
        downloader=pooch.HTTPDownloader(progressbar=minimal_progress),
    )
