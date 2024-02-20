.. _intermediate:

Manage a package's sample data
==============================

In this section, we'll use Pooch to manage the download of a Python package's
sample datasets.

.. note::

    The setup will be very similar to what we saw in :ref:`beginner`.
    It may be helpful to read that first.

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

.. seealso::

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


Disable file updates for testing
--------------------------------

Sometimes we can forget to update the hash of a file in the registry when we
change one of the existing data files.
If this happens in a pull request or any branch that is not the default, Pooch
will detect that there is a mismatch and will update the local file by
re-downloading (usually from the default development branch).
If your tests don't check the file contents exactly (which is usually not
practical), you can have tests that pass on development or continuous
integration and then fail once a pull request is merged.

In these cases, it is better to temporarily disallow file updates so that Pooch
raises an error when the hash doesn't match (indicating that you forgot to
update it).
To do so, use the ``allow_updates`` argument in :func:`pooch.create`.
Setting this to ``False`` will mean that a hash mismatch between local file and
the registry always results in an error.

.. tip::

    We **do not recommend setting this permanenetly to** ``False``. Instead,
    set it to the name of an environment variable that activates this
    behaviour, like ``pooch.create(...,
    allow_updates="MYPROJECT_ALLOW_UPDATES")``.
    Then you can set ``MYPROJECT_ALLOW_UPDATES=false`` on continuous
    integration or when running your tests locally.

.. note::

    Requires Pooch >= 1.6.0.


Where to go from here
---------------------

Pooch has more features for handling different download protocols, handling
large registries, downloading from multiple sources, and more. Check out the
tutorials under "Training your Pooch" for more information.

Most users will also benefit from reading at least:

* :ref:`environmentvariable`
* :ref:`hashes`
* :ref:`registryfiles`
