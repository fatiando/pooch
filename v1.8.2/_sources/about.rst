.. _about:

Why use Pooch?
==============

Use cases
---------

.. tab-set::

    .. tab-item:: Just download a file

        **Who**: Scientists/researchers/developers looking to simply download a
        file.

        Pooch makes it easy to download a file (one function call).
        On top of that, it also comes with some bonus features:

        * Download and cache your data files locally (so it's only downloaded
          once).
        * Make sure everyone running the code has the same version of the data
          files by verifying cryptographic hashes.
        * Multiple download protocols HTTP/FTP/SFTP and basic authentication.
        * Download from Digital Object Identifiers (DOIs) issued by repositories
          like figshare and Zenodo.
        * Built-in utilities to unzip/decompress files upon download

        **Start here:** :ref:`retrieve`

    .. tab-item::  Manage sample data for a Python program

        **Who**: Package developers wanting to include sample data for use in
        tutorials and tests.

        Pooch was designed for this! It offers:

        * Pure Python and :ref:`minimal dependencies <dependencies>`.
        * Download a file only if necessary.
        * Verification of download integrity through cryptographic hashes.
        * Extensible design: plug in custom download and post-processing functions.
        * Built-in utilities to unzip/decompress files upon download
        * Multiple download protocols HTTP/FTP/SFTP and basic authentication.
        * User control of data cache location through environment variables.

        **Start here:** :ref:`intermediate`

History
-------

Pooch was born out of shared need between the
`Fatiando a Terra <https://www.fatiando.org>`__ libraries and
`MetPy <https://unidata.github.io/MetPy/>`__.
During the
`Scipy Conference 2018 <https://www.youtube.com/playlist?list=PLYx7XA2nY5Gd-tNhm79CNMe_qvi35PgUR>`__
sprints, developers from both projects got together and, realizing the shared
necessity, devised a package that would combine the best of the existing
functionality already present in each project and extend it's capabilities.
