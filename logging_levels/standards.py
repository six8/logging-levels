"""
Everyone should have standards.
Import some additional standardize log levels.

Example::

    import logging_levels.standards
    import logging

    logging.verbose("I've said too much")
    logging.trace("But I haven't said enough")
"""
from logging_levels import add_log_level
import logging

add_log_level(
    # Log debug details of constant changes
    TRACE=8, 
    # Log debug with a little more chattyness
    VERBOSE=9,
)

# Log a suppressed exception a warning level
add_log_level(
    SUPPRESSED=logging.WARN,
    exceptions=True, 
)