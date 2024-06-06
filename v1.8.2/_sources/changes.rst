.. _changes:

Changelog
=========

Version 1.8.2
-------------

Released on: 2024/06/06

DOI: https://doi.org/10.5281/zenodo.11493461

Bug fixes:

* Use a variable to set the default request timeout (`#418 <https://github.com/fatiando/pooch/pull/418>`__)

Documentation:

* Add HyperSpy, RosettaSciIO, eXSpy to projects using pooch (`#408 <https://github.com/fatiando/pooch/pull/408>`__)
* Add more packages using Pooch (`#403 <https://github.com/fatiando/pooch/pull/403>`__)

Maintenance:

* Add optional dependencies to environment.yml (`#413 <https://github.com/fatiando/pooch/pull/413>`__)
* Run tests with oldest dependencies on x86 macos (`#414 <https://github.com/fatiando/pooch/pull/414>`__)
* Mark additional tests requiring network (`#412 <https://github.com/fatiando/pooch/pull/412>`__)
* Fix package description in pyproject.toml (`#407 <https://github.com/fatiando/pooch/pull/407>`__)
* Setup Trusted Publisher deployment to PyPI (`#406 <https://github.com/fatiando/pooch/pull/406>`__)
* Use Burocrata to check and add license notices (`#402 <https://github.com/fatiando/pooch/pull/402>`__)
* Use pyproject.toml instead of setup.cfg (`#401 <https://github.com/fatiando/pooch/pull/401>`__)

This release contains contributions from:

* Sandro
* Jonas Lähnemann
* Santiago Soler
* Leonardo Uieda

Version 1.8.1
-------------

Released on: 2024/02/19

DOI: https://doi.org/10.5281/zenodo.10680982

Bug fixes:

* Use the ID instead of persistentID for Dataverse downloads since some repositories don't issue persistentIDs but all issue normal IDs (`#355 <https://github.com/fatiando/pooch/pull/355>`__)
* Ensure all archive members are unpacked in subsequent uses of ``Untar``/``Unzip`` if the first call only asked for a few members (`#365 <https://github.com/fatiando/pooch/pull/365>`__)

Documentation:

* Move "Projects using Pooch" further up the README (`#386 <https://github.com/fatiando/pooch/pull/386>`__)
* Update the versions of sphinx and its plugins (`#385 <https://github.com/fatiando/pooch/pull/385>`__)

Maintenance:

* Remove many deprecated pylint options (`#329 <https://github.com/fatiando/pooch/pull/329>`__)
* Use Dependabot to manage GitHub Actions (`#387 <https://github.com/fatiando/pooch/pull/387>`__)
* Simplify the test GitHub Actions workflow (`#384 <https://github.com/fatiando/pooch/pull/384>`__)
* Update format for Black 24.1.1 (`#383 <https://github.com/fatiando/pooch/pull/383>`__)

This release contains contributions from:

* Mark Harfouche
* Juan Nunez-Iglesias
* Santiago Soler
* Leonardo Uieda

Version 1.8.0
-------------

Released on: 2023/10/24

DOI: https://doi.org/10.5281/zenodo.10037888

Bug fixes:

* Fix bug: add support for old and new Zenodo APIs (`#375 <https://github.com/fatiando/pooch/pull/375>`__)

New features:

* Only create local data directories if necessary (`#370 <https://github.com/fatiando/pooch/pull/370>`__)
* Speed up import time by lazy loading requests (`#328 <https://github.com/fatiando/pooch/pull/328>`__)

Maintenance:

* Add support for Python 3.11 (`#348 <https://github.com/fatiando/pooch/pull/348>`__)
* Only run CI cron job for the upstream repository (`#361 <https://github.com/fatiando/pooch/pull/361>`__)

Documentation:

* Add GemGIS to list of projects using Pooch (`#349 <https://github.com/fatiando/pooch/pull/349>`__)
* Fix spelling of Dataverse (`#353 <https://github.com/fatiando/pooch/pull/353>`__)
* Fix grammar on retrieve documentation (`#359 <https://github.com/fatiando/pooch/pull/359>`__)

This release contains contributions from:

* Hugo van Kemenade
* AlexanderJuestel
* Mark Harfouche
* Philip Durbin
* Rob Luke
* Santiago Soler
* Stephan Hoyer


