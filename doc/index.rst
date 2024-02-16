.. title:: Home

.. raw:: html

    <div class="text-center">
    <img src="_static/pooch-logo.svg" class="mx-auto my-4 dark-light" style="width: 100%; max-width: 200px;">
    <h1 class="display-1">Pooch</h1>
    <p class="fs-4">
    <strong>
    A friend to fetch your data files
    </strong>
    </p>
    </div>


.. raw:: html

    <p class="fs-5">
        Just want to download a file without messing with
        <code>requests</code> and <code>urllib</code>?
        Trying to add sample datasets to your Python package?
        <strong>Pooch is here to help!</strong>
    </p>

*Pooch* is a **Python library** that can manage data by **downloading files**
from a server (only when needed) and storing them locally in a data **cache**
(a folder on your computer).

* Pure Python and minimal dependencies.
* Download files over HTTP, FTP, and from data repositories like Zenodo and figshare.
* Built-in post-processors to unzip/decompress the data after download.
* Designed to be extended: create custom downloaders and post-processors.

Are you a **scientist** or researcher? Pooch can help you too!

* Host your data on a repository and download using the DOI.
* Automatically download data using code instead of telling colleagues to do it themselves.
* Make sure everyone running the code has the same version of the data files.

----

.. grid:: 1 2 1 2
    :margin: 5 5 0 0
    :padding: 0 0 0 0
    :gutter: 4

    .. grid-item-card:: :octicon:`info` Getting started
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        New to Pooch? Start here!

        .. button-ref:: about
            :ref-type: ref
            :click-parent:
            :color: primary
            :outline:
            :expand:

    .. grid-item-card:: :octicon:`comment-discussion` Need help?
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        Ask on our community channels.

        .. button-link:: https://www.fatiando.org/contact
            :click-parent:
            :color: primary
            :outline:
            :expand:

            Join the conversation :octicon:`link-external`

    .. grid-item-card:: :octicon:`file-badge` Reference documentation
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        A list of modules and functions.

        .. button-ref:: api
            :ref-type: ref
            :color: primary
            :outline:
            :expand:

    .. grid-item-card:: :octicon:`bookmark` Using Pooch for research?
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        Citations help support our work!

        .. button-ref:: citing
            :ref-type: ref
            :color: primary
            :outline:
            :expand:

----

.. seealso::

    Pooch is a part of the
    `Fatiando a Terra <https://www.fatiando.org/>`_ project.

.. toctree::
    :caption: Getting Started
    :hidden:
    :maxdepth: 1

    about.rst
    install.rst
    retrieve.rst
    multiple-files.rst
    sample-data.rst

.. toctree::
    :caption: Training your Pooch
    :hidden:
    :maxdepth: 1

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
    :caption: Reference
    :hidden:
    :maxdepth: 1

    api/index.rst
    compatibility.rst
    citing.rst
    changes.rst
    versions.rst

.. toctree::
    :caption: Community
    :hidden:

    Join the community <https://www.fatiando.org/contact/>
    Code of Conduct <https://github.com/fatiando/community/blob/main/CODE_OF_CONDUCT.md>
    How to contribute <https://github.com/fatiando/pooch/blob/main/CONTRIBUTING.md>
    Source code on GitHub <https://github.com/fatiando/pooch>
    Authors <https://github.com/fatiando/pooch/blob/main/AUTHORS.md>
    Fatiando a Terra <https://www.fatiando.org>
