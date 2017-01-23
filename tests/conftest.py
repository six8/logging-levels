import logging
import sys
import pytest

try:
    from StringIO import StringIO as Stream    
except ImportError:
    # Python 3.x use io.StringIO but not in 2.x
    # because in 2.x io.StringIO expects unicodes
    from io import StringIO as Stream


@pytest.fixture(scope='function')
def logging(request):
    """
    Get an isolated logging module
    """
    # Remove existing logging module so we don't re-use it
    sys.modules.pop('logging', None)
    import logging
    sys.modules['logging'] = logging

    def exit():
        loaded = sys.modules.get('logging', None)
        if loaded == logging:
            # Remove so others don't use it
            del sys.modules['logging']

    request.addfinalizer(exit)

    return logging


@pytest.fixture
def stream_log():
    """
    Returns a function that will create a logger
    for the specified logging module
    with a StringIO log handler and sets the format
    to "{levelname}:{message}".
    """

    def make(logging):
        stream = Stream()
        handler = logging.StreamHandler(stream)

        formatter = logging.Formatter('%(levelname)s:%(message)s')
        handler.setFormatter(formatter)

        log = logging.getLogger()
        log.setLevel(0)
        for handler in log.handlers:
            log.removeHandler(handler)
        log.addHandler(handler)

        ctx = {'pos': 0}

        def readlines():
            """
            Read one line from the log stream.
            """
            handler.flush()
            stream.seek(ctx['pos'])
            lines = stream.readlines()
            ctx['pos'] = stream.tell()
            return lines

        def last():
            """
            Returns the last log message as a tuple of levelname and message
            """
            lines = readlines()
            if lines:
                msg = lines[-1]
                return msg.strip().split(':', 1)

        log.readlines = readlines
        log.last = last
        return log
    return make


@pytest.fixture(scope='function')
def log(logging, stream_log):
    """
    Get a logger for the isolated logging module
    with a StringIO log handler and sets the format
    to "{levelname}:{message}".
    """
    return stream_log(logging)
