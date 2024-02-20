.. _authentication:

Authentication
==============

HTTP authentication
-------------------

Use the :class:`~pooch.HTTPDownloader` class directly to provide login
credentials to HTTP servers that require basic authentication. For example:

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

It's probably not a good idea to hard-code credentials in your code. One way
around this is to ask users to set their own credentials through environment
variables. The download code could look something like so:

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


FTP/SFTP with authentication
----------------------------

Pooch also comes with the :class:`~pooch.FTPDownloader` and
:class:`~pooch.SFTPDownloader` downloaders that can be used
when files are distributed over FTP or SFTP (secure FTP).

.. note::

    To download files over SFTP,
    `paramiko <https://github.com/paramiko/paramiko>`__ needs to be installed.


Sometimes the FTP server doesn't support anonymous FTP and needs authentication
or uses a non-default port.
In these cases, pass in the downloader class explicitly (works with both FTP
and SFTP):

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
