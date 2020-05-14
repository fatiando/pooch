.. _changes:

Changelog
=========

Version 1.1.1
-------------

*Released on: 2020/05/14*

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3826458.svg
    :alt: Digital Object Identifier for the Zenodo archive
    :target: https://doi.org/10.5281/zenodo.3826458

Bug fixes:

* Delay data cache folder creation until the first download is attempted. As
  seen in `recent issues in scikit-image
  <https://github.com/scikit-image/scikit-image/issues/4719>`__, creating the
  data folder in ``pooch.create`` can cause problems since this function is
  called at import time. This means that importing the package in parallel can
  cause race conditions and crashes. To prevent that from happening, delay the
  creation of the cache folder until ``Pooch.fetch`` or ``retrieve`` are
  called.
  (`#173 <https://github.com/fatiando/pooch/pull/173>`__)
* Allow the data folder to already exist when creating it. This is can help
  cope with parallel execution as well.
  (`#171 <https://github.com/fatiando/pooch/pull/171>`__)

Documentation:

* Added scikit-image to list of Pooch users.
  (`#168 <https://github.com/fatiando/pooch/pull/168>`__)
* Fix typo in README and front page contributing section.
  (`#166 <https://github.com/fatiando/pooch/pull/166>`__)

This release contains contributions from:

* Leonardo Uieda
* Egor Panfilov
* Rowan Cockett

Version 1.1.0
-------------

*Released on: 2020/04/13*

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3747184.svg
    :alt: Digital Object Identifier for the Zenodo archive
    :target: https://doi.org/10.5281/zenodo.3747184

New features:

* New function ``pooch.retrieve`` to fetch single files This is much more
  convenient than setting up a ``Pooch`` while retaining the hash checks and
  use of downloaders and processors. It automatically selects a unique file
  name and saves files to a cache folder.
  (`#152 <https://github.com/fatiando/pooch/pull/152>`__)
* Allow to use of different hashing algorithms (other than SHA256). Optionally
  specify the hash as ``alg:hash`` and allow ``pooch.Pooch`` to recognize the
  algorithm when comparing hashes. Setting an algorithsm is optional and
  omiting it defaults to SHA256. This is particularly useful when data are
  coming from external sources and published hashes are already available.
  (`#133 <https://github.com/fatiando/pooch/pull/133>`__)

Documentation:

* Add example for fetching datasets that change on the server, for which the
  hash check would always fail.
  (`#144 <https://github.com/fatiando/pooch/pull/144>`__)
* Fix path examples in docstring of ``pooch.os_cache``. The docstring mentioned
  the data path as examples instead of the cache path.
  (`#140 <https://github.com/fatiando/pooch/pull/140>`__)
* Add example of creating a registry when you don't have the data files locally
  and would have to download them manually. The example uses the
  ``pooch.retrieve`` function to automate the process. The example covers two
  cases: when all remote files share the same base URL and when every file has
  its own URL.
  (`#161 <https://github.com/fatiando/pooch/pull/161>`__)

Maintenance:

* A lot of general refactoring of the internals of Pooch to facilitate
  development of the new ``pooch.retrieve`` function
  (`#159 <https://github.com/fatiando/pooch/pull/159>`__
  `#157 <https://github.com/fatiando/pooch/pull/157>`__
  `#156 <https://github.com/fatiando/pooch/pull/156>`__
  `#151 <https://github.com/fatiando/pooch/pull/151>`__
  `#149 <https://github.com/fatiando/pooch/pull/149>`__)

This release contains contributions from:

* Leonardo Uieda
* Santiago Soler
* Kacper Kowalik
* Lucas Martin-King
* Zac Flamig

Version 1.0.0
-------------

*Released on: 2020/01/28*

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3629329.svg
    :alt: Digital Object Identifier for the Zenodo archive
    :target: https://doi.org/10.5281/zenodo.3629329

This release marks the stabilization of the Pooch API. Further changes to the
1.* line will be fully backwards compatible (meaning that updating Pooch should
not break existing code). If there is great need to make backwards incompatible
changes, we will release a 2.* line. In that case, bug fixes will still be
ported to the 1.* line for a period of time.

