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

.. note::

    The commands below should be executed in a terminal. On Windows, use the
    "Anaconda Prompt" app or ``cmd.exe`` if you're not using Anaconda.


Installing
----------

There are different ways to install Pooch:

.. tabbed:: conda

    Using the `conda <https://conda.io/>`__ package manager that comes with the
    Anaconda/Miniconda distribution:

    .. code:: bash

        conda install pooch --channel conda-forge

.. tabbed:: pip

    Using the `pip <https://pypi.org/project/pip/>`__ package manager:

    .. code:: bash

        python -m pip install pooch


.. tabbed:: Development version

    Using ``pip`` to install the latest **unreleased** version from GitHub:

    .. code:: bash

        python -m pip install --upgrade git+https://github.com/fatiando/pooch


.. _dependencies:

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

* `tqdm <https://github.com/tqdm/tqdm>`__: For printing a download
  progress bar. See :ref:`progressbars`.
* `paramiko <https://github.com/paramiko/paramiko>`__: For SFTP downloads. See
  :class:`pooch.SFTPDownloader`.
