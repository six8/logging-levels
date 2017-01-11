from logging_levels.standards import add_standards


def test_level_standards(logging, log):
    """
    Ensure that the standard log levels work
    """
    add_standards(logging)

    assert logging.EMERGENCY == 100
    log.emergency("Emergency!")
    assert log.last() == ['EMERGENCY', "Emergency!"]

    assert logging.ALERT == 70
    log.alert("Alert!")
    assert log.last() == ['ALERT', "Alert!"]

    assert logging.NOTICE == 25
    log.notice("FYI")
    assert log.last() == ['NOTICE', "FYI"]

    assert logging.VERBOSE == 7
    log.verbose("I've said too much")
    assert log.last() == ['VERBOSE', "I've said too much"]

    assert logging.TRACE == 5
    log.trace("But I haven't said enough")
    assert log.last() == ['TRACE', "But I haven't said enough"]


def test_standards_suppressed(logging, log):
    """
    Ensure that the suppressed log level includes
    the suppressed exception.
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


def test_standards_suppressed_is_not_warn(logging, log):
    """
    Ensure that the new SUPPRESSED level does not collide with the
    existing python WARN level.
    """
    add_standards(logging)
    assert logging.SUPPRESSED == logging.WARN + 1
