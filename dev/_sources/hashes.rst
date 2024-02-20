.. _hashes:

Hashes: Calculating and bypassing
=================================

Pooch uses hashes to check if files are up-to-date or possibly
corrupted:

* If a file exists in the local folder, Pooch will check that its hash matches
  the one in the registry. If it doesn't, we'll assume that it needs to be
  updated.
* If a file needs to be updated or doesn't exist, Pooch will download it from
  the remote source and check the hash. If the hash doesn't match, an exception
  is raised to warn of possible file corruption.
* Cryptographic hashes may be used where users wish to ensure the security of
  their download.

Calculating hashes
------------------

You can generate hashes for your data files using ``openssl`` in the terminal:

.. code:: bash

    $ openssl sha256 data/c137.csv
    SHA256(data/c137.csv)= baee0894dba14b12085eacb204284b97e362f4f3e5a5807693cc90ef415c1b2d

Or using the :func:`pooch.file_hash` function (which is a convenient way of
calling Python's :mod:`hashlib`):

.. code:: python

    import pooch
    print(pooch.file_hash("data/c137.csv"))


Specifying the hash algorithm
-----------------------------

By default, Pooch uses `SHA256 <https://en.wikipedia.org/wiki/SHA-2>`__
hashes.
Other hash methods that are available in :mod:`hashlib` can also be used:

.. code:: python

    import pooch
    print(pooch.file_hash("data/c137.csv", alg="sha512"))

In this case, you can specify the hash algorithm in the **registry** by
prepending it to the hash, for example ``"md5:0hljc7298ndo2"`` or
``"sha512:803o3uh2pecb2p3829d1bwouh9d"``.
Pooch will understand this and use the appropriate method.


Bypassing the hash check
------------------------

Sometimes we might not know the hash of the file or it could change on the
server periodically.
To bypass the check, we can set the hash value to ``None`` when specifying the
``registry`` argument for :func:`pooch.create`
(or the ``known_hash`` in :func:`pooch.retrieve`).

In this example, we want to use Pooch to download a list of weather stations
around Australia:

* The file with the stations is in an FTP server and we want to store it
  locally in separate folders for each day that the code is run.
* The problem is that the ``stations.zip`` file is updated on the server
  instead of creating a new one, so the hash check would fail.

This is how you can solve this problem:

.. code:: python

    import datetime
    import pooch

    # Get the current data to store the files in separate folders
    CURRENT_DATE = datetime.datetime.now().date()

    GOODBOY = pooch.create(
        path=pooch.os_cache("bom_daily_stations") / CURRENT_DATE,
        base_url="ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/",
        registry={
            "stations.zip": None,
        },
    )

When running this same code again at a different date, the file will be
downloaded again because the local cache folder changed and the file is no
longer present in it.
If you omit ``CURRENT_DATE`` from the cache path, then Pooch will only fetch
the files once, unless they are deleted from the cache.

.. attention::

    If this script is run over a period of time, your cache directory will
    increase in size, as the files are stored in daily subdirectories.


.. _hashes-other:

Other supported hashes
----------------------

Beyond hashing algorithms supported by ``hashlib``, Pooch supports algorithms
provided by the `xxhash package <https://github.com/ifduyue/python-xxhash>`__.
If the ``xxhash`` package is available, users may specify to use one of
the algorithms provided by the package.

.. code:: bash

    $ xxh128sum data/store.zip
    6a71973c93eac6c8839ce751ce10ae48  data/store.zip
    $ # ^^^^^^^^^^^^^^^^^^^ The hash  ^^^^^^^^^^^^^^ The filename

.. code:: python

    import datetime
    import pooch

    # Get the current data to store the files in separate folders
    CURRENT_DATE = datetime.datetime.now().date()

    GOODBOY = pooch.create(
        [...],
        registry={
            "store.zip": "xxh128:6a71973c93eac6c8839ce751ce10ae48",
        },
    )
