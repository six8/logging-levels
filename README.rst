==============
logging-levels
==============

.. image:: https://travis-ci.org/six8/logging-levels.png
   :target: https://travis-ci.org/six8/logging-levels

As projects get bigger, ``logging.debug()`` becomes the dumping
ground for everything that your application is doing. This usually
becomes so noisy that you can't really make sense of what you're 
trying to debug. 

Although it is usually disabled in production, 
sometimes you need to enable debug logging to -- you know -- actually
debug something. But since *everything* is dumped there, it's too
much of a mess to wade through.

To help with this, you can add extra logging levels. However, rarely
are they added to projects and when they are, they're often incomplete.
Then sometimes you go to other projects and they're not there. So you
have to lookup how to add them but usually give up and just stick with
dumping something in ``logging.debug()`` cause you'll remove it later
-- right?

What if it was as easy as 2 lines of code to add a new log level?

Bam!:

.. code:: python

    from logging_levels import add_log_level
    add_log_level(VERBOSE=9)

How about a few new log levels?:

.. code:: python

    add_log_level(VERBOSE=9, TRACE=8, NOISE=5, IMPORTANT=100)

Now log with them:

.. code:: python

    log.verbose("I've said too much")
    log.trace("But I haven't said enough")
    log.noise("That's me in the corner")
    log.important("That's me in the spotlight")

Want to implicitly log exceptions with your fancy new log level?:

.. code:: python

    add_log_level(DANG=90, exceptions=True)

    try:
        raise Exception('Oops')
    except:
        # Will include exception in log
        log.dang('Something broke.')

To help everyone standardize on some log levels, logging_levels
has standards:

.. code:: python

    import logging_levels.standards    

    log.trace('Log every -- single -- detail')
    log.verbose('Debug, but so much more')
    log.suppressed('Warn a suppressed exception')        

Project Loggers
---------------

By defualt, logging_levels manipulates the global logging module.
For your projects -- especially if you're creating open source
modules -- you should isolate your logging module.

.. code:: python

    from logging_levels import isolated_logging, log_exceptions

    logging = isolated_logging(
        STUFF=8,
        THINGS=22,
        WTF=log_exceptions(1000),
    )

    logging.stuff('Log some stuff')
    logging.wtf('Log some exceptions')

If you create this isolated logging module
in ``mylib/__init__.py``, then you can use it throughout your
project easily.

.. code:: python

    from mylib import logging
    logging.error('Oops, broke something.')

Installing
----------

.. code-block:: console

    pip install logging_levels

Testing
-------

Install dev requirements:

.. code-block:: console

    pip install -r dev.requirements.txt

Install project:

.. code-block:: console

    pip install -e .

Run pytest:

.. code-block:: console

    py.test tests