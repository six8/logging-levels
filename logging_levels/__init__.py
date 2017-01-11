import sys


class Level(object):
    """
    Represents a log level
    """
    def __init__(self, level, exceptions=False):
        """
        :param level: int log level
        :param exceptions: True to log exceptions for this level
        """
        self.level = level
        self.exceptions = exceptions


def log_exceptions(level):
    """
    Shortcut to create a Level that logs exceptions
    """
    return Level(level, exceptions=True)


def isolated_logging(**levels):
    """
    Get an isolated logging module that you can modify
    without affecting the global logging module import.

    Example::

        logging = isolated_logging(
            STUFF=8,
            THINGS=22,
            WTF=log_exceptions(1000),
        )

        logging.stuff('Log some stuff')
        logging.wtf('Log some exceptions')

    :param levels: Same as ``add_log_level``
    """
    # Get current module so we can put it back
    existing = sys.modules.pop('logging', None)

    # Import logging module in isolated closure
    import logging

    if levels:
        add_log_level(logging=logging, **levels)

    if existing:
        # Put old module back
        sys.modules['logging'] = existing
    else:
        # Remove our new import to keep others from getting it
        del sys.modules['logging']

    return logging


def add_log_level(exceptions=False, logging=None, **levels):
    """
    Add additional log levels.

    :param logging: Logging module to use (default ``import logging``).
    :param exceptions: True to include exceptions by default with these log levels.
    :param levels: dict of with log name as the key and log level as the value.
        Level names must be UPPER_CASE

    Example::

        add_log_level(TRACE=8, VERBOSE=9, exceptions=True)
        add_log_level(WTF=log_exceptions(1000))
    """
    if not logging:
        import logging

    for name, level in levels.items():
        if not name.isupper():
            raise KeyError('Logging level name "{0}" must be upper case.'.format(name))

        existing = getattr(logging, name, None)
        if existing:
            raise KeyError('Can not register log level name "{0}" as it already exists.'.format(name))

        if not isinstance(level, (int, Level)):
            raise ValueError('Level for log level name "{0}" must be int or Level, got "{1}".'.format(name, level))

    # Now that error checking is out of way, register handlers
    for name, level in levels.items():
        include_exceptions = exceptions
        if isinstance(level, Level):
            include_exceptions = level.exceptions
            level = level.level

        _make_log_level(name, level, include_exceptions, logging)


def _make_log_level(name, level, exceptions, logging):
    """
    Create neccessary log levels, functions, and
    logging attributes for a new log level.
    """
    logging.addLevelName(level, name)
    setattr(logging, name, level)

    func_name = name.lower()

    def log(self, message, *args, **kws):
        if exceptions:
            # Include exceptions by default
            kws['exc_info'] = kws.get('exc_info', True)

        self.log(level, message, *args, **kws)

    log.__name__ = func_name

    setattr(logging.Logger, func_name, log)

    def log_root(message, *args, **kws):
        if exceptions:
            # Include exceptions by default
            kws['exc_info'] = kws.get('exc_info', True)

        logging.log(level, message, *args, **kws) 

    log_root.__name__ = func_name

    setattr(logging, func_name, log_root)
