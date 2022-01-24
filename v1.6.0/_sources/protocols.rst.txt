.. _protocols:

Download protocols
==================

Pooch supports the HTTP, FTP, and SFTP protocols by default.
It also includes a custom protocol for Digital Object Identifiers (DOI) from
providers like `figshare <https://www.figshare.com>`__ and `Zenodo
<https://www.zenodo.org>`__ (see :ref:`below <doidownloads>`).
It will **automatically detect** the correct protocol from the URL and use the
appropriate download method.

.. note::

    To download files over SFTP,
    `paramiko <https://github.com/paramiko/paramiko>`__ needs to be installed.

For example, if our data were hosted on an FTP server, we could use the
following setup:

.. code:: python

    POOCH = pooch.create(
        path=pooch.os_cache("plumbus"),
        # Use an FTP server instead of HTTP. The rest is all the same.
        base_url="ftp://garage-basement.org/{version}/",
        version=version,
        version_dev="main",
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
    )


    def fetch_c137():
        """
        Load the C-137 sample data as a pandas.DataFrame (over FTP this time).
        """
        fname = POOCH.fetch("c137.csv")
        data = pandas.read_csv(fname)
        return data

You can even specify custom functions for the download or login credentials for
**authentication**. See :ref:`downloaders` for more information.

.. _doidownloads:

Digital Object Identifiers (DOIs)
---------------------------------

Pooch can download files stored in data repositories from the DOI by formatting
the URL as ``doi:{DOI}/{file name}``.
Notice that there are no ``//`` like in HTTP/FTP and you must specify a file
name after the DOI (separated by a ``/``).

.. seealso::

    For a list of supported data repositories, see
    :class:`pooch.DOIDownloader`.

For example, one of our test files (``"tiny-data.txt"``) is stored in the
figshare dataset
doi:`10.6084/m9.figshare.14763051.v1 <https://doi.org/10.6084/m9.figshare.14763051.v1>`__.
We can could use :func:`pooch.retrieve` to download it like so:

.. code-block:: python

    file_path = pooch.retrieve(
        url="doi:10.6084/m9.figshare.14763051.v1/tiny-data.txt",
        known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
    )

We can also make a :class:`pooch.Pooch` with a registry stored entirely on a
figshare dataset:

.. code-block:: python

    POOCH = pooch.create(
        path=pooch.os_cache("plumbus"),
        # Use the figshare DOI
        base_url="doi:10.6084/m9.figshare.14763051.v1/",
        registry={
            "tiny-data.txt": "md5:70e2afd3fd7e336ae478b1e740a5f08e",
            "store.zip": "md5:7008231125631739b64720d1526619ae",
        },
    )


    def fetch_tiny_data():
        """
        Load the tiny data as a numpy array.
        """
        fname = POOCH.fetch("tiny-data.txt")
        data = numpy.loadtxt(fname)
        return data


.. warning::

    A figshare DOI must point to a figshare *dataset*, not a figshare
    *collection*. Collection DOIs have a ``.c.`` in them, e.g.
    ``doi:10.6084/m9.figshare.c.4362224.v1``. Attempting to download files
    from a figshare collection will raise an error.
    See `issue #274 <https://github.com/fatiando/pooch/issues/274>`__ details.
