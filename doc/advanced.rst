.. _advanced:

Advanced tricks
===============

These are more advanced things that can be done for specific use cases. **Most
projects will not require these**.


Adjusting the logging level
---------------------------

Pooch will log events like downloading a new file, updating an existing one, or
unpacking an archive by printing to the terminal. You can change how verbose
these events are by getting the event logger from pooch and changing the
logging level:

.. code:: python

    logger = pooch.get_logger()
    logger.setLevel("WARNING")

Most of the events from Pooch are logged at the info level; this code says that
you only care about warnings or errors, like inability to create the data
cache. The event logger is a :class:`logging.Logger` object, so you can use
that class's methods to handle logging events in more sophisticated ways if you
wish.


Bypassing the hash check
------------------------

Sometimes we might not know the hash of the file or it could change on the
server periodically. In these cases, we need a way of bypassing the hash check.
One way of doing that is with Python's ``unittest.mock`` module. It defines the
object ``unittest.mock.ANY`` which passes all equality tests made against it.
To bypass the check, we can set the hash value to ``unittest.mock.ANY`` when
specifying the ``registry`` argument for :func:`pooch.create`.

In this example, we want to use Pooch to download a list of weather stations
around Australia. The file with the stations is in an FTP server and we want to
store it locally in separate folders for each day that the code is run. The
problem is that the ``stations.zip`` file is updated on the server instead of
creating a new one, so the hash check would fail. This is how you can solve
this problem:

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

Because hash check is always ``True``, Pooch will only download the file once.
When running again at a different date, the file will be downloaded again
because the local cache folder changed and the file is no longer present in it.
If you omit ``CURRENT_DATE`` from the cache path, then Pooch will only fetch
the files once, unless they are deleted from the cache.

.. note::

    If this script is run over a period of time, your cache directory will
    increase in size, as the files are stored in daily subdirectories.


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
                f"{fname} {pooch.file_hash(path)} {url}\n"
            )

.. warning::

    Notice that there are **no checks for download integrity** (since we don't
    know the file hashes before hand). Only do this for trusted data sources
    and over a secure connection. If you have access to file hashes/checksums,
    **we highly recommend using them** to set the ``known_hash`` argument.
