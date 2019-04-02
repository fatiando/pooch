.. _usage:

Training your Pooch
===================

The problem
-----------

You develop a Python library called ``plumbus`` for analysing data emitted by
interdimensional portals. You want to distribute sample data so that your users can
easily try out the library by copying and pasting from the docs. You want to have a
``plumbus.datasets`` module that defines functions like ``fetch_c137()`` that will
return the data loaded as a :class:`pandas.DataFrame` for convenient access.


Assumptions
-----------

We'll setup a :class:`~pooch.Pooch` to solve your data distribution needs.
In this example, we'll work with the follow assumptions:

1. Your sample data are in a folder of your Github repository.
2. You use git tags to mark releases of your project in the history.
3. Your project has a variable that defines the version string.
4. The version string contains an indicator that the current commit is not a release
   (like ``'v1.2.3+12.d908jdl'`` or ``'v0.1+dev'``).

Let's say that this is the layout of your repository on Github:

.. code-block:: none

    doc/
        ...
    data/
        README.md
        c137.csv
        cronen.csv
    plumbus/
        __init__.py
        ...
        datasets.py
    setup.py
    ...

The sample data are stored in the ``data`` folder of your repository.

Setup
-----

Pooch can download and cache your data files to the users computer automatically.
This is what the ``plumbus/datasets.py`` file would look like:

.. code:: python

    """
    Load sample data.
    """
    import pandas
    import pooch

    from . import version  # The version string of your project


    GOODBOY = pooch.create(
        # Use the default cache folder for the OS
        path=pooch.os_cache("plumbus"),
        # The remote data is on Github
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        # If this is a development version, get the data from the master branch
        version_dev="master",
        # The registry specifies the files that can be fetched from the local storage
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
    )


    def fetch_c137():
        """
        Load the C-137 sample data as a pandas.DataFrame.
        """
        # The file will be downloaded automatically the first time this is run.
        fname = GOODBOY.fetch("c137.csv")
        data = pandas.read_csv(fname)
        return data


    def fetch_cronen():
        """
        Load the Cronenberg sample data as a pandas.DataFrame.
        """
        fname = GOODBOY.fetch("cronen.csv")
        data = pandas.read_csv(fname)
        return data


When the user calls ``plumbus.datasets.fetch_c137()`` for the first time, the data file
will be downloaded and stored in the local storage. In this case, we're using
:func:`pooch.os_cache` to set the local folder to the default cache location for your
OS. You could also provide any other path if you prefer. See the documentation for
:func:`pooch.create` for more options.


Hashes
------

Pooch uses `SHA256 <https://en.wikipedia.org/wiki/SHA-2>`__ hashes to check if files
are up-to-date or possibly corrupted:

* If a file exists in the local folder, Pooch will check that its hash matches the one
  in the registry. If it doesn't, we'll assume that it needs to be updated.
* If a file needs to be updated or doesn't exist, Pooch will download it from the
  remote source and check the hash. If the hash doesn't match, an exception is raised to
  warn of possible file corruption.

You can generate hashes for your data files using the terminal:

.. code:: bash

    $ openssl sha256 data/c137.csv
    SHA256(data/c137.csv)= baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d