Version 1.7.0
-------------

Released on: 2023/02/27

DOI: https://doi.org/10.5281/zenodo.7678844

Bug fixes:

* Make archive extraction always take members into account (`#316 <https://github.com/fatiando/pooch/pull/316>`__)
* Figshare downloaders fetch the correct version, instead of always the latest one. (`#343 <https://github.com/fatiando/pooch/pull/343>`__)

New features:

* Allow spaces in filenames in registry files (`#315 <https://github.com/fatiando/pooch/pull/315>`__)
* Refactor ``Pooch.is_available`` to use downloaders (`#322 <https://github.com/fatiando/pooch/pull/322>`__)
* Add support for downloading files from Dataverse DOIs (`#318 <https://github.com/fatiando/pooch/pull/318>`__)
* Add a new ``Pooch.load_registry_from_doi`` method that populates the Pooch registry using DOI-based data repositories (`#325 <https://github.com/fatiando/pooch/pull/325>`__)
* Support urls for Zenodo repositories created through the GitHub integration service, which include slashes in the filename of the main zip files (`#340 <https://github.com/fatiando/pooch/pull/340>`__)
* Automatically add a trailing slash to ``base_url`` on ``pooch.create`` (`#344 <https://github.com/fatiando/pooch/pull/344>`__)

Maintenance:

* Drop support for Python 3.6 (`#299 <https://github.com/fatiando/pooch/pull/299>`__)
* Port from deprecated ``appdirs`` to ``platformdirs`` (`#339 <https://github.com/fatiando/pooch/pull/339>`__)
* Update version of Codecov's Action to v3 (`#345 <https://github.com/fatiando/pooch/pull/345>`__)

Documentation:

* Update sphinx, theme, and sphinx-panels (`#300 <https://github.com/fatiando/pooch/pull/300>`__)
* Add CITATION.cff for the JOSS article (`#308 <https://github.com/fatiando/pooch/pull/308>`__)
* Use Markdown for the README (`#311 <https://github.com/fatiando/pooch/pull/311>`__)
* Improve docstring of `known_hash` in `retrieve` function (`#333 <https://github.com/fatiando/pooch/pull/333>`__)
* Replace link to Pooch's citation with a BibTeX code snippet (`#335 <https://github.com/fatiando/pooch/pull/335>`__)

Projects that started using Pooch:

* Open AR-Sandbox (`#305 <https://github.com/fatiando/pooch/pull/305>`__)
* ``climlab`` (`#312 <https://github.com/fatiando/pooch/pull/312>`__)
* SciPy (`#320 <https://github.com/fatiando/pooch/pull/320>`__)
* ``napari`` (`#321 <https://github.com/fatiando/pooch/pull/321>`__)
* ``mne-python`` (`#323 <https://github.com/fatiando/pooch/pull/323>`__)

This release contains contributions from:

* Alex Fikl
* Anirudh Dagar
* Björn Ludwig
* Brian Rose
* Dominic Kempf
* Florian Wellmann
* Gabriel Fu
* Kyle I S Harrington
* Leonardo Uieda
* myd7349
* Rowan Cockett
* Santiago Soler

Version 1.6.0
-------------

Released on: 2022/01/24

DOI: https://doi.org/10.5281/zenodo.5793074

.. warning::

    **Pooch v1.6.0 is the last release that is compatible with Python 3.6.**

Important notes:

* Pooch now specifies version bounds for our required dependencies and a plan for dropping support for older versions. Please revise it if you depend on Pooch.

Enhancements:

* Add option to disable updates on hash mismatch (`#291 <https://github.com/fatiando/pooch/pull/291>`__ and `#292 <https://github.com/fatiando/pooch/pull/292>`__)
* Allow enabling progress bars with an argument in ``Pooch.fetch`` and ``retrieve`` (`#277 <https://github.com/fatiando/pooch/pull/277>`__)

Documentation:

* Use real data URLs in the README example code (`#295 <https://github.com/fatiando/pooch/pull/295>`__)
* Tell users to import from the top-level namespace (`#288 <https://github.com/fatiando/pooch/pull/288>`__)
* Update the contact link to `fatiando.org/contact <https://www.fatiando.org/contact/>`__ (`#282 <https://github.com/fatiando/pooch/pull/282>`__)
* Refer the community guides to `fatiando/community <https://github.com/fatiando/community>`__ (`#281 <https://github.com/fatiando/pooch/pull/281>`__)
* Mention in docs that figshare collections aren't supported (`#275 <https://github.com/fatiando/pooch/pull/275>`__)

