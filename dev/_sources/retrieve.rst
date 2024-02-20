.. _retrieve:

Retrieving a single data file
=============================

Basic usage
-----------

If you only want to download one or two data files, use the
:func:`pooch.retrieve` function:

.. code-block:: python

    import pooch


    file_path = pooch.retrieve(
        # URL to one of Pooch's test files
        url="https://github.com/fatiando/pooch/raw/v1.0.0/data/tiny-data.txt",
        known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
    )

The code above will:

1. Check if the file from this URL already exists in Pooch's default cache
   folder (see :func:`pooch.os_cache`).
2. If it doesn't, the file is downloaded and saved to the cache folder.
3. The MD5 `hash <https://en.wikipedia.org/wiki/Cryptographic_hash_function>`__
   is compared against the ``known_hash`` to make sure the file isn't
   corrupted.
4. The function returns the absolute path to the file on your computer.

If the file already existed on your machine, Pooch will check if it's MD5 hash
matches the ``known_hash``:

* If it does, no download happens and the file path is returned.
* If it doesn't, the file is downloaded once more to get an updated version on
  your computer.

Since the download happens only once, you can place this function call at the
start of your script or Jupyter notebook without having to worry about repeat
downloads.
Anyone getting a copy of your code should also get the correct data file the
first time they run it.

.. seealso::

    Pooch can handle multiple download protocols like HTTP, FTP, SFTP, and
    even download from repositories like `figshare <https://www.figshare.com>`__
    and `Zenodo <https://www.zenodo.org>`__ by using the DOI instead of a URL.
    See :ref:`protocols`.

.. seealso::

    You can use **different hashes** by specifying different algorithm names:
    ``sha256:XXXXXX``, ``sha1:XXXXXX``, etc. See :ref:`hashes`.


Unknown file hash
-----------------

If you don't know the hash of the file, you can set ``known_hash=None`` to
bypass the check.
:func:`~pooch.retrieve` will print a log message with the SHA256 hash of the
downloaded file.
**It's highly recommended that you copy and paste this hash into your code
and use it as the** ``known_hash``.

.. tip::

    Setting the ``known_hash`` guarantees that the next time your code is run
    (by you or someone else) the exact same file is downloaded. This helps
    make the results of your code **reproducible**.


Customizing the download
------------------------

The :func:`pooch.retrieve` function supports for all of Pooch's
:ref:`downloaders <downloaders>` and :ref:`processors <processors>`.
You can use HTTP, FTP, and SFTP
(even with :ref:`authentication <authentication>`),
:ref:`decompress files <decompressing>`,
:ref:`unpack archives <unpacking>`,
show :ref:`progress bars <progressbars>`, and more with a bit of configuration.


When not to use ``retrieve``
----------------------------

If you need to manage the download and caching of several files from one or
more sources, then you should start using the full capabilities of the
:class:`pooch.Pooch` class.
It can handle sandboxing
data for different package versions, allow users to set the download
locations, and more.

The classic example is a **Python package that contains several sample
datasets** for use in testing and documentation.

See :ref:`beginner` and :ref:`intermediate` to get started.
