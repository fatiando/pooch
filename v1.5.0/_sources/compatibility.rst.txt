.. _compatibility:

Compatibility notes
===================

Pooch version compatibility
---------------------------

We try to retain backwards compatibility whenever possible. Major breaking
changes to the Pooch API will be marked by a major release and deprecation
warnings will be issued in previous releases to give developers ample time to
adapt.

If there are any backwards incompatible changes, they will be listed below:

.. list-table::
    :widths: 20 10 70

    * - **Version introduced**
      - **Severity**
      - **Notes**
    * - v1.0.0
      - Low
      - We replaced use of ``warning`` with the ``logging`` module for all
        messages issued by Pooch. This allows messages to be logged with
        different priorities and the user filter out log messages or silence
        Pooch entirely. **Users who relied on Pooch issuing warnings will need
        to update to capturing logs instead.** The vast majority of users are
        unaffected.



.. _python-versions:

Python version compatibility
----------------------------

If you require support for older Python versions, please pin Pooch to the
following releases to ensure compatibility:

.. list-table::
    :widths: 40 60

    * - **Python version**
      - **Last compatible Pooch release**
    * - 2.7
      - 0.6.0
    * - 3.5
      - 1.2.0

