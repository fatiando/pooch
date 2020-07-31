.. _downloaders:

Downloaders
===========

By default, :meth:`pooch.Pooch.fetch` and :meth:`pooch.retrieve` will detect
the download protocol from the given URL (HTTP, FTP, or SFTP) and use the
appropriate download method. Sometimes this is not enough: some servers require
logins, redirections, or other non-standard operations. To get around this, you
can pass a ``downloader`` argument to :meth:`~pooch.Pooch.fetch` and
:meth:`~pooch.retrieve`.

Downloaders are Python *callable objects*  (like functions or classes with a
``__call__`` method) and must have the following format:

.. code:: python

    def mydownloader(url, output_file, pooch):
        '''
        Download a file from the given URL to the given local file.

        The function **must** take as arguments (in order):

        url : str
            The URL to the file you want to download.
        output_file : str or file-like object
            Path (and file name) to which the file will be downloaded.
        pooch : pooch.Pooch
            The instance of the Pooch class that is calling this function.

        No return value is required.
        '''
        ...


Pooch provides downloaders for HTTP, FTP, and SFTP that support authentication
and optionally printing progress bars. See :ref:`api` for a list of available
downloaders.


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

However, sometimes the FTP server doesn't support anonymous FTP and needs
authentication or uses a non-default port. In these cases, pass in the
downloader class explicitly (works with both FTP and SFTP):

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

.. note::

    To download files hosted on SFTP servers, the package `paramiko
    <https://github.com/paramiko/paramiko>`__ needs to be installed.


Custom downloaders
------------------

If your use case is not covered by our downloaders, you can implement your own.
:meth:`pooch.Pooch.fetch` and :meth:`pooch.retrive` will accept any *callable
obejct* that has the signature specified above. As an example, consider the
case in which the login credentials need to be provided to a site that is
redirected from the original download URL:

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
