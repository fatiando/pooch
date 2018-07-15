.. _install:

Installing
==========

Which Python?
-------------

You'll need **Python 3.5 or greater**.

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


Installing with conda
---------------------

You can install garage using the `conda package manager <https://conda.io/>`__ that
comes with the Anaconda distribution::

    conda install garage --channel conda-forge


Installing with pip
-------------------

Alternatively, you can also use the `pip package manager
<https://pypi.org/project/pip/>`__::

    pip install garage


Installing the latest development version
-----------------------------------------

You can use ``pip`` to install the latest source from Github::

    pip install https://github.com/fatiando/garage/archive/master.zip

Alternatively, you can clone the git repository locally and install from there::

    git clone https://github.com/fatiando/garage.git
    cd garage
    pip install .


Testing your install
--------------------

We ship a full test suite with the package.
To run the tests, you'll need to install some extra dependencies first:

* `pytest <https://docs.pytest.org/>`__

After that, you can test your installation by running the following inside a Python
interpreter::

    import garage
    garage.test()
