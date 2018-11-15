.. _changes:

Changelog
=========


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
