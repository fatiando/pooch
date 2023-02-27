.. _unpacking:

Unpacking archives
==================

Let's say our data file is actually a zip (or tar) archive with a collection of
files.
We may want to store an unpacked version of the archive or extract just a
single file from it.
We can do both operations with the :class:`pooch.Unzip` and
:class:`pooch.Untar` processors.

For example, to extract a single file from a zip archive:

.. code:: python

    from pooch import Unzip


    def fetch_zipped_file():
        """
        Load a large zipped sample data as a pandas.DataFrame.
        """
        # Extract the file "actual-data-file.txt" from the archive
        unpack = Unzip(members=["actual-data-file.txt"])
        # Pass in the processor to unzip the data file
        fnames = GOODBOY.fetch("zipped-data-file.zip", processor=unpack)
        # Returns the paths of all extract members (in our case, only one)
        fname = fnames[0]
        # fname is now the path of the unzipped file ("actual-data-file.txt")
        # which can be loaded by pandas directly
        data = pandas.read_csv(fname)
        return data

By default, the :class:`~pooch.Unzip` processor (and similarly the
:class:`~pooch.Untar` processor) will create a new folder in the same location
as the downloaded archive file, and give it the same name as the archive file
with the suffix ``.unzip`` (or ``.untar``) appended.

If you want to change the location of the unpacked files, you can provide a
parameter ``extract_dir`` to the processor to tell it where you want to unpack
the files:

.. code:: python

    from pooch import Untar


    def fetch_and_unpack_tar_file():
        """
        Unpack a file from a tar archive to a custom subdirectory in the cache.
        """
        # Extract a single file from the archive, to a specific location
        unpack_to_custom_dir = Untar(members=["actual-data-file.txt"],
                                     extract_dir="custom_folder")
        # Pass in the processor to untar the data file
        fnames = GOODBOY.fetch("tarred-data-file.tar.gz", processor=unpack)
        # Returns the paths of all extract members (in our case, only one)
        fname = fnames[0]
        return fname


To extract all files into a folder and return the path to each file, omit the
``members`` parameter:

.. code:: python

    def fetch_zipped_archive():
        """
        Load all files from a zipped archive.
        """
        fnames = GOODBOY.fetch("zipped-archive.zip", processor=Unzip())
        return fnames

Use :class:`pooch.Untar` to do the exact same for tar archives (with optional
compression).
