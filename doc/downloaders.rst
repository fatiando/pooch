.. _downloaders:

Downloaders: Customizing the download
=====================================

By default, :meth:`pooch.Pooch.fetch` and :meth:`pooch.retrieve` will detect
the download protocol from the given URL (HTTP, FTP, SFTP, DOI) and use the
appropriate download method.
Sometimes this is not enough: some servers require logins, redirections, or
other non-standard operations.
To get around this, use the ``downloader`` argument of
:meth:`~pooch.Pooch.fetch` and :meth:`~pooch.retrieve`.

Downloaders are Python *callable objects*  (like functions or classes with a
``__call__`` method) and must have the following format:

.. code:: python

    def mydownloader(url, output_file, pooch):
        '''
        Download a file from the given URL to the given local file.

        The function **must** take the following arguments (in order).

        Parameters
        ----------
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
and optionally printing progress bars.
See :ref:`api` for a list of available downloaders.

Common uses of downloaders include:

* Passing :ref:`login credentials <authentication>` to HTTP and FTP servers
* Printing :ref:`progress bars <progressbars>`
* Passing custom keyword arguments to :func:`requests.get` (see
  :ref:`passing-requests-arguments`)


.. _passing-requests-arguments:

Passing arguments to ``requests``
---------------------------------

Any keyword arguments passed to :class:`pooch.HTTPDownloader` (besides
``progressbar`` and ``chunk_size``) are forwarded directly to
:func:`requests.get` when downloading over HTTP or HTTPS. This also works with
:class:`pooch.DOIDownloader`.

This allows you to customize HTTP requests with options such as custom
``headers``, query ``params``, ``timeout``, proxies, or SSL settings. For
example, to pass custom headers and a request timeout:

.. code:: python

    downloader = pooch.HTTPDownloader(
        headers={"User-Agent": "my-package/1.0"},
        timeout=60,
    )
    fname = GOODBOY.fetch("some-data.csv", downloader=downloader)

If a server uses a self-signed certificate or you need to bypass SSL
verification in a restricted environment, you can pass ``verify=False`` (or a
path to a CA bundle):

.. code:: python

    downloader = pooch.HTTPDownloader(verify=False)
    fname = pooch.retrieve(
        url="https://some-data-server.org/some-data.csv",
        known_hash="...",
        downloader=downloader,
    )

.. warning::

    Setting ``verify=False`` disables SSL certificate verification, which
    exposes the connection to man-in-the-middle attacks. Only use this when
    explicitly required for trusted servers.


Creating your own downloaders
-----------------------------

If your use case is not covered by our downloaders, you can implement your own.
:meth:`pooch.Pooch.fetch` and :func:`pooch.retrieve` will accept any *callable
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


Availability checks
-------------------

**Optionally**, downloaders can take a ``check_only`` keyword argument (default
to ``False``) that makes them only check if a given file is available for
download **without** downloading the file.
This makes a downloader compatible with :meth:`pooch.Pooch.is_available`.

In this case, the downloader should return a boolean:

.. code:: python

    def mydownloader(url, output_file, pooch, check_only=False):
        '''
        Download a file from the given URL to the given local file.

        The function **must** take the following arguments (in order).

        Parameters
        ----------
        url : str
            The URL to the file you want to download.
        output_file : str or file-like object
            Path (and file name) to which the file will be downloaded.
        pooch : pooch.Pooch
            The instance of the Pooch class that is calling this function.
        check_only : bool
            If True, will only check if a file exists on the server and
            **without downloading the file**. Will return ``True`` if the file
            exists and ``False`` otherwise.

        Returns
        -------
        None or availability
            If ``check_only==True``, returns a boolean indicating if the file
            is available on the server. Otherwise, returns ``None``.
        '''
        ...

If a downloader does not implement an availability check (i.e., doesn't take
``check_only`` as a keyword argument), then :meth:`pooch.Pooch.is_available`
will raise a ``NotImplementedError``.
