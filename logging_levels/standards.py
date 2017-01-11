"""
Everyone should have standards.
Import some additional standardize log levels.

Example::

    from logging_levels.standards import add_standards
    import logging
    add_standards(logging)

    logging.verbose("I've said too much")
    logging.trace("But I haven't said enough")
"""
from logging_levels import add_log_level


def add_standards(logging):
    """
    Add standard log levels to ``logging`` module
    """
    add_log_level(
        # From syslog: System is unusable.
        # This level should not be used by applications.
        EMERGENCY=100,

        # From syslog: Should be corrected immediately.
        # Loss of the primary ISP connection.
        ALERT=70,

        # From syslog: Events that are unusual, but not error conditions.
        NOTICE=25,

        # Log debug messages with a little more chattyness
        VERBOSE=7,

        # Log debug details of constant changes
        TRACE=5,
        logging=logging
    )

    # Log a suppressed exception at warning level
    add_log_level(
        # We want this to be nearly the same as WARN, but we don't
        # want to blow away the WARN log level name. If we used a
        # level below WARN these suppressed exceptions would not be
        # logged when setting the log level to WARN. Since we're
        # deliberately trying to expose exceptions and such at this
        # level we're choosing something right above the WARN level
        # so that we don't collide and so that it still gets logged.
        SUPPRESSED=logging.WARN + 1,
        exceptions=True,
        logging=logging
    )
