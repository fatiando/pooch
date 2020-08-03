.. _retrieve:

Retrieving a data file
======================

A common task in data analysis workflows is downloading the data from a
publicly available source. This could be done manually (which can't be easily
reproduced) or programmatically using :mod:`urllib` or :mod:`requests` (which
can require a non-trivial amount of code). Ideally, we should
be checking that the downloaded file is not corrupted with a known
`checksum <https://en.wikipedia.org/wiki/Cryptographic_hash_function>`__.


Getting started
---------------

Pooch is designed to simplify all of these tasks (and more). If you're only
looking to download one or two data files only, Pooch offers the
:func:`pooch.retrieve` function:

.. code-block:: python

    import pooch


    # Download the file and save it locally.
    fname = pooch.retrieve(
        # URL to one of Pooch's test files
        url="https://github.com/fatiando/pooch/raw/v1.0.0/data/tiny-data.txt",
        # Pooch will check the MD5 checksum of the downloaded file against the
        # given value to make sure it haven't been corrupted. You can use other
        # hashes by specifying different algorithm names (sha256, sha1, etc).
        known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
    )

The file is stored locally, by default in a folder called ``pooch`` in the
default cache location of your operating system (see :func:`pooch.os_cache`).
The function returns the full path to the downloaded data file, which you can
then pass to pandas, numpy, xarray, etc, to load into memory.

Running this code a second time will not trigger a download since the file
already exists. So you can place this function call at the start of your script
or Jupyter notebook without having to worry about repeat downloads. Anyone
getting a copy of your code should also get the correct data file the first
time they run it.

If the file is updated on the server and ``known_hash`` is set to the checksum
of the new file, Pooch will automatically detect that the file needs to be
updated and download the new version.


Unknown file hash
-----------------

If you don't know the hash of the file, you can set ``known_hash=None`` to
bypass the check. If this is the case, :func:`~pooch.retrieve` will print a log
message with the SHA256 hash of the downloaded file. **It's highly recommended
that you copy and paste this hash into your code** and use it as the
``known_hash``.

That way, the next time your code is run (by you or someone
else) you can guarantee that the exact same file is downloaded. This is a way
to help make sure the results of your code are reproducible.


Customizing the download
------------------------

Function :func:`pooch.retrieve` has support for all of Pooch's
:ref:`downloaders <downloaders>` and :ref:`processors <processors>`. You can
use HTTP, FTP, and SFTP (with or without authentication), decompress files, unpack
archives, show progress bars, and more with a bit of configuration.


Downloading multiple files
--------------------------

The :func:`pooch.retrieve` function is useful when you have one or two files to
download. If you need to manage the download and caching of several files, with
versioning, then you should start using Pooch's full capabilities. See
:ref:`beginner` to get started.
