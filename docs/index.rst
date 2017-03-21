=======================
LogrusFormatter
=======================
.. toctree::
   :maxdepth: 2
.. currentmodule:: logrusformatter

Logrus is a library for formatting the output of a standard logging system in a 
python. Modifies the log records, making them simulating `Logrus golang library <https://github.com/sirupsen/logrus>`_.

.. contents::
   :local:
   :backlinks: none

Basic usage
-----------

Initialize a :class:`LogrusFormatter` to add logging with fields::

    from logrusformatter import LogrusFormatter
    fmtr = LogrusFormatter(fmt=""%(levelname)s %(message)-20s (datetime)s")

and add formatter to logger::

    # Create logger
    logger = logging.getLogger('example')
    logger.setLevel(logging.DEBUG)
    # Add handler
    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setFormatter(fmtr)
    logger.addHandler(hdlr)

For color output use option :param:`colorize`::

    from logrusformatter import LogrusFormatter
    fmtr = LogrusFormatter(colorized=True,
                           fmt=""%(levelname)s %(message)-20s (datetime)s")
