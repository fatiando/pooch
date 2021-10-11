.. _beginner:

Fetching files from a registry
==============================

If you need to manage the download of multiple files from one or more
locations, then this section is for you!

Setup
-----

In the following example we'll assume that:

1. You have several data files served from the same base URL (for example,
   ``"https://www.somewebpage.org/science/data"``).
2. You know the file names and their
   `hashes <https://en.wikipedia.org/wiki/Cryptographic_hash_function>`__.

We will use :func:`pooch.create` to set up our download manager:

.. code:: python

    import pooch


    odie = pooch.create(
        # Use the default cache folder for the operating system
        path=pooch.os_cache("my-project"),
        base_url="https://www.somewebpage.org/science/data/",
        # The registry specifies the files that can be fetched
        registry={
            "temperature.csv": "sha256:19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "gravity-disturbance.nc": "sha256:1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
    )

The return value (``odie``) is an instance of :class:`pooch.Pooch`.
It contains all of the information needed to fetch the data files in our
**registry** and store them in the specified cache folder.

.. note::

    The Pooch **registry** is a mapping of file names and their associated
    hashes (and optionally download URLs).

.. tip::

    If you don't know the hash or are otherwise unable to obtain it, it is
    possible to bypass the check. This is **not recommended** for general use,
    only if it can't be avoided. See :ref:`hashes`.


.. attention::

    You can have data files in **subdirectories** of the remote data store
    (URL).
    These files will be saved to the same subdirectories in the local storage
    folder.

    However, the names of these files in the registry **must use Unix-style
    separators** (``'/'``) **even on Windows**.
    Pooch will handle the appropriate conversions.


Downloading files
-----------------

To download one our data files and load it with `xarray
<http://xarray.pydata.org/>`__:

.. code:: python

    import xarray as xr


    file_path = odie.fetch("gravity-disturbance.nc")
    # Standard use of xarray to load a netCDF file (.nc)
    data = xr.open_dataset(file_path)

The call to :meth:`pooch.Pooch.fetch`  will check if the file already exists in
the cache folder.

If it doesn't:

1. The file is downloaded and saved to the cache folder.
2. The hash of the downloaded file is compared against the one stored in the
   registry to make sure the file isn't corrupted.
3. The function returns the absolute path to the file on your computer.

If it does:

1. Check if it's hash matches the one in the registry.
2. If it does, no download happens and the file path is returned.
3. If it doesn't, the file is downloaded once more to get an updated version on
   your computer.

Why use this method?
--------------------

With :class:`pooch.Pooch`, you can centralize the information about the URLs,
hashes, and files in a single place.
Once the instance is created, it can be used to fetch individual files without
repeating the URL and hash everywhere.

A good way to use this is to place the call to :func:`pooch.create` in Python
module (a ``.py`` file).
Then you can ``import`` the module in ``.py`` scripts or Jupyter notebooks and
use the instance to fetch your data.
This way, you don't need to define the URLs or hashes in multiple
scripts/notebooks.

Customizing the download
------------------------

The :meth:`pooch.Pooch.fetch` method supports for all of Pooch's
:ref:`downloaders <downloaders>` and :ref:`processors <processors>`.
You can use HTTP, FTP, and SFTP
(even with :ref:`authentication <authentication>`),
:ref:`decompress files <decompressing>`,
:ref:`unpack archives <unpacking>`,
show :ref:`progress bars <progressbars>`, and more with a bit of configuration.
