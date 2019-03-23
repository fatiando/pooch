.. _install:

Installing
==========

Which Python?
-------------

You'll need Python 2.7 or **Python >=3.6 (recommended)**.

.. warning::

   🚨 **Python 2.7 will only be supported until the Fall of 2019.** 🚨

   Relases made after this date will only be compatible with Python 3.

We recommend using the
`Anaconda Python distribution <https://www.anaconda.com/download>`__
to ensure you have all dependencies installed and the ``conda`` package manager
available.
Installing Anaconda does not require administrative rights to your computer and
doesn't interfere with any other Python installations in your system.


Dependencies
------------

* `requests <http://docs.python-requests.org/>`__
* `packaging <https://github.com/pypa/packaging>`__

The following are only required for Python 2.7:

* `pathlib <https://pypi.org/project/pathlib/>`__
* `backports.tempfile <https://pypi.org/project/backports.tempfile/>`__


Installing with conda
---------------------

You can install pooch using the `conda package manager <https://conda.io/>`__ that
comes with the Anaconda distribution::

    conda install pooch --channel conda-forge


Installing with pip
-------------------

Alternatively, you can also use the `pip package manager
<https://pypi.org/project/pip/>`__::

    pip install pooch


Installing the latest development version
-----------------------------------------

You can use ``pip`` to install the latest source from Github::

    pip install https://github.com/fatiando/pooch/archive/master.zip

Alternatively, you can clone the git repository locally and install from there::

    git clone https://github.com/fatiando/pooch.git
    cd pooch
    pip install .


Testing your install
--------------------

We ship a full test suite with the package.
To run the tests, you'll need to install some extra dependencies first:

* `pytest <https://docs.pytest.org/>`__

After that, you can test your installation by running the following inside a Python
interpreter::

    import pooch
    pooch.test()