Improvements:

* Allow blank lines in registry files. Previously, they would cause an error.
  (`#138 <https://github.com/fatiando/pooch/pull/138>`__)

**Backwards incompatible changes**:

* Using Python's ``logging`` module to instead of ``warnings`` to inform users
  of download, update, and decompression/unpacking actions. This allows
  messages to be logged with different priorities and the user filter out log
  messages or silence Pooch entirely. Introduces the function
  ``pooch.get_logger`` to access the ``logging`` object used by Pooch. **Users
  who relied on Pooch issuing warnings will need to update to capturing logs
  instead.** All other parts of the API remain unchanged.
  (`#115 <https://github.com/fatiando/pooch/pull/115>`__)

This release contains contributions from:

* Daniel Shapero

Version 0.7.2
-------------

*Released on: 2020/01/17*

🚨 **Announcement:** 🚨
We now have a `JOSS paper about Pooch <https://doi.org/10.21105/joss.01943>`__!
Please :ref:`cite it <citing>` when you use Pooch for your research.
(`#116 <https://github.com/fatiando/pooch/pull/116>`__ with reviews in
`#132 <https://github.com/fatiando/pooch/pull/132>`__ and
`#134 <https://github.com/fatiando/pooch/pull/134>`__)

This is minor release which only updates the citation information to
the new JOSS paper. No DOI was issued for this release since there are
no code or documentation changes.

Version 0.7.1
-------------

*Released on: 2020/01/17*

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3611376.svg
    :alt: Digital Object Identifier for the Zenodo archive
    :target: https://doi.org/10.5281/zenodo.3611376

Improvements:

* Better error messages when hashes don't match. Include the file name in the
  exception for a hash mismatch between a downloaded file and the registry.
  Before, we included the name of temporary file, which wasn't very
  informative.
  (`#128 <https://github.com/fatiando/pooch/pull/128>`__)
* Better error message for malformed registry files. When loading a registry
  file, inform the name of the file and include the offending content in the
  error message instead of just the line number.
  (`#129 <https://github.com/fatiando/pooch/pull/129>`__)

Maintenance:

* Change development status flag in ``setup.py`` to "stable" instead of
  "alpha".
  (`#127 <https://github.com/fatiando/pooch/pull/127>`__)

This release was reviewed at the `Journal of Open Source Software
<https://github.com/openjournals/joss-reviews/issues/1943>`__. The code and
software paper contain contributions from:

* Anderson Banihirwe
* Martin Durant
* Mark Harfouche
* Hugo van Kemenade
* John Leeman
* Rémi Rampin
* Daniel Shapero
* Santiago Rubén Soler
* Matthew Turk
* Leonardo Uieda

Version 0.7.0
-------------

*Released on: 2019/11/19*

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3547640.svg
    :alt: Digital Object Identifier for the Zenodo archive
    :target: https://doi.org/10.5281/zenodo.3547640

New features:

* New ``pooch.FTPDownloader`` class for downloading files over FTP. Uses the
  standard library ``ftplib``. The appropriate downloader is automatically
  selected by ``pooch.Pooch.fetch`` based on the URL (for anonymous FTP only),
  so no configuration is required.
  If authentication is required, ``pooch.FTPDownloader`` provides the need
  support. Ported from
  `NCAR/aletheia-data <https://github.com/NCAR/aletheia-data>`__ by the author.
  (`#118 <https://github.com/fatiando/pooch/pull/118>`__)
* Support for file-like objects to ``Pooch.load_registry`` (opened either in
  binary or text mode).
  (`#117 <https://github.com/fatiando/pooch/pull/117>`__)

Maintenance:

* Testing and official support for Python 3.8.
  (`#113 <https://github.com/fatiando/pooch/pull/113>`__)
* 🚨 **Drop support for Python 2.7.** 🚨 Remove conditional dependencies and CI
  jobs.
  (`#100 <https://github.com/fatiando/pooch/pull/100>`__)

Documentation:

