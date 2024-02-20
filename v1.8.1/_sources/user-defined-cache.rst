.. _environmentvariable:

User-defined cache location
---------------------------

The location of the local storage cache in the users' computer
is usually hard-coded when we call :func:`pooch.create`.
There is no way for them to change it to something else.

To avoid being a tyrant, you can allow the user to define the cache location
using an environment variable:

.. code:: python

    BRIAN = pooch.create(
        # This is still the default
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="main",
        registry={
            "c137.csv": "19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
            "cronen.csv": "1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
        },
        # The name of an environment variable that can overwrite the path
        env="PLUMBUS_DATA_DIR",
    )

In this case, if the user defines the ``PLUMBUS_DATA_DIR`` environment
variable, Pooch use its value instead of ``path``.

Pooch will still append the value of ``version`` to the path, so the value of
``PLUMBUS_DATA_DIR`` should not include a version number.

