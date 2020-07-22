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

Pooch can download and cache your data files to the users' computer automatically.
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

Pooch uses `SHA256 <https://en.wikipedia.org/wiki/SHA-2>`__ hashes by default to check
if files are up-to-date or possibly corrupted:

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

Alternative hashing algorithms supported by :mod:`hashlib` can be used if necessary:

.. code:: python

    import pooch
    print(pooch.file_hash("data/c137.csv", alg="sha512"))


Bypassing the hash check
------------------------

Sometimes we might not know the hash of the file or it could change on the server
periodically. In these cases, we need a way of bypassing the hash check.
One way of doing that is with Python's ``unittest.mock`` module. It defines the object
``unittest.mock.ANY`` which passes all equality tests made against it. To bypass the
check, we can set the hash value to ``unittest.mock.ANY`` when specifying the
``registry`` argument for :func:`pooch.create`.

In this example, we want to use Pooch to download a list of weather stations around
Australia. The file with the stations is in an FTP server and we want to store it locally
in separate folders for each day that the code is run. The problem is that the
``stations.zip`` file is updated on the server instead of creating a new one, so the
hash check would fail. This is how you can solve this problem:


.. code:: python

    import datetime
    import unittest.mock
    import pooch

    # Get the current data to store the files in separate folders
    CURRENT_DATE = datetime.datetime.now().date()

    GOODBOY = pooch.create(
        path=pooch.os_cache("bom_daily_stations") / CURRENT_DATE,
        base_url="ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/",
        # Use ANY for the hash value to ignore the checks
        registry={
            "stations.zip": unittest.mock.ANY,
        },
    )

Because hash check is always ``True``, Pooch will only download the file once. When running
again at a different date, the file will be downloaded again because the local cache folder
changed and the file is no longer present in it. If you omit ``CURRENT_DATE`` from the cache
path, then Pooch will only fetch the files once, unless they are deleted from the cache.

.. note::

    If run over a period of time, your cache directory will increase in size, as the
    files are stored in daily subdirectories.


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

In the above example, the location of the local storage in the users' computer is
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


.. _processors:

Post-processing hooks
---------------------

Sometimes further post-processing actions need to be taken on downloaded files
(unzipping, conversion to a more efficient format, etc). If these actions are time or
memory consuming, it would be best to do this only once when the file is actually
downloaded and not every time :meth:`pooch.Pooch.fetch` is called.

One way to do this is using *post-processing hooks*. Method :meth:`pooch.Pooch.fetch`
takes a ``processor`` argument that allows us to specify a function that is executed
post-download and before returning the local file path. The processor also lets us
overwrite the file name returned by :meth:`pooch.Pooch.fetch`.

See the :ref:`api` for a list of all available post-processing hooks.

