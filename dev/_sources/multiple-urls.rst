.. _multipleurls:

Multiple download URLs
======================

You can set different download URLs for individual files with the ``urls``
argument of :func:`pooch.create`.
It should be a dictionary with the file names as keys and the URLs for
downloading the files as values.

For example, say we have a ``citadel.csv`` file that we want to download from
``https://www.some-data-hosting-site.com`` instead:

.. code:: python

    # The basic setup is the same
    POOCH = pooch.create(
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="main",
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
            # Still include the file in the registry
            "citadel.csv": "893yprofwjndcwhx9c0ehp3ue9gcwoscjwdfgh923e0hwhcwiyc",
        },
        # Now specify custom URLs for some of the files in the registry.
        urls={
            "citadel.csv": "https://www.some-data-hosting-site.com/files/citadel.csv",
        },
    )

When ``POOCH.fetch("citadel.csv")`` is called, the download will by from the
specified URL instead of the ``base_url``.
The file name will not be appended automatically to the URL in case you want to
change the file name in local storage.

.. attention::

    **Versioning of custom URLs is not supported** since they are assumed to be
    data files independent of your project.
    The file will **still be placed in a versioned cache folder**.


.. tip::

    Custom URLs can be used along side ``base_url`` or you can omit
    ``base_url`` entirely by setting it to an empty string (``base_url=""``).
    **Doing so requires setting a custom URL for every file in the registry**.

Usage with registry files
-------------------------

You can also include custom URLs in a :ref:`registry file <registryfiles>` by
adding the URL for a file to end of the line (separated by a space):

.. code-block:: none

    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w
    citadel.csv 893yprofwjndcwhx9c0ehp3ue9gcwoscjwdfgh923e0hwhcwiyc https://www.some-data-hosting-site.com/files/citadel.csv

:meth:`pooch.Pooch.load_registry` will automatically populate the ``urls``
attribute.
This way, custom URLs don't need to be set in the code.
In fact, the module code doesn't change at all:

.. code:: python

    # Define the Pooch exactly the same (urls is None by default)
    POOCH = pooch.create(
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="main",
        registry=None,
    )
    # If custom URLs are present in the registry file, they will be set
    # automatically.
    POOCH.load_registry(os.path.join(os.path.dirname(__file__), "registry.txt"))

