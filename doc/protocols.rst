.. _protocols:

Download protocols
==================

Pooch supports the HTTP, FTP, and SFTP protocols by default.
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
        fname = POOCH.fetch("c137.csv")
        data = pandas.read_csv(fname)
        return data

You can even specify custom functions for the download or login credentials for
**authentication**. See :ref:`downloaders` for more information.
