# -*- coding: utf-8 -*-
import unittest
import time
try:
    from unittest import mock
except ImportError:
    import mock
from logrusformatter import LogrusFormatter, COLORS


class TestFormatter(unittest.TestCase):

    @mock.patch('logging.Formatter.__init__', return_value=None)
    def test_init_formatter(self, mock_init):
        formatter = LogrusFormatter()
        self.assertTrue(mock_init.called)
        self.assertEqual(formatter.colorize, False)

    @mock.patch('logging.Formatter.format')
    def test_format(self, mock_format):
        formatter = LogrusFormatter()
        # Mocking logging.Formatter.format

        def format_effect(formatter, record):
            return formatter._fmt % record.__dict__
        mock_format.side_effect = format_effect
        # Mocking LogRecord
        mock_record = mock.Mock(spec='logging.LogRecord')

        # LogRecord attributes
        str_attrs = ["asctime", "filename", "funcName", "levelno", "module",
                     "message", "name", "pathname", "processName", "threadName"]
        float_attrs = ["lineno", "msecs", "process", "relativeCreated",
                       "thread"]
        # Test string attributes without color
        for att in str_attrs:
            mock_record.reset_mock()
            mock_record.created = int(time.time())
            mock_record.levelname = "INFO"
            formatter._fmt = "%({0})s".format(att)
            setattr(mock_record, att, "test")
            self.assertEqual(formatter.format(
                record=mock_record), "{0}=test".format(att))
            mock_format.assert_called_with(formatter, mock_record)
        # Test float attributes without color
        for att in float_attrs:
            mock_record.reset_mock()
            mock_record.created = int(time.time())
            mock_record.levelname = "INFO"
            formatter._fmt = "%({0})s".format(att)
            setattr(mock_record, att, 1.1)
            self.assertEqual(formatter.format(
                record=mock_record), "{0}=1.1".format(att))
            mock_format.assert_called_with(formatter, mock_record)
        # Test colors
        color_formatter = LogrusFormatter(True)
        levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        for lvl in levels:
            mock_record.reset_mock()
            mock_record.created = int(time.time())
            mock_record.levelname = lvl
            mock_record.message = "test"
            log = color_formatter.format(record=mock_record)
            self.assertEqual(
                "\033[{0}mmessage\033[0m=test\033[0m".format(30 + COLORS[lvl]),
                log)
