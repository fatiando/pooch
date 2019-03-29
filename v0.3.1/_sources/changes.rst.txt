.. _changes:

Changelog
=========

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
