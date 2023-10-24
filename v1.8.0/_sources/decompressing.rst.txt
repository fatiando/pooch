.. _decompressing:

Decompressing
=============

If you have a compressed file that is not an archive (zip or tar), you can use
:class:`pooch.Decompress` to decompress it after download.

For example, large binary files can be compressed with ``gzip`` to reduce
download times but will need to be decompressed before loading, which can be
slow.
You can trade storage space for speed by keeping a decompressed copy of the
file:

.. code:: python

    from pooch import Decompress

    def fetch_compressed_file():
        """
        Load a large binary file that has been gzip compressed.
        """
        # Pass in the processor to decompress the file on download
        fname = GOODBOY.fetch("large-binary-file.npy.gz", processor=Decompress())
        # The file returned is the decompressed version which can be loaded by
        # numpy
        data = numpy.load(fname)
        return data

:class:`pooch.Decompress` returns ``"large-binary-file.npy.gz.decomp"`` as the
decompressed file name by default.
You can change this behaviour by passing a file name instead:

.. code:: python

    import os
    from pooch import Decompress

    def fetch_compressed_file():
        """
        Load a large binary file that has been gzip compressed.
        """
        # Pass in the processor to decompress the file on download
        fname = GOODBOY.fetch("large-binary-file.npy.gz",
            processor=Decompress(name="a-different-file-name.npy"),
        )
        # The file returned is now named "a-different-file-name.npy"
        data = numpy.load(fname)
        return data

.. warning::

    Passing in ``name`` can cause existing data to be lost!
    For example, if a file already exists with the specified name it will be
    overwritten with the new decompressed file content.
    **Use this option with caution.**