Maintenance:

* Replace Google Analytics for `Plausible <https://plausible.io>`__ to make our docs more privacy-friendly (`#293 <https://github.com/fatiando/pooch/pull/293>`__)
* Use `Dependente <https://github.com/fatiando/dependente>`__ to capture dependencies on CI (`#289 <https://github.com/fatiando/pooch/pull/289>`__)
* Use ``build`` instead of setup.py (`#287 <https://github.com/fatiando/pooch/pull/287>`__)
* Run the tests weekly on GitHub Actions (`#286 <https://github.com/fatiando/pooch/pull/286>`__)
* Set minimum required version of dependencies (`#280 <https://github.com/fatiando/pooch/pull/280>`__)
* Rename "master" to "main" throughout the project (`#278 <https://github.com/fatiando/pooch/pull/278>`__)
* Remove trailing slash from GitHub handle in ``AUTHORS.md`` (`#279 <https://github.com/fatiando/pooch/pull/279>`__)

This release contains contributions from:

* Santiago Soler
* Genevieve Buckley
* Ryan Abernathey
* Ryan May
* Leonardo Uieda

Version 1.5.2
-------------

Released on: 2021/10/11

DOI: https://doi.org/10.5281/zenodo.5560923

Bug fixes:

* Fix bug when unpacking an entire subfolder from an archive. Now both unpacking processors (``Untar`` and ``Unzip``) handle ``members`` that are folders (not files) correctly. (`#266 <https://github.com/fatiando/pooch/pull/266>`__)

Enhancements:

* Add support for Python 3.10 (`#260 <https://github.com/fatiando/pooch/pull/260>`__)
* Point to the user's code for the file_hash warning instead of our internal code (which isn't very useful) (`#259 <https://github.com/fatiando/pooch/pull/259>`__)

Documentation:

* Fix typo in a variable name of the examples in the documentation (`#268 <https://github.com/fatiando/pooch/pull/268>`__)
* Fix typo when specifying the SFTP protocol in the about page (`#267 <https://github.com/fatiando/pooch/pull/267>`__)

Maintenance:

* Remove old testing checks if running on TravisCI (`#265 <https://github.com/fatiando/pooch/pull/265>`__)

This release contains contributions from:

* Santiago Soler
* Hugo van Kemenade
* Mark Harfouche
* Leonardo Uieda

Version 1.5.1
-------------

Released on: 2021/08/24

DOI: https://doi.org/10.5281/zenodo.5242882

.. warning::

    **Please use** ``from pooch import file_hash`` **instead of** ``from
    pooch.utils import file_hash``. This is backwards compatible with all
    previous versions of Pooch. We recommend importing all functions and
    classes from the top-level namespace.

Bug fixes:

* Make ``file_hash`` accessible from the ``pooch.utils`` module again. Moving
  this function to ``pooch.hashes`` caused crashes downstream. To prevent these
  crashes, add a wrapper back to utils that issues a warning that users should
  import from the top-level namespace instead.
  (`#257 <https://github.com/fatiando/pooch/pull/257>`__)
* Use a mirror of the test data directory in tests that write to it.
  (`#255 <https://github.com/fatiando/pooch/pull/255>`__)
* Add a pytest mark for tests accessing the network so that they can easily
  excluded when testing offline. (`#254 <https://github.com/fatiando/pooch/pull/254>`__)

This release contains contributions from:

* Antonio Valentino
* Leonardo Uieda

Version 1.5.0
-------------

Released on: 2021/08/23

DOI: https://doi.org/10.5281/zenodo.5235242

New features:

* Add support for non-cryptographic hashes from the xxhash package. They aren't
  as safe (but safe enough) and compute in fractions of the time from SHA or
  MD5. This makes it feasible to use hash checking on large datasets. (`#242
  <https://github.com/fatiando/pooch/pull/242>`__)
* Add support for using figshare and Zenodo DOIs as URLs (with the protocol
  ``doi:{DOI}/{file name}``, which works out-of-the-box with ``Pooch.fetch``
  and ``retrieve``). Can only download 1 file from the archive (not the full
  archive) and the file name must be specified in the URL. (`#241
  <https://github.com/fatiando/pooch/pull/241>`__)

