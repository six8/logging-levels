import sys

def test_level_stanards(logging, log):
    """
    Ensure that the standard log levels work 
    """
    import logging_levels.standards    
    del sys.modules['logging_levels.standards'] # Force module to re-import
    
    assert logging.TRACE == 8
    assert logging.VERBOSE == 9

    log.verbose("I've said too much")
    assert log.last() == ['VERBOSE', "I've said too much"]

    log.trace("But I haven't said enough")
    assert log.last() == ['TRACE', "But I haven't said enough"]

def test_stanards_suppressed(logging, log):
    """
    Ensure that the suppressed log level includes
    the suppressed exception
    """
    import logging_levels.standards
    del sys.modules['logging_levels.standards'] # Force module to re-import

    assert logging.SUPPRESSED

    try:
        raise Exception('Suppress this')
    except:
        log.suppressed('Suppressed exception')

    lines = ''.join(log.readlines())
    assert lines.startswith('SUPPRESSED:')
    assert 'Exception: Suppress this' in lines