* In the tutorial, use ``pkg_resources.resource_stream()`` from setuptools to
  load the ``registry.txt`` file. It's less error-prone than using ``os.path``
  and ``__file__`` and allows the package to work from zip files.
  (`#120 <https://github.com/fatiando/pooch/pull/120>`__)
* Docstrings formatted to 79 characters (instead of 88) for better rendering in
  Jupyter notebooks and IPython. These displays are limited to 80 chars so the
  longer lines made the docstring unreadable.
  (`#123 <https://github.com/fatiando/pooch/pull/123>`__)

This release contains contributions from:

* Anderson Banihirwe
* Hugo van Kemenade
* Remi Rampin
* Leonardo Uieda

Version 0.6.0
-------------

*Released on: 2019/10/22*

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3515031.svg
    :alt: Digital Object Identifier for the Zenodo archive
    :target: https://doi.org/10.5281/zenodo.3515031

🚨 **Pooch v0.6.0 is the last release to support Python 2.7** 🚨

New features:

* Add optional download progress bar to ``pooch.HTTPDownloader``
  (`#97 <https://github.com/fatiando/pooch/pull/97>`__)

Maintenance:

* Warn that 0.6.0 is the last version to support Python 2.7
  (`#108 <https://github.com/fatiando/pooch/pull/108>`__)

Documentation:

* Update contact information to point to our Slack channel
  (`#107 <https://github.com/fatiando/pooch/pull/107>`__)
* Add icepack to list of projects using Pooch
  (`#98 <https://github.com/fatiando/pooch/pull/98>`__)

This release contains contributions from:

* Daniel Shapero
* Leonardo Uieda

Version 0.5.2
-------------

*Released on: 2019/06/24*

Maintenance:

* Add back support for Python 3.5 with continuous integration tests. No code changes
  were needed, only removing the restriction from ``setup.py``.
  (`#93 <https://github.com/fatiando/pooch/pull/93>`__)

This release contains contributions from:

* Leonardo Uieda

Version 0.5.1
-------------

*Released on: 2019/05/21*

Documentation fixes:

* Fix formatting error in ``pooch.Decompress`` docstring.
  (`#81 <https://github.com/fatiando/pooch/pull/81>`__)
* Fix wrong imports in the usage guide for post-processing hooks.
  (`#84 <https://github.com/fatiando/pooch/pull/84>`__)
* Add section to the usage guide explaining when to use ``pooch.Decompress``.
  (`#85 <https://github.com/fatiando/pooch/pull/85>`__)

This release contains contributions from:

* Santiago Soler
* Leonardo Uieda

Version 0.5.0
-------------

*Released on: 2019/05/20*

New features:

* New processor ``pooch.Decompress`` saves a decompressed version of the downloaded
  file. Supports gzip, lzma/xz, and bzip2 compression. **Note**: Under Python 2.7, lzma
  and bzip2 require the ``backports.lzma`` and ``bz2file`` packages as well. These are
  soft dependencies and not required to use Pooch. See :ref:`install`. (`#78
  <https://github.com/fatiando/pooch/pull/78>`__)
* New processor ``pooch.Untar`` unpacks files contained in a downloaded tar archive
  (with or without compression). (`#77 <https://github.com/fatiando/pooch/pull/77>`__)

This release contains contributions from:

* Matthew Turk
* Leonardo Uieda

Version 0.4.0
-------------

*Released on: 2019/05/01*

New features:

* Add customizable downloaders. Delegate file download into separate classes that can be
  passed to ``Pooch.fetch``. Created the ``HTTPDownloader`` class (used by default)
  which can also be used to download files that require authentication/login. (`#66
  <https://github.com/fatiando/pooch/pull/66>`__)
* Add post-download processor hooks to ``Pooch.fetch``. Allows users to pass in a
  function that is executed right before returning and can overwrite the file path that
  is returned by ``fetch``. Use this, for example, to perform unpacking/decompression
  operations on larger files that can be time consuming and we only want to do once.
  (`#59 <https://github.com/fatiando/pooch/pull/59>`__)
