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
        # Log debug details of constant changes
        TRACE=5 , 
        # Log debug with a little more chattyness
        VERBOSE=7,
        logging=logging
    )

    # Log a suppressed exception at warning level
    add_log_level(
        SUPPRESSED=logging.WARN,
        exceptions=True, 
        logging=logging
    )