.. _install:

Installing
==========

Which Python?
-------------

You'll need **Python >= 3.6** (see :ref:`python-versions` if you
require support for older versions).

We recommend using the
`Anaconda <https://www.anaconda.com/download>`__
or `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`__
Python distributions to ensure you have all dependencies installed and the
``conda`` package manager available.
Installing Anaconda does not require administrative rights to your computer and
doesn't interfere with any other Python installations in your system.


Installing with conda
---------------------

You can install pooch using the `conda package manager <https://conda.io/>`__
that comes with the Anaconda distribution::

    conda install pooch --channel conda-forge


Installing with pip
-------------------

Alternatively, you can also use the `pip package manager
<https://pypi.org/project/pip/>`__::

    python -m pip install pooch


Installing the latest development version
-----------------------------------------

You can use ``pip`` to install the latest version of the source code from
GitHub::

    python -m pip install --upgrade git+https://github.com/fatiando/pooch


Dependencies
------------

The required dependencies should be installed automatically when you install
Pooch using ``conda`` or ``pip``. Optional dependencies have to be installed
manually.

Required:

* `requests <http://docs.python-requests.org/>`__
* `packaging <https://github.com/pypa/packaging>`__
* `appdirs <https://github.com/ActiveState/appdirs>`__

Optional:

* `tqdm <https://github.com/tqdm/tqdm>`__: Required to print a download
  progress bar (see :ref:`tqdm-progressbar` or :ref:`custom-progressbar`).
* `paramiko <https://github.com/paramiko/paramiko>`__: Required for SFTP
  downloads (see :class:`pooch.SFTPDownloader`).
