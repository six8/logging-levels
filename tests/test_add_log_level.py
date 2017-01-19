from logging_levels import add_log_level

from uuid import uuid4
import pytest


def test_add_levels(logging, log):
    """
    Ensure that we can add a couple log levels and log with them
    """
    assert not hasattr(logging, 'TEST')
    assert not hasattr(logging, 'FOO')

    add_log_level(TEST=5, FOO=1, logging=logging)

    assert logging.TEST == 5
    assert logging.FOO == 1

    for i in range(10):
        message = 'Testing TEST {0}'.format(uuid4())
        log.test(message)

        lvl, msg = log.last()
        assert lvl == 'TEST'
        assert msg == message

    for i in range(10):
        message = 'Testing FOO {0}'.format(uuid4())
        log.foo(message)

        lvl, msg = log.last()
        assert lvl == 'FOO'
        assert msg == message


def test_log_level_works(logging, log):
    """
    Ensure that log messages only appear in the logging
    if the log level is within range.
    """
    add_log_level(SPAM=1, NOISE=5, IMPORTANT=1000, logging=logging)

    log.setLevel(logging.DEBUG)

    # Debug message should appear
    log.debug('debug')

    assert log.last() == ['DEBUG', 'debug']

    # Noise message should NOT appear
    log.noise('noise')
    assert not log.last()

    # Spam message should NOT appear
    log.spam('spam')
    assert not log.last()

    # Important message should appear
    log.important('important')
    assert log.last() == ['IMPORTANT', 'important']

    log.setLevel(logging.NOISE)

    # Noise message should now appear
    log.noise('noise')
    assert log.last() == ['NOISE', 'noise']

    # Important message should still appear
    log.important('important')
    assert log.last() == ['IMPORTANT', 'important']

    # Spam message should NOT appear
    log.spam('spam')
    assert not log.last()


def test_names_must_be_upper_case(logging):
    """
    Ensure logging names must be uppercase
    """

    with pytest.raises(KeyError):
        # Lowercase not OK
        add_log_level(foo=1, logging=logging)

    # Upper case OK
    add_log_level(FOO=1, logging=logging)

    # Underscore OK
    add_log_level(FOO_BAR=1, logging=logging)


def test_add_levels_with_exceptions(logging, log):
    """
    Ensure that we can add a log level that
    also logs exception.
    """
    assert not hasattr(logging, 'WTF')

    add_log_level(WTF=5000, logging=logging, exceptions=True)

    assert logging.WTF == 5000

    try:
        raise Exception('What was that?')
    except:
        log.wtf('Something just happened')

    lines = ''.join(log.readlines())
    assert lines.startswith('WTF:')
    assert 'Exception: What was that?' in lines


def test_override_default_levels(logging, log):
    """
    Ensure we can not overwrite existing log levels
    """

    # Override default log levels?
    assert logging.DEBUG == 10

    with pytest.raises(KeyError):
        add_log_level(DEBUG=5000, logging=logging)

    # Override custom log levels?
    add_log_level(MONKEY=1000, logging=logging)
    assert logging.MONKEY == 1000

    with pytest.raises(KeyError):
        add_log_level(MONKEY=1000, logging=logging)


def test_log_level_must_be_int(logging, log):
    """
    Ensure log levels are ints
    """
    with pytest.raises(ValueError):
        add_log_level(DANG='dang', logging=logging)

    # Do it correctly this time
    add_log_level(DANG=1, logging=logging)
    assert logging.DANG == 1


def test_root_logger_methods(logging):
    """
    Ensure new logging methods work on root logger
    """
    assert not hasattr(logging, 'roof')
    add_log_level(ROOF=1, logging=logging)
    logging.roof('Test roof')


def test_aliases_change_builtin_severity_levels(logging, log):
    """
    This test asserts a specific behavior of how adding log levels
    behaves when using the python logging modules. If you add a level
    using logging-levels for a log level that already exists, your new
    level will override any existing level. This can be intended, but
    it can have unintended consequences if you're not expecting it.
    """
    assert not hasattr(logging, 'SUPPRESSED')

    add_log_level(SUPPRESSED=logging.WARN, logging=logging)

    assert logging.SUPPRESSED == logging.WARN

    message = 'Testing suppressed logging {0}'.format(uuid4())
    log.suppressed(message)

    lvl, msg = log.last()
    assert lvl == 'SUPPRESSED'
    assert msg == message

    message = 'Testing warning logging {0}'.format(uuid4())

    # Python still tracks a shortcut for WARN here, but after adding
    # SUPPRESSED at the same level above, python has updated it's mapping
    # from NAME to LVL to be this latest level name. This severity alias
    # will work, but the level name will be the new level.
    log.warn(message)

    lvl, msg = log.last()
    assert lvl == 'SUPPRESSED'
    assert msg == message
