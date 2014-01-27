import sys
from logging_levels.standards import add_standards    

def test_level_standards(logging, log):
    """
    Ensure that the standard log levels work 
    """
    add_standards(logging)
    
    assert logging.TRACE == 5
    assert logging.VERBOSE == 7

    log.verbose("I've said too much")
    assert log.last() == ['VERBOSE', "I've said too much"]

    log.trace("But I haven't said enough")
    assert log.last() == ['TRACE', "But I haven't said enough"]

def test_standards_suppressed(logging, log):
    """
    Ensure that the suppressed log level includes
    the suppressed exception
    """
    add_standards(logging)

    assert logging.SUPPRESSED

    try:
        raise Exception('Suppress this')
    except:
        log.suppressed('Suppressed exception')

    lines = ''.join(log.readlines())
    assert lines.startswith('SUPPRESSED:')
    assert 'Exception: Suppress this' in lines

