def add_log_level(exceptions=False, logging=None, **kwargs):
    """
    Add additional log levels. 

    :param logging: Logging module to use (default ``import logging``).
    :param exceptions: True to include exceptions by default with these log levels.
    :param kwargs: dict of with log name as the key and log level as the value.
        Level names must be UPPER_CASE

    Example::

        add_log_level(TRACE=8, VERBOSE=9, exceptions=True)
    """    
    if not logging:
        import logging

    for name, level in kwargs.items():
        if not name.isupper():
            raise KeyError('Logging level name "{0}" must be upper case.'.format(name))

        existing = getattr(logging, name, None)
        if existing:
            raise KeyError('Can not register log level name "{0}" as it already exists.'.format(name))

        if not isinstance(level, int):
            raise ValueError('Level for log level name "{0}" must be int, got "{1}".'.format(name, level))

    # Now that error checking is out of way, register handlers
    for name, level in kwargs.items():
        _make_log_level(name, level, exceptions, logging)

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