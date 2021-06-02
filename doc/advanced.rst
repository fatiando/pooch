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


Retry failed downloads
----------------------

When downloading data repeatedly, like in continuous integration, failures can
occur due to sporadic network outages or other factors outside of our control.
In these cases, it can be frustrating to have entire jobs fail because a single
download was not successful.

Pooch allows you to specify a number of times to retry the download in case of
failure by setting ``retry_if_failed`` in :func:`pooch.create`. This setting
will be valid for all downloads attempted with :meth:`pooch.Pooch.fetch`. The
download can fail because the file hash doesn't match the known hash (due to a
partial download, for example) or because of network errors coming from
:mod:`requests`. Other errors (file system permission errors, etc) will still
result in a failed download.

.. note::

    Requires Pooch >= 1.3.0.


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