Or using the :func:`pooch.file_hash` function (which is a convenient way of calling
Python's :mod:`hashlib`):

.. code:: python

    import pooch
    print(pooch.file_hash("data/c137.csv"))


Versioning
----------

The files from different version of your project will be kept in separate folders to
make sure they don't conflict with each other. This way, you can safely update data
files while maintaining backward compatibility.
For example, if ``path=".plumbus"`` and ``version="v0.1"``, the data folder will be
``.plumbus/v0.1``.

When your project updates, Pooch will automatically setup a separate folder for the new
data files based on the given version string. The remote URL will also be updated.
Notice that there is a format specifier ``{version}`` in the URL that Pooch substitutes
for you.

Versioning is optional and can be ignored by omitting the ``version`` and
``version_dev`` arguments or setting them to ``None``.


User-defined paths
-------------------

In the above example, the location of the local storage in the users computer is
hard-coded. There is no way for them to change it to something else. To avoid being a
tyrant, you can allow the user to define the ``path`` argument using an environment
variable:

.. code:: python

    GOODBOY = pooch.create(
        # This is still the default in case the environment variable isn't defined
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="master",
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
        # The name of the environment variable that can overwrite the path argument
        env="PLUMBUS_DATA_DIR",
    )

In this case, if the user defines the ``PLUMBUS_DATA_DIR`` environment variable, we'll
use its value instead of ``path``. Pooch will still append the value of ``version`` to
the path, so the value of ``PLUMBUS_DATA_DIR`` should not include a version number.


Subdirectories
--------------

You can have data files in subdirectories of the remote data store. These files will be
saved to the same subdirectories in the local storage folder. Note, however, that the
names of these files in the registry **must use Unix-style separators** (``'/'``) even
on Windows. We will handle the appropriate conversions.


Post-processing hooks
---------------------

Sometimes further post-processing actions need to be taken on downloaded files
(unzipping, conversion to a more efficient format, etc). If these actions are time or
memory consuming, it would be best to do this only once when the file is actually
downloaded and not every time :meth:`pooch.Pooch.fetch` is called.

One way to do this is using *post-processing hooks*. Method :meth:`pooch.Pooch.fetch`
takes a ``hook`` argument that allows us to specify a function that is executed
post-download and before returning the local file path. The hook also lets us overwrite
the file name returned by :meth:`pooch.Pooch.fetch`.

For example, let's say our data file is zipped and we want to store an unzipped copy of
it and read that instead. We can do this with a post-processing hook that unzips the
file and returns the path to the unzipped file instead of the original zip archive:

.. code:: python

    import os
    from zipfile import ZipFile

    def unpack_hook(fname, action, pup):
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
           The instance of Pooch that called the hook function.

        Returns
        -------
        fname : str
           The full path to the unzipped file.
           (Return the same fname is your hook doesn't modify the file).

        """
        # Create a new name for the unzipped file. Appending something to the name is a
        # relatively safe way of making sure there are no clashes with other files in
        # the registry.
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
        # Pass in the hook to unzip the data file
        fname = GOODBOY.fetch("zipped-data-file.zip", hook=unpack_hook)
        # fname is now the path of the unzipped file which can be loaded by pandas
        # directly
        data = pandas.read_csv(fname)
        return data


Alternatively, your zip archive could contain multiple files that you want to unpack. In
this case, the hook can extract all files into a directory and return a list of file
paths instead of a single one:

.. code:: python

    def unpack_multiple_hook(fname, action, pup):
        """
        Post-processing hook to unpack a zip archive and return a list of all files.

        Parameters
        ----------
        fname : str
           Full path of the zipped file in local storage
        action : str
           One of "download" (file doesn't exist and will download),
           "update" (file is outdated and will download), and
           "fetch" (file exists and is updated so no download).
        pup : Pooch
           The instance of Pooch that called the hook function.

        Returns
        -------
        fnames : list of str
           A list of the full path to all files in the unzipped archive.

        """
        unzipped = fname + ".unzipped"
        if action in ("update", "download") or not os.path.exists(unzipped):
            # Make sure that the folder with the unzipped files exists
            if not os.path.exists(unzipped):
                os.makedirs(unzipped)
            with ZipFile(fname, "r") as zip_file:
                # Unpack all files from the archive into our new folder
                zip_file.extractall(path=unzipped)
        # Get a list of all file names (including subdirectories) in our folder of
        # unzipped files.
        fnames = [
            os.path.join(path, fname)
            for path, _, files in os.walk(unzipped)
            for fname in files
        ]
        return fnames


    def fetch_zipped_archive():
        """
        Load all files from a zipped archive.
        """
        # Pass in the hook to unzip the data file
        fnames = GOODBOY.fetch("zipped-archive.zip", hook=unpack_multiple_hook)
        data = [pandas.read_csv(fname) for fname in fnames]
        return data


So you have 1000 data files
---------------------------

If your project has a large number of data files, it can be tedious to list them in a
dictionary. In these cases, it's better to store the file names and hashes in a file and
use :meth:`pooch.Pooch.load_registry` to read them:

.. code:: python

    import os

    GOODBOY = pooch.create(
        # Use the default cache folder for the OS
        path=pooch.os_cache("plumbus"),
        # The remote data is on Github
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        # If this is a development version, get the data from the master branch
        version_dev="master",
        # We'll load it from a file later
        registry=None,
    )
    GOODBOY.load_registry(os.path.join(os.path.dirname(__file__), "registry.txt"))

The ``registry.txt`` file in this case is in the same directory as the ``datasets.py``
module and should be shipped with the package. It's contents are:

.. code-block:: none

    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w

To make sure the registry file is shipped with your package, include the following in
your ``MANIFEST.in`` file:

.. code-block:: none

    include plumbus/registry.txt

And the following entry in the ``setup`` function of your ``setup.py``:

.. code:: python

    setup(
        ...
        package_data={"plumbus": ["registry.txt"]},
        ...
    )


Creating a registry file
------------------------

If you have many data files, creating the registry and keeping it updated can be a
challenge. Function :func:`pooch.make_registry` will create a registry file with all
contents of a directory. For example, we can generate the registry file for our
fictitious project from the command-line:

.. code:: bash

   $ python -c "import pooch; pooch.make_registry('data', 'plumbus/registry.txt')"


Multiple URLs
-------------

You can set a custom download URL for individual files with the ``urls`` argument of
:func:`pooch.create` or :class:`pooch.Pooch`. It should be a dictionary with the file
names as keys and the URLs for downloading the files as values. For example, say we have
a ``citadel.csv`` file that we want to download from
``https://www.some-data-hosting-site.com`` instead:

.. code:: python

    # The basic setup is the same and we must include citadel.csv in the registry.
    GOODBOY = pooch.create(
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="master",
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
            "citadel.csv": "893yprofwjndcwhx9c0ehp3ue9gcwoscjwdfgh923e0hwhcwiyc",
        },
        # Now specify custom URLs for some of the files in the registry.
        urls={
            "citadel.csv": "https://www.some-data-hosting-site.com/files/citadel.csv",
        },
    )

Notice that versioning of custom URLs is not supported (since they are assumed to be
data files independent of your project) and the file name will not be appended
automatically to the URL (in case you want to change the file name in local storage).

Custom URLs can be used along side ``base_url`` or you can omit ``base_url`` entirely by
setting it to an empty string (``base_url=""``). However, doing so requires setting a
custom URL for every file in the registry.

You can also include custom URLs in a registry file by adding the URL for a file to end
of the line (separated by a space):

.. code-block:: none

    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w
    citadel.csv 893yprofwjndcwhx9c0ehp3ue9gcwoscjwdfgh923e0hwhcwiyc https://www.some-data-hosting-site.com/files/citadel.csv

:meth:`pooch.Pooch.load_registry` will automatically populate the ``urls`` attribute.
This way, custom URLs don't need to be set in the code. In fact, the module code doesn't
change at all:

.. code:: python

    # Define the Pooch exactly the same (urls is None by default)
    GOODBOY = pooch.create(
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="master",
        registry=None,
    )
    # If custom URLs are present in the registry file, they will be set automatically
    GOODBOY.load_registry(os.path.join(os.path.dirname(__file__), "registry.txt"))
