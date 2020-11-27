.. _processors:

Processors
==========

Post-download actions sometimes need to be taken on downloaded files
(unzipping, conversion to a more efficient format, etc). If these actions are
time or memory consuming, it might be worth doing them only once after the file
is downloaded. This is a way of trading disk space for computation time.
:meth:`pooch.Pooch.fetch` and :func:`pooch.retrieve` accept the ``processor``
argument to handle these situations.

Processors are Python *callable objects*  (like functions or classes with a
``__call__`` method) that are executed after a file is downloaded to perform
these actions. They must have the following format:

.. code:: python

    def myprocessor(fname, action, pooch):
        '''
        Processes the downloaded file and returns a new file name.

        The function **must** take as arguments (in order):

        fname : str
            The full path of the file in the local data storage
        action : str
            Either: "download" (file doesn't exist and will be downloaded),
            "update" (file is outdated and will be downloaded), or "fetch"
            (file exists and is updated so no download is necessary).
        pooch : pooch.Pooch
            The instance of the Pooch class that is calling this function.

        The return value can be anything but is usually a full path to a file
        (or list of files). This is what will be returned by Pooch.fetch and
        pooch.retrieve in place of the original file path.
        '''
        ...
        return full_path

The processor is executed after a file downloaded attempted (whether the
download actually happens or not) and before returning the path to the
downloaded file. The processor lets us intercept the returned path, perform
actions, and possibly return a different path.

Pooch provides built-in processors for common tasks, like decompressing files
and unpacking tar and zip archives. See the :ref:`api` for a full list.


Unpacking archives
------------------

Let's say our data file is actually a zip (or tar) archive with a collection of files.
We may want to store an unpacked version of the archive or extract just a
single file from it. We can do both operations with the :class:`pooch.Unzip`
and :class:`pooch.Untar` processors.

For example, to extract a single file from a zip archive:

.. code:: python

    from pooch import Unzip


    def fetch_zipped_file():
        """
        Load a large zipped sample data as a pandas.DataFrame.
        """
        # Extract the file "actual-data-file.txt" from the archive
        unpack =  Unzip(members=["actual-data-file.txt"])
        # Pass in the processor to unzip the data file
        fnames = GOODBOY.fetch("zipped-data-file.zip", processor=unpack)
        # Returns the paths of all extract members (in our case, only one)
        fname = fnames[0]
        # fname is now the path of the unzipped file ("actual-data-file.txt")
        # which can be loaded by pandas directly
        data = pandas.read_csv(fname)
        return data

Or to extract all files into a folder and return the path to each file:

.. code:: python

    def fetch_zipped_archive():
        """
        Load all files from a zipped archive.
        """
        # Pass in the processor to unzip the data file
        fnames = GOODBOY.fetch("zipped-archive.zip", processor=Unzip())
        data = [pandas.read_csv(fname) for fname in fnames]
        return data

Use :class:`pooch.Untar` to do the exact same for tar archives (with optional
compression).


Decompressing
-------------

If you have a compressed file that is not an archive (zip or tar), you can use
:class:`pooch.Decompress` to decompress it after download. For example, large
binary files can be compressed with ``gzip`` to reduce download times but will
need to be decompressed before loading, which can be slow. You can trade
storage space for speed by keeping a decompressed copy of the file:

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
decompressed file name by default. You can change this behaviour by passing a
file name instead:

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

    Passing in ``name`` can cause existing data to be lost! For example, if
    a file already exists with the specified name it will be overwritten with
    the new decompressed file content. **Use this option with caution.**


Custom processors
-----------------

Let's say we want to implement the :class:`pooch.Unzip` processor ourselves to
extract a single file from the archive. We could do that with the following
function:

.. code:: python

    import os
    from zipfile import ZipFile


    def unpack(fname, action, pup):
        """
        Post-processing hook to unzip a file and return the unzipped file name.

        Parameters
        ----------
        fname : str
           Full path of the zipped file in local storage
        action : str
           One of "download" (file doesn't exist and will download),
           "update" (file is outdated and will download), and
           "fetch" (file exists and is updated so no download).
        pup : Pooch
           The instance of Pooch that called the processor function.

        Returns
        -------
        fname : str
           The full path to the unzipped file. (Return the same fname is your
           processor doesn't modify the file).

        """
        # Create a new name for the unzipped file. Appending something to the
        # name is a relatively safe way of making sure there are no clashes
        # with other files in the registry.
        unzipped = fname + ".unzipped"
        # Don't unzip if file already exists and is not being downloaded
        if action in ("update", "download") or not os.path.exists(unzipped):
            with ZipFile(fname, "r") as zip_file:
                # Extract the data file from within the archive
                with zip_file.open("actual-data-file.txt") as data_file:
                    # Save it to our desired file name
                    with open(unzipped, "wb") as output:
                        output.write(data_file.read())
        # Return the path of the unzipped file
        return unzipped


    def fetch_zipped_file():
        """
        Load a large zipped sample data as a pandas.DataFrame.
        """
        # Pass in the processor to unzip the data file
        fname = GOODBOY.fetch("zipped-data-file.zip", processor=unpack)
        # fname is now the path of the unzipped file which can be loaded by
        # pandas directly
        data = pandas.read_csv(fname)
        return data


Similarly, you could build any custom processor function so long as it receives
the ``fname, action, pup`` arguments. Example use cases for this would be:

* Converting data from a download-friendly format (compressed and minimal file
  size) to a more user friendly format (easy to open and fast to load into
  memory).
* Add missing metadata to data from public servers. You might be using public
  data that has known issues (poorly formated entries, missing metadata, etc)
  which can be fixed when the file is downloaded.

The main advantage to using a processor for these actions is that they are
performed only when the file is downloaded. A modified version of the file can
be kept on disk so that loading the file is easier. This is particularly
convenient if the processor task takes a long time to run.