* Add the ``Unzip`` post-download processor to extract files from a downloaded zip
  archive. Unpacks files into a directory in the local store and returns a list of all
  unzipped files. (`#72 <https://github.com/fatiando/pooch/pull/72>`__)
* Make the ``check_version`` function public. It's used internally but will be useful in
  examples that want to download things from the pooch repository. (`#69
  <https://github.com/fatiando/pooch/pull/69>`__)

Maintenance:

* Pin sphinx to version 1.8.5. New versions of Sphinx (2.0.*) are messing up the
  numpydoc style docstrings. (`#64 <https://github.com/fatiando/pooch/pull/64>`__)

This release contains contributions from:

* Santiago Soler
* Leonardo Uieda

Version 0.3.1
-------------

*Released on: 2019/03/28*

Minor patches:

* Add a project logo (`#57 <https://github.com/fatiando/pooch/pull/57>`__)
* Replace ``http`` with ``https`` in the ``README.rst`` to avoid mixed content warnings
  in some browsers (`#56 <https://github.com/fatiando/pooch/pull/56>`__)

Version 0.3.0
-------------

*Released on: 2019/03/27*

New features:

* Use the ``appdirs`` library to get the cache directory. **Could change the default
  data location on all platforms**. Locations are compatible with the
  `XDG Base Directory Specification <https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`__
  (`#45 <https://github.com/fatiando/pooch/pull/45>`__)
* Add method ``Pooch.is_available`` to check remote file availability
  (`#50 <https://github.com/fatiando/pooch/pull/50>`__)
* Add ``Pooch.registry_files`` property to get a name of all files in the registry
  (`#42 <https://github.com/fatiando/pooch/pull/42>`__)
* Make ``Pooch.get_url`` a public method to get the download URL for a given file
  (`#55 <https://github.com/fatiando/pooch/pull/55>`__)

Maintenance:

* **Drop support for Python 3.5**. Pooch now requires Python >= 3.6.
  (`#52 <https://github.com/fatiando/pooch/pull/52>`__)
* Add a private method to check if a file is in the registry (`#49 <https://github.com/fatiando/pooch/pull/49>`__)
* Fix typo in the ``Pooch.load_registry`` docstring (`#41 <https://github.com/fatiando/pooch/pull/41>`__)

This release contains contributions from:

* Santiago Soler
* Rémi Rampin
* Leonardo Uieda

Version 0.2.1
-------------

*Released on: 2018/11/15*

Bug fixes:

* Fix unwanted ``~`` directory creation when not using a ``version`` in ``pooch.create``
  (`#37 <https://github.com/fatiando/pooch/pull/37>`__)


Version 0.2.0
-------------

*Released on: 2018/10/31*

Bug fixes:

* Avoid copying of files across the file system (`#33 <https://github.com/fatiando/pooch/pull/33>`__)
* Correctly delete temporary downloads on error (`#32 <https://github.com/fatiando/pooch/pull/32>`__)

New features:

* Allow custom download URLs for individual files (`#30 <https://github.com/fatiando/pooch/pull/30>`__)
* Allow dataset versioning to be optional (`#29 <https://github.com/fatiando/pooch/pull/29>`__)

Maintenance:

* Move URLs building to a dedicated method for easy subclassing (`#31 <https://github.com/fatiando/pooch/pull/31>`__)
* Add testing and support for Python 3.7 (`#25 <https://github.com/fatiando/pooch/pull/25>`__)


Version 0.1.1
-------------

*Released on: 2018/08/30*

Bug fixes:

* Check if the local data folder is writable and warn the user instead of crashing
  (`#23 <https://github.com/fatiando/pooch/pull/23>`__)


Version 0.1
-----------

*Released on: 2018/08/20*

* Fist release of Pooch. Manages downloading sample data files over HTTP from a server
  and storing them in a local directory. Main features:

  - Download a file only if it's not in the local storage.
  - Check the SHA256 hash to make sure the file is not corrupted or needs updating.
  - If the hash is different from the registry, Pooch will download a new version of
    the file.
  - If the hash still doesn't match, Pooch will raise an exception warning of possible
    data corruption.
