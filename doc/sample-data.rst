.. _intermediate:

Manage a package's sample data
==============================

In this section, we'll use Pooch to manage the download of a Python package's
sample datasets.
The setup will be very similar to what we saw in :ref:`beginner` (please read
that tutorial first).
This time, we'll also use some other features that make our lives a bit easier.

The problem
-----------

In this example, we'll work with the follow assumptions:

* You develop a Python library called ``plumbus`` for analysing data emitted by
  interdimensional portals.
* You want to distribute sample data so that your users can easily try out the
  library by copying and pasting from the documentation.
* You want to have a ``plumbus.datasets`` module that defines functions like
  ``fetch_c137()`` that will return the data loaded as a
  :class:`pandas.DataFrame` for convenient access.
* Your sample data are in a folder of your GitHub repository but you don't want
  to include the data files with your source and wheel distributions because of
  their size.
* You use git tags to mark releases of your project.
* Your project has a variable that defines the version string.
* The version string contains an indicator that the current commit is not a
  release (like ``'v1.2.3+12.d908jdl'`` or ``'v0.1+dev'``).

For now, let's say that this is the layout of your repository on GitHub:

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

.. tip::

    Pooch can handle different use cases as well, like: FTP/SFTP, authenticated
    HTTP, multiple URLs, decompressing and unpacking archives, etc.

    See the tutorials under "Training your Pooch" and the documentation for
    :func:`pooch.create` and :func:`pooch.Pooch` for more options.


Basic setup
-----------

This is what the ``plumbus/datasets.py`` file would look like:

.. code:: python

    """
    Load sample data.
    """
    import pandas
    import pooch

    from . import version  # The version string of your project


    BRIAN = pooch.create(
        # Use the default cache folder for the operating system
        path=pooch.os_cache("plumbus"),
        # The remote data is on Github
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        # If this is a development version, get the data from the "main" branch
        version_dev="main",
        registry={
            "c137.csv": "sha256:19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "sha256:1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
    )


    def fetch_c137():
        """
        Load the C-137 sample data as a pandas.DataFrame.
        """
        # The file will be downloaded automatically the first time this is run
        # returns the file path to the downloaded file. Afterwards, Pooch finds
        # it in the local cache and doesn't repeat the download.
        fname = BRIAN.fetch("c137.csv")
        # The "fetch" method returns the full path to the downloaded data file.
        # All we need to do now is load it with our standard Python tools.
        data = pandas.read_csv(fname)
        return data


    def fetch_cronen():
        """
        Load the Cronenberg sample data as a pandas.DataFrame.
        """
        fname = BRIAN.fetch("cronen.csv")
        data = pandas.read_csv(fname)
        return data


The ``BRIAN`` variable captures the value returned by :func:`pooch.create`,
which is an instance of the :class:`~pooch.Pooch` class. The class contains the
data registry (files, URLs, hashes, etc) and handles downloading files from the
registry using the :meth:`~pooch.Pooch.fetch` method.
When the user calls ``plumbus.datasets.fetch_c137()`` for the first time, the
data file will be downloaded and stored in the local storage.

.. tip::

    We're using :func:`pooch.os_cache` to set the local folder to the default
    cache location for the user's operating system. You could also provide any
    other path if you prefer.


Versioning
----------

The files from different version of your project will be kept in separate
folders to make sure they don't conflict with each other. This way, you can
safely update data files while maintaining backward compatibility. For example,
if ``path=".plumbus"`` and ``version="v0.1"``, the data folder will be
``.plumbus/v0.1``.

When your project updates, Pooch will automatically setup a separate folder for
the new data files based on the given version string. The remote URL will also
be updated. Notice that there is a format specifier ``{version}`` in the URL
that Pooch substitutes for you.

**Versioning is optional** and can be ignored by omitting the ``version`` and
``version_dev`` arguments or setting them to ``None``.


Where to go from here
---------------------

Pooch has more features for handling different download protocols, handling
large registries, downloading from multiple sources, and more. Check out the
tutorials under "Training your Pooch" for more information.

You can also customize the download itself (adding authentication, progress
bars, etc) and apply post-download steps (unzipping an archive, decompressing a
file, etc) through its :ref:`downloaders` and :ref:`processors`.