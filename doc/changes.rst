.. _changes:

Changelog
=========

Version 0.1.1 (2018-08-30)
--------------------------

**Bug fixes:**

* Check if the local data folder is writable and warn the user instead of crashing
  (`#23 <https://github.com/fatiando/pooch/pull/23>`__)

Version 0.1 (2018-08-20)
------------------------

* Fist release of Pooch. Manages downloading sample data files over HTTP from a server
  and storing them in a local directory. Main features:

  - Download a file only if it's not in the local storage.
  - Check the SHA256 hash to make sure the file is not corrupted or needs updating.
  - If the hash is different from the registry, Pooch will download a new version of
    the file.
  - If the hash still doesn't match, Pooch will raise an exception warning of possible
    data corruption.