Maintenance:

* Move hash functions to their own private module. No changes to the public
  API. (`#244 <https://github.com/fatiando/pooch/pull/244>`__)
* Run CI jobs on Python version extremes instead of all supported versions
  (`#243 <https://github.com/fatiando/pooch/pull/243>`__)

This release contains contributions from:

* Mark Harfouche
* Leonardo Uieda

Version 1.4.0
-------------

Released on: 2021/06/08

DOI: https://doi.org/10.5281/zenodo.4914758

Bug fixes:

* Fix bug in ``Untar`` and ``Unzip`` when the archive contains subfolders
  (`#224 <https://github.com/fatiando/pooch/pull/224>`__)

Documentation:

* New theme (``sphinx-book-theme``) and layout of the documentation (`#236
  <https://github.com/fatiando/pooch/pull/236>`__ `#237
  <https://github.com/fatiando/pooch/pull/237>`__ `#238
  <https://github.com/fatiando/pooch/pull/238>`__)

Enhancements:

* Add support for non-tqdm progress bars on HTTPDownloader (`#228
  <https://github.com/fatiando/pooch/pull/228>`__)
* Allow custom unpack locations in ``Untar`` and ``Unzip`` (`#224
  <https://github.com/fatiando/pooch/pull/224>`__)

Maintenance:

* Replace versioneer with setuptools-scm (`#235
  <https://github.com/fatiando/pooch/pull/235>`__)
* Automatically check license notice on code files (`#231
  <https://github.com/fatiando/pooch/pull/231>`__)
* Don't store documentation HTML as CI build artifacts (`#221
  <https://github.com/fatiando/pooch/pull/221>`__)

This release contains contributions from:

* Leonardo Uieda
* Agustina Pesce
* Clément Robert
* Daniel McCloy

Version 1.3.0
-------------

Released on: 2020/11/27

DOI: https://doi.org/10.5281/zenodo.4293216

Bug fixes:

* Properly handle capitalized hashes. On Windows, users might sometimes get
  capitalized hashes from the system. To avoid false hash mismatches, convert
  stored and computed hashes to lowercase before doing comparisons. Convert
  hashes to lowercase when reading from the registry to make sure stored hashes
  are always lowercase. (`#214 <https://github.com/fatiando/pooch/pull/214>`__)

New features:

* Add option to retry downloads if they fail. The new ``retry_if_failed``
  option to ``pooch.create`` and ``pooch.Pooch`` allows retrying the download
  the specified number of times in case of failures due to hash mismatches
  (coming from Pooch) or network issues (coming from ``requests``). This is
  useful for running downloads on CI that tend to fail sporadically. Waits a
  period of time between consecutive downloads starting with 1s and increasing
  up to 10s in 1s increments. (`#215
  <https://github.com/fatiando/pooch/pull/215>`__)
* Allow user defined decompressed file names. Introduce new ``name`` argument
  to ``pooch.Decompress`` to allow user defined file names. Defaults to the
  previous naming convention for backward compatibility. (`#203
  <https://github.com/fatiando/pooch/pull/203>`__)

Documentation:

* Add seaborn-image to list of packages using Pooch (`#218
  <https://github.com/fatiando/pooch/pull/218>`__)

Maintenance:

* Add support for Python 3.9. (`#220
  <https://github.com/fatiando/pooch/pull/220>`__)
* Drop support for Python 3.5. (`#204
  <https://github.com/fatiando/pooch/pull/204>`__)
* Use pip instead of conda to speed up Actions (`#216
  <https://github.com/fatiando/pooch/pull/216>`__)
* Add license and copyright notice to every .py file (`#213
  <https://github.com/fatiando/pooch/pull/213>`__)

This release contains contributions from:

* Leonardo Uieda
* Danilo Horta
* Hugo van Kemenade
* SarthakJariwala


Version 1.2.0
-------------

Released on: 2020/09/10

DOI: https://doi.org/10.5281/zenodo.4022246

.. warning::

    **Pooch v1.2.0 is the last release that is compatible with Python 3.5.**

Bug fixes:

