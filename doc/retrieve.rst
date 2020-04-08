.. _retrieve:

Downloading a single file
=========================

Sometimes, you just want to download a single file (caching it locally and
checking the hash to make sure you have the right one). In these cases,
:class:`pooch.Pooch` is overkill and requires too much setup.

For that, :func:`pooch.retrieve` is what you want:

.. code-block:: python

    from pooch import retrieve


    # Download the file and save it locally. Will check the MD5 checksum of
    # the downloaded file against the given value to make sure it's the right
    # file. You can use other hashes by specifying different algorithm
    # names (sha256, sha1, etc).
    fname = retrieve(
        # URL to one of Pooch's test files
        url="https://github.com/fatiando/pooch/raw/v1.0.0/data/tiny-data.txt",
        known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
    )

The file is stored locally, by default in a ``pooch`` folder in the default
cache location of your operating system (see :func:`pooch.os_cache`).
Running this code a second time will not trigger a download, same as with
:meth:`pooch.Pooch.fetch`.

If you don't know the hash of the file, you can set ``known_hash=None`` to
bypass the check. If this is the case, :func:`~pooch.retrieve` will show a log
message with the SHA256 hash of the downloaded file. **It's highly recommended
that you copy and paste this hash into your code** and use it as the
``known_hash``. That way, the next time your code is run (by you or someone
else) you can guarantee that the exact same file is downloaded. This is a way
to help make sure the results of your code are reproducible.

Function :func:`~pooch.retrieve` has support for all of Pooch's
:ref:`custom downloaders <downloaders>` and
:ref:`post-processing hooks <processors>`. So you can use HTTP and FTP (with or
without authentication), decompress files, unpack archives, and print progress
bars with a bit of configuration.

.. note::

    This function is meant for downloading single files. If you need to
    manage the download and caching of several files, with versioning, use
    :func:`pooch.create` and :class:`pooch.Pooch` instead. See :ref:`usage`.

