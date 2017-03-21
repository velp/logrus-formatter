# -*- coding: utf-8 -*-
"""
LogrusFormatter
-----------------------

The format of the log library for simulating Logrus golang library
https://github.com/sirupsen/logrus

Formatter supports color output of the log.

Modified standard log record attributes
(https://docs.python.org/2/library/logging.html#logrecord-attributes):
asctime            %(asctime)s         -> %(datetime)s
created            %(created)f         -> %(created)s
lineno             %(lineno)d          -> %(lineno)s
msecs              %(msecs)d           -> %(msecs)s
process            %(process)d         -> %(process)s
relativeCreated    %(relativeCreated)d -> %(relativeCreated)s
thread             %(thread)d          -> %(thread)s

The name of the attribute in the log is the name of the field.

Example:
    fmt_string = "%(levelname)s %(message)-20s %(threadName)s " \
        "%(processName)s %(datetime)s"
    fmtr = LogrusFormatter(fmt=fmt_string)
    # Create logger
    logger = logging.getLogger('example')
    logger.setLevel(logging.DEBUG)
    # Add handler
    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setFormatter(fmtr)
    logger.addHandler(hdlr)
    # Example logging
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

Output:
    [DEBU] debug message        threadName=MainThread processName=MainProcess \
    datetime=2017-03-21T11:58:48.132062
    [INFO] info message         threadName=MainThread processName=MainProcess \
    datetime=2017-03-21T11:58:48.132263
    [WARN] warning message      threadName=MainThread processName=MainProcess \
    datetime=2017-03-21T11:58:48.132395
    [ERRO] error message        threadName=MainThread processName=MainProcess \
    datetime=2017-03-21T11:58:48.132525
    [CRIT] critical message     threadName=MainThread processName=MainProcess \
    datetime=2017-03-21T11:58:48.132661
"""

import logging
from datetime import datetime
import six

__all__ = ["LogrusFormatter"]
__version__ = 0.1

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    # Colors by level
    'WARNING': YELLOW,
    'INFO': BLUE,
    'DEBUG': WHITE,
    'CRITICAL': YELLOW,
    'ERROR': RED,
}

SHORT_LEVELS = {
    'DEBUG': '[DEBU]',
    'INFO': '[INFO]',
    'WARNING': '[WARN]',
    'ERROR': '[ERRO]',
    'CRITICAL': '[CRIT]'
}
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[%dm"
BOLD_SEQ = "\033[1m"


class LogrusFormatter(logging.Formatter):
    """A :class:`~logging.Formatter` which defines a set of parameters in the
    log line
    """

    def __init__(self, colorize=False, *args, **kwargs):
        """
        :param colorize: enable color output
        """
        self.colorize = colorize
        # can't do super(...) here because Formatter is an old school class
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        """Formatting the log line. The output color is set. Parameters are
        parsed.

        :param record: a :class:`~logging.LogRecord`
        """
        levelname = record.levelname
        # Get level color
        lvl_color = COLOR_SEQ % (30 + COLORS[levelname])
        if self.colorize:
            attr_tmpl = "%s{0}%s={1}" % (lvl_color, RESET_SEQ)
            # Rename level
            record.levelname = lvl_color + SHORT_LEVELS[levelname] + RESET_SEQ
        else:
            attr_tmpl = "{0}={1}"
            # Rename level
            record.levelname = SHORT_LEVELS[levelname]
        # Add datetime attribute
        record.datetime = datetime.fromtimestamp(
            record.created).strftime("%Y-%m-%dT%H:%M:%S.%f")
        # Formatt and colorize other attributes
        # Attributes: levelno, lineno, process, thread convert from int to str
        types = six.string_types + six.integer_types + (float,)
        for attr_name in dir(record):
            if not(attr_name.startswith('__') and attr_name.endswith('__')):
                # Unchangeable Attributes
                if attr_name not in ['msg', 'args', 'exc_info', 'levelname']:
                    attr_val = getattr(record, attr_name)
                    if isinstance(attr_val, types):
                        val = attr_tmpl.format(attr_name, attr_val)
                        setattr(record, attr_name, val)
        # Set custom attributes
        if self.colorize:
            record.color = lvl_color
            record.color_reset = RESET_SEQ
            record.color_bold = BOLD_SEQ
        # make message
        message = logging.Formatter.format(self, record)
        if self.colorize:
            return message + RESET_SEQ
        else:
            return message