* Fix FTP availability check when the file is in a directory. If the data file
  is not in the base directory, the ``Pooch.is_available`` test was broken
  since we were checking for the full path in ``ftp.nlst`` instead of just the
  file name. (`#191 <https://github.com/fatiando/pooch/pull/191>`__)

New features:

* Add the SFTPDownloader class for secure FTP downloads (`#165
  <https://github.com/fatiando/pooch/pull/165>`__)
* Expose Pooch version as ``pooch.__version__`` (`#179
  <https://github.com/fatiando/pooch/pull/179>`__)
* Allow line comments in registry files with ``#`` (`#180
  <https://github.com/fatiando/pooch/pull/180>`__)

Enhancements:

* Point to Unzip/tar from Decompress docs and errors (`#200
  <https://github.com/fatiando/pooch/pull/200>`__)

Documentation:

* Re-factor the documentation into separate pages (`#202
  <https://github.com/fatiando/pooch/pull/202>`__)
* Add warning to the docs about dropping Python 3.5 (`#201
  <https://github.com/fatiando/pooch/pull/201>`__)
* Add `histolab <https://github.com/histolab/histolab>`__ to the Pooch-powered
  projects (`#189 <https://github.com/fatiando/pooch/pull/189>`__)

Maintenance:

* Push documentation to GitHub Pages using Actions (`#198
  <https://github.com/fatiando/pooch/pull/198>`__)
* Add GitHub Actions workflow for publishing to PyPI (`#196
  <https://github.com/fatiando/pooch/pull/196>`__)
* Set up GitHub Actions for testing and linting (`#194
  <https://github.com/fatiando/pooch/pull/194>`__)
* Test FTP downloads using a local test server (`#192
  <https://github.com/fatiando/pooch/pull/192>`__)

This release contains contributions from:

* Leonardo Uieda
* Hugo van Kemenade
* Alessia Marcolini
* Luke Gregor
* Mathias Hauser

Version 1.1.1
-------------

Released on: 2020/05/14

DOI: https://doi.org/10.5281/zenodo.3826458

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

Released on: 2020/04/13

DOI: https://doi.org/10.5281/zenodo.3747184

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

Released on: 2020/01/28

DOI: https://doi.org/10.5281/zenodo.3629329

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

Released on: 2020/01/17

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

Released on: 2020/01/17

DOI: https://doi.org/10.5281/zenodo.3611376

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

Released on: 2019/11/19

DOI: https://doi.org/10.5281/zenodo.3547640

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

Released on: 2019/10/22

DOI: https://doi.org/10.5281/zenodo.3515031

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

Released on: 2019/06/24

Maintenance:

* Add back support for Python 3.5 with continuous integration tests. No code changes
  were needed, only removing the restriction from ``setup.py``.
  (`#93 <https://github.com/fatiando/pooch/pull/93>`__)

This release contains contributions from:

* Leonardo Uieda

Version 0.5.1
-------------

Released on: 2019/05/21

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

Released on: 2019/05/20

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

Released on: 2019/05/01

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

Released on: 2019/03/28

Minor patches:

* Add a project logo (`#57 <https://github.com/fatiando/pooch/pull/57>`__)
* Replace ``http`` with ``https`` in the ``README.rst`` to avoid mixed content warnings
  in some browsers (`#56 <https://github.com/fatiando/pooch/pull/56>`__)

Version 0.3.0
-------------

Released on: 2019/03/27

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

Released on: 2018/11/15

Bug fixes:

* Fix unwanted ``~`` directory creation when not using a ``version`` in ``pooch.create``
  (`#37 <https://github.com/fatiando/pooch/pull/37>`__)


Version 0.2.0
-------------

Released on: 2018/10/31

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

Released on: 2018/08/30

Bug fixes:

* Check if the local data folder is writable and warn the user instead of crashing
  (`#23 <https://github.com/fatiando/pooch/pull/23>`__)


Version 0.1
-----------

Released on: 2018/08/20

* Fist release of Pooch. Manages downloading sample data files over HTTP from a server
  and storing them in a local directory. Main features:

  - Download a file only if it's not in the local storage.
  - Check the SHA256 hash to make sure the file is not corrupted or needs updating.
  - If the hash is different from the registry, Pooch will download a new version of
    the file.
  - If the hash still doesn't match, Pooch will raise an exception warning of possible
    data corruption.
