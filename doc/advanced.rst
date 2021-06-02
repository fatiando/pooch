.. _advanced:

Advanced tricks
===============

These are more advanced things that can be done for specific use cases. **Most
projects will not require these**.


Adjusting the logging level
---------------------------

Pooch will log events like downloading a new file, updating an existing one, or
unpacking an archive by printing to the terminal. You can change how verbose
these events are by getting the event logger from pooch and changing the
logging level:

.. code:: python

    logger = pooch.get_logger()
    logger.setLevel("WARNING")

Most of the events from Pooch are logged at the info level; this code says that
you only care about warnings or errors, like inability to create the data
cache. The event logger is a :class:`logging.Logger` object, so you can use
that class's methods to handle logging events in more sophisticated ways if you
wish.