For example, let's say our data file is zipped and we want to store an unzipped copy of
it and read that instead. We can do this with a post-processing hook that unzips the
file and returns the path to the unzipped file instead of the original zip archive:

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
           The full path to the unzipped file.
           (Return the same fname is your processor doesn't modify the file).

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
        # Pass in the processor to unzip the data file
        fname = GOODBOY.fetch("zipped-data-file.zip", processor=unpack)
        # fname is now the path of the unzipped file which can be loaded by pandas
        # directly
        data = pandas.read_csv(fname)
        return data

Fortunately, you don't have to implement your own unzip processor. Pooch provides the
:class:`pooch.Unzip` processor for exactly this use case. The above example using the
Pooch processor would look like:

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
        # fname is now the path of the unzipped file ("actual-data-file.txt") which can
        # be loaded by pandas directly
        data = pandas.read_csv(fname)
        return data

Alternatively, your zip archive could contain multiple files that you want to unpack. In
this case, the default behavior of :class:`pooch.Unzip` is to extract all files into a
directory and return a list of file paths instead of a single one:

.. code:: python

    def fetch_zipped_archive():
        """
        Load all files from a zipped archive.
        """
        # Pass in the processor to unzip the data file
        fnames = GOODBOY.fetch("zipped-archive.zip", processor=Unzip())
        data = [pandas.read_csv(fname) for fname in fnames]
        return data

If you have a compressed file that is not an archive (zip or tar), you can use
:class:`pooch.Decompress` to decompress it after download. For example, large binary
files can be compressed with ``gzip`` to reduce download times but will need to be
decompressed before loading, which can be slow. You can trade storage space for speed by
keeping a decompressed copy of the file:

.. code:: python

    from pooch import Decompress

    def fetch_compressed_file():
        """
        Load a large binary file that has been gzip compressed.
        """
        # Pass in the processor to decompress the file on download
        fname = GOODBOY.fetch("large-binary-file.npy.gz", processor=Decompress())
        # The file returned is the decompressed version which can be loaded by numpy
        data = numpy.load(fname)
        return data


.. _downloaders:

Downloaders and authentication
------------------------------

By default, :meth:`pooch.Pooch.fetch` will download files over HTTP without
authentication. Sometimes this is not enough: some servers require logins, some are FTP
instead of HTTP. To get around this, you can pass a ``downloader`` to
:meth:`~pooch.Pooch.fetch`.

Pooch provides :class:`~pooch.HTTPDownloader` class (which is used by default) that can
be used to provide login credentials to HTTP servers that require authentication. For
example:

.. code:: python

    from pooch import HTTPDownloader


    def fetch_protected_data():
        """
        Fetch a file from a server that requires authentication
        """
        # Let the downloader know the login credentials
        download_auth = HTTPDownloader(auth=("my_username", "my_password"))
        fname = GOODBOY.fetch("some-data.csv", downloader=download_auth)
        data = pandas.read_csv(fname)
        return data

It's probably not a good idea to hard-code credentials in your code. One way around this
is to ask users to set their own credentials through environment variables. The download
code could look something like this:


.. code:: python

    import os


    def fetch_protected_data():
        """
        Fetch a file from a server that requires authentication
        """
        # Get the credentials from the user's environment
        username = os.environ.get("SOMESITE_USERNAME")
        password = os.environ.get("SOMESITE_PASSWORD")
        # Let the downloader know the login credentials
        download_auth = HTTPDownloader(auth=(username, password))
        fname = GOODBOY.fetch("some-data.csv", downloader=download_auth)
        data = pandas.read_csv(fname)
        return data


FTP/SFTP with or without authentication
---------------------------------------

Pooch also comes with the :class:`~pooch.FTPDownloader` and 
:class:`~pooch.SFTPDownloader` classes that can be used
when files are distributed over FTP or SFTP (secure FTP). 
By default, :meth:`pooch.Pooch.fetch` will automatically detect 
if the download URL is HTTP(S), FTP or SFTP and use the
appropriate downloader:

.. code:: python

    GOODBOY = pooch.create(
        path=pooch.os_cache("plumbus"),
        # Use an FTP server instead of HTTP. The rest is all the same.
        base_url="ftp://my-data-server.org/{version}/",
        version=version,
        version_dev="master",
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
    )


    def fetch_c137():
        """
        Load the C-137 sample data as a pandas.DataFrame (over FTP this time).
        """
        fname = GOODBOY.fetch("c137.csv")
        data = pandas.read_csv(fname)
        return data


However, sometimes the FTP server doesn't support anonymous FTP and needs
authentication. In these cases, pass in an :class:`~pooch.FTPDownloader`
explicitly to :meth:`pooch.Pooch.fetch`:

.. code:: python

    import os


    def fetch_c137():
        """
        Load the C-137 sample data as a pandas.DataFrame (over FTP this time).
        """
        username = os.environ.get("MYDATASERVER_USERNAME")
        password = os.environ.get("MYDATASERVER_PASSWORD")
        download_ftp = pooch.FTPDownloader(username=username, password=password)
        fname = GOODBOY.fetch("c137.csv", downloader=download_ftp)
        data = pandas.read_csv(fname)
        return data


To download files hosted on SFTP servers, the package `paramiko <https://github.com/paramiko/paramiko>`__ needs to be 
installed. The usage of SFTP is identical to the example given above for the 
authenticated :class:`~pooch.FTPDownloader` where :class:`~pooch.SFTPDownloader`
is used instead. 


Custom downloaders
------------------

If your use case is not covered by our downloaders, you can implement your own. See
:meth:`pooch.Pooch.fetch` for the required format of downloaders. As an example,
consider the case in which the login credentials need to be provided to a site that is
redirected from the original download URL in the :class:`~pooch.Pooch` registry:

.. code:: python

    import requests


    def redirect_downloader(url, output_file, pooch):
        """
        Download after following a redirection.
        """
        # Get the credentials from the user's environment
        username = os.environ.get("SOMESITE_USERNAME")
        password = os.environ.get("SOMESITE_PASSWORD")
        # Make a request that will redirect to the login page
        login = requests.get(url)
        # Provide the credentials and download from the new URL
        download = HTTPDownloader(auth=(username, password))
        download(login.url, output_file, mypooch)


    def fetch_protected_data():
        """
        Fetch a file from a server that requires authentication
        """
        fname = GOODBOY.fetch("some-data.csv", downloader=redirect_downloader)
        data = pandas.read_csv(fname)
        return data


Printing a download progress bar
--------------------------------

The :class:`~pooch.HTTPDownloader` can use `tqdm <https://github.com/tqdm/tqdm>`__ to
print a download progress bar. This is turned off by default but can be enabled using:

.. code:: python

    from pooch import HTTPDownloader


    def fetch_large_data():
        """
        Fetch a large file from a server and print a progress bar.
        """
        download = HTTPDownloader(progressbar=True)
        fname = GOODBOY.fetch("large-data-file.h5", downloader=download)
        data = h5py.File(fname, "r")
        return data

The resulting progress bar will be printed to stderr and should look something like
this:

.. code::

    100%|█████████████████████████████████████████| 336/336 [...]

.. note::

    ``tqdm`` is not installed by default with Pooch. You will have to install it
    separately in order to use this feature.


Adjusting the logging level
---------------------------

Pooch will log events like downloading a new file, updating an existing one, or
unpacking an archive by printing to the terminal. You can change how verbose these
events are by getting the event logger from pooch and changing the logging level:

.. code:: python

    logger = pooch.get_logger()
    logger.setLevel("WARNING")

Most of the events from Pooch are logged at the info level; this code says that you only
care about warnings or errors, like inability to create the data cache. The event logger
is a :class:`logging.Logger` object, so you can use that class's methods to handle
logging events in more sophisticated ways if you wish.

So you have 1000 data files
---------------------------

If your project has a large number of data files, it can be tedious to list them in a
dictionary. In these cases, it's better to store the file names and hashes in a file and
use :meth:`pooch.Pooch.load_registry` to read them:

.. code:: python

    import os
    import pkg_resources

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
    # Get registry file from package_data
    registry_file = pkg_resources.resource_stream("plumbus", "registry.txt")
    # Load this registry file
    GOODBOY.load_registry(registry_file)

In this case, the ``registry.txt`` file is in the ``plumbus/`` package directory and should be
shipped with the package (see below for instructions).
We use `pkg_resources <https://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access>`__
to access the ``registry.txt``, giving it the name of our Python package.

The contents of ``registry.txt`` are:

.. code-block:: none

    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w

A specific hashing algorithm can be enforced, if a checksum for a file is
prefixed with ``alg:``, e.g.

.. code-block:: none

    c137.csv sha1:e32b18dab23935bc091c353b308f724f18edcb5e
    cronen.csv md5:b53c08d3570b82665784cedde591a8b0

From version 1.2 the registry file can also contain line comments, prepended with a ``#``, e.g.:

.. code-block:: none

    # C-137 sample data
    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    # Cronenberg sample data
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w

.. note::

    Make sure you set the pooch version in your ``setup.py`` to version 1.2 or
    later when using comments as earlier versions cannot handle them:
     ``install_requires = [..., "pooch>=1.2", ...]``


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


Create registry file from remote files
--------------------------------------

If you want to create a registry file for a large number of data files that are
available for download but you don't have their hashes or any local copies, 
you must download them first. Manually downloading each file
can be tedious. However, we can automate the process using
:func:`pooch.retrieve`. Below, we'll explore two different scenarios.

If the data files share the same base url, we can use :func:`pooch.retrieve`
to download them and then use :func:`pooch.make_registry` to create the
registry:

.. code:: python

    import os

    # Names of the data files
    filenames = ["c137.csv", "cronen.csv", "citadel.csv"]

    # Base url from which the data files can be downloaded from
    base_url = "https://www.some-data-hosting-site.com/files/"

    # Create a new directory where all files will be downloaded
    directory = "data_files"
    os.makedirs(directory)

    # Download each data file to data_files
    for fname in filenames:
        path = pooch.retrieve(
            url=base_url + fname, known_hash=None, fname=fname, path=directory
        )

    # Create the registry file from the downloaded data files
    pooch.make_registry("data_files", "registry.txt")

If each data file has its own url, the registry file can be manually created
after downloading each data file through :func:`pooch.retrieve`:

.. code:: python

    import os

    # Names and urls of the data files. The file names are used for naming the 
    # downloaded files. These are the names that will be included in the registry.
    fnames_and_urls = {
        "c137.csv": "https://www.some-data-hosting-site.com/c137/data.csv",
        "cronen.csv": "https://www.some-data-hosting-site.com/cronen/data.csv",
        "citadel.csv": "https://www.some-data-hosting-site.com/citadel/data.csv",
    }

    # Create a new directory where all files will be downloaded
    directory = "data_files"
    os.makedirs(directory)

    # Create a new registry file
    with open("registry.txt", "w") as registry:
        for fname, url in fnames_and_urls.items():
            # Download each data file to the specified directory
            path = pooch.retrieve(
                url=url, known_hash=None, fname=fname, path=directory
            )
            # Add the name, hash, and url of the file to the new registry file
            registry.write(
                "{} {} {}\n".format(fname, pooch.file_hash(path), url)
            )
            
.. warning::
    
    Notice that there are **no checks for download integrity** (since we don't know the
    file hashes before hand). Only do this for trusted data sources and over a secure 
    connection. If you have access to file hashes/checksums, **we highly recommend
    using them** to set the ``known_hash`` argument. 
