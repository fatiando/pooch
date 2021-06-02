.. _registryfiles:

Registry files
==============

Usage
-----

If your project has a large number of data files, it can be tedious to list
them in a dictionary. In these cases, it's better to store the file names and
hashes in a file and use :meth:`pooch.Pooch.load_registry` to read them.

.. code:: python

    import os
    import pkg_resources

    POOCH = pooch.create(
        path=pooch.os_cache("plumbus"),
        base_url="https://github.com/rick/plumbus/raw/{version}/data/",
        version=version,
        version_dev="main",
        # We'll load it from a file later
        registry=None,
    )
    # Get registry file from package_data
    registry_file = pkg_resources.resource_stream("plumbus", "registry.txt")
    # Load this registry file
    POOCH.load_registry(registry_file)

In this case, the ``registry.txt`` file is in the ``plumbus/`` package
directory and should be shipped with the package (see below for instructions).
We use `pkg_resources <https://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access>`__
to access the ``registry.txt``, giving it the name of our Python package.

Registry file format
--------------------

Registry files are light-weight text files that specify a file's name and hash.
In our example, the contents of ``registry.txt`` are:

.. code-block:: none

    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w

A specific hashing algorithm can be enforced, if a checksum for a file is
prefixed with ``alg:``:

.. code-block:: none

    c137.csv sha1:e32b18dab23935bc091c353b308f724f18edcb5e
    cronen.csv md5:b53c08d3570b82665784cedde591a8b0

From Pooch v1.2.0 the registry file can also contain line comments, prepended
with a ``#``:

.. code-block:: none

    # C-137 sample data
    c137.csv 19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc
    # Cronenberg sample data
    cronen.csv 1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w

.. attention::

    Make sure you set the Pooch version in your ``setup.py`` to >=1.2.0 when
    using comments as earlier versions cannot handle them:
    ``install_requires = [..., "pooch>=1.2.0", ...]``


Packaging registry files
------------------------

To make sure the registry file is shipped with your package, include the
following in your ``MANIFEST.in`` file:

.. code-block:: none

    include plumbus/registry.txt

And the following entry in the ``setup`` function of your ``setup.py`` file:

.. code:: python

    setup(
        ...
        package_data={"plumbus": ["registry.txt"]},
        ...
    )


Creating a registry file
------------------------

If you have many data files, creating the registry and keeping it updated can
be a challenge. Function :func:`pooch.make_registry` will create a registry
file with all contents of a directory. For example, we can generate the
registry file for our fictitious project from the command-line:

.. code:: bash

   $ python -c "import pooch; pooch.make_registry('data', 'plumbus/registry.txt')"

