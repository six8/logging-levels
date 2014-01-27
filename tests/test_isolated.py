from logging_levels import isolated_logging, log_exceptions
import logging

def test_isolated_module():
    """
    Ensure we can get an isolated logging module to mess with
    """
    my_logging = isolated_logging(
        STUFF=8,
        THINGS=22,
    )

    assert id(logging) != id(my_logging), 'Should not be same reference'

    assert my_logging.THINGS == 22
    assert my_logging.STUFF == 8

    assert not hasattr(logging, 'THINGS')
    assert not hasattr(logging, 'STUFF')

    my_logging2 = isolated_logging(
        HAPPS=8
    )

    assert id(my_logging) != id(my_logging2), 'Should not be same reference'

    assert my_logging2.HAPPS == 8
    assert not hasattr(my_logging, 'HAPPS')

def test_isolated_module_with_exceptions(stream_log):
    """
    Ensure we can create log levels with exceptions    
    """
    my_logging = isolated_logging(
        WTF=log_exceptions(100),
    )

    assert my_logging.WTF == 100

    log = stream_log(my_logging)

    try:
        raise Exception('OMG!')
    except:
        log.wtf('Something happened')

    lines = ''.join(log.readlines())
    assert lines.startswith('WTF:')
    assert 'Exception: OMG!' in lines



