.. _paralleldownloads:

Parallel downloads
==================

When running :func:`pooch.retrieve` or :meth:`pooch.Pooch.fetch` on parallel
processes, Pooch will trigger multiple downloads of the same file(s). Although
there is no `race condition <https://en.wikipedia.org/wiki/Race_condition>`_
happening in this process, download the same file multiple time is not
desirable, it slows down the fetching process and consumes more bandwidth than
necessary.

A solution to this problem is to create a `lock file
<https://en.wikipedia.org/wiki/File_locking#Lock_files>`_ that will allow only
one process to download the desired file, and force all the other processes to
wait until it finishes for fetching the file directly from the cache.
Lock files can be easily created through the :mod:`filelock` package.

For example, let's create a ``download.py`` file that defines a lock file
before calling the :fun:`pooch.retrieve` function.

.. code:: python

   # file: download.py
   import pooch
   import filelock

   lock = filelock.LockFile(path="foo.lock")
   with lock:
       file_path = pooch.retrieve(
           url="https://github.com/fatiando/pooch/raw/v1.0.0/data/tiny-data.txt",
           known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
           path="my_dir",
       )

   # Perform tasks with this file using different parameters passed as argument
   parameter = sys.arg[1] # get parameter from first argument
   ... # perform tasks using the file and the parameter

We can run this script in parallel using the Bash ampersand:

.. code:: bash

   python download.py 1 &
   python download.py 2 &
   python download.py 3 &

Since we are using a lock file, only one of these process will take care of the
download. The rest will wait for it to finish, and then fetch the file from the
cache. Then all further tasks that the ``download.py`` performs using the
different arguments will be run in parallel as usual.
