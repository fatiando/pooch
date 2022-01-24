.. _install:

Installing
==========

There are different ways to install Pooch:

.. tabbed:: pip

    Using the `pip <https://pypi.org/project/pip/>`__ package manager:

    .. code:: bash

        python -m pip install pooch

.. tabbed:: conda

    Using the `conda <https://conda.io/>`__ package manager that comes with the
    Anaconda/Miniconda distribution:

    .. code:: bash

        conda install pooch --channel conda-forge

.. tabbed:: Development version

    Using ``pip`` to install the latest **unreleased** version from GitHub
    (**not recommended** in most situations):

    .. code:: bash

        python -m pip install --upgrade git+https://github.com/fatiando/pooch

.. note::

    The commands above should be executed in a terminal. On Windows, use the
    ``cmd.exe`` or the "Anaconda Prompt" app if you're using Anaconda.

Which Python?
-------------

You'll need **Python >= 3.6**. See :ref:`python-versions` if you
require support for older versions.

.. _dependencies:

Dependencies
------------

The required dependencies should be installed automatically when you install
Pooch using ``conda`` or ``pip``. Optional dependencies have to be installed
manually.

Required:

* `appdirs <https://github.com/ActiveState/appdirs>`__
* `packaging <https://github.com/pypa/packaging>`__
* `requests <https://docs.python-requests.org/>`__

Optional:

* `tqdm <https://github.com/tqdm/tqdm>`__: For printing a download
  progress bar. See :ref:`progressbars`.
* `paramiko <https://github.com/paramiko/paramiko>`__: For SFTP downloads. See
  :class:`pooch.SFTPDownloader`.
* `xxhash <https://github.com/ifduyue/python-xxhash>`__: For the faster xxHash
  algorithms. See :ref:`hashes-other`.
