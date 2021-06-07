.. title:: Home

========
|banner|
========

.. |banner| image:: _static/readme-banner.png
    :alt: Pooch Documentation
    :align: middle

.. raw:: html

    <p class="lead centered front-page-callout">
        Just want to download a file without messing with
        <code>requests</code> and <code>urllib</code>?
        <br>
        Want to add sample datasets to your Python package?
        <br>
        <strong>Pooch is here to help!</strong>
    </p>


.. panels::
    :header: text-center text-large

    **New to Pooch?**
    ^^^^^^^^^^^^^^^^^

    Looking to get started using Pooch?

    .. link-button:: about
        :type: ref
        :text: Start here
        :classes: btn-outline-primary btn-block

    ---

    **Experienced user?**
    ^^^^^^^^^^^^^^^^^^^^^

    .. link-button:: api
        :type: ref
        :text: Start here
        :classes: btn-outline-primary

    .. link-button:: api
        :type: ref
        :text: API
        :classes: btn-outline-primary



.. admonition:: Using Pooch for your research?

    Please consider :ref:`citing it <citing>` in your publications.
    Citations help us get credit for all the effort we put into this project.

.. seealso::

    Pooch is a part of the
    `Fatiando a Terra <https://www.fatiando.org/>`_ project.

Contacting Us
-------------

* Most discussion happens `on Github <https://github.com/fatiando/pooch>`__.
  Feel free to `open an issue
  <https://github.com/fatiando/pooch/issues/new>`__ or comment
  on any open issue or pull request.
* We have `chat room on Slack <http://contact.fatiando.org>`__ where you can
  ask questions and leave comments.


Documentation
-------------

.. toctree::
    :maxdepth: 1
    :caption: Getting Started
    :name: gettingstarted

    about.rst
    install.rst
    retrieve.rst
    multiple-files.rst
    sample-data.rst

.. toctree::
    :maxdepth: 1
    :caption: Training your Pooch
    :name: training

    hashes.rst
    user-defined-cache.rst
    registry-files.rst
    multiple-urls.rst
    protocols.rst
    logging.rst
    downloaders.rst
    processors.rst
    authentication.rst
    progressbars.rst
    unpacking.rst
    decompressing.rst

.. toctree::
    :maxdepth: 1
    :caption: Reference
    :name: reference

    api/index.rst
    versions.rst
    compatibility.rst
    changes.rst
    citing.rst

.. toctree::
    :maxdepth: 1
    :caption: Getting help and contributing
    :name: community

    Join the Community <http://contact.fatiando.org>
    Code of Conduct <https://github.com/fatiando/pooch/blob/master/CODE_OF_CONDUCT.md>
    How to Contribute <https://github.com/fatiando/pooch/blob/master/CONTRIBUTING.md>
    Source Code on GitHub <https://github.com/fatiando/pooch>
    Authors <https://github.com/fatiando/pooch/blob/master/AUTHORS.md>
    Fatiando a Terra <https://www.fatiando.org>
