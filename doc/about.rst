Why use Pooch?
==============

Pooch has two main uses cases:

1. Scientists/researchers/developers looking to simply download a file.
2. Package developers wanting to include sample data for use in tutorials and
   tests.

Pooch makes it easy to :ref:`download a file <retrieve>` with a single function
call:

* Download and cache your data files locally (so it's only downloaded once).
* Make sure everyone running the code has the same version of the data files by
  verifying cryptographic hashes.

For :ref:`package developers <intermediate>`, Pooch offers:

* Pure Python and :ref:`minimal dependencies <dependencies>`.
* Download a file only if necessary (it's not in the data cache or needs to be
  updated).
* Verify download integrity through hashes (also used to check if a file needs
  to be updated).
* Designed to be extended: plug in custom download (FTP, scp, etc) and
  post-processing (unzip, decompress, rename) functions.
* Includes utilities to unzip/decompress the data upon download to save loading
  time.
* Can handle HTTP/FTP/SFT and basic authentication.
* Easily set up an environment variable to overwrite the data cache location.

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
