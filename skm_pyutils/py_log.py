"""
Logging related functions.
"""
import datetime
import logging
import os
import sys
import traceback

import psutil

from skm_pyutils.py_path import make_path_if_not_exists


def log_exception(ex, more_info="", location=None):
    """
    Log an expection to file and additional info.

    Parameters
    ----------
    ex : Exception
        The python exception that occurred
    more_info : str, optional
        Additional string to log, default is ""
    location : str, optional
        Where to store the log, default is
        home/.skm_python/caught_errors.txt

    Returns
    -------
    None

    """
    if location is None:
        default_loc = get_default_log_loc("caught_errors.txt")
    else:
        default_loc = location

    now = datetime.datetime.now()
    make_path_if_not_exists(default_loc)
    with open(default_loc, "a+") as f:
        f.write("\n----------Caught Exception at {}----------\n".format(now))
        traceback.print_exc(file=f)
    logging.error(
        "{} failed with caught exception.\nSee {} for more information.".format(
            more_info, default_loc
        ),
        exc_info=False,
    )


def default_excepthook(exc_type, exc_value, exc_traceback):
    """Any uncaught exceptions will be logged from here."""
    default_loc = get_default_log_loc("uncaught_errors.txt")

    file_logger = logging.getLogger(__name__)
    file_logger.propagate = False
    handler = logging.FileHandler(default_loc)
    file_logger.addHandler(handler)

    # Don't catch CTRL+C exceptions
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    now = datetime.datetime.now()
    file_logger.critical(
        "\n----------Uncaught Exception at {}----------".format(now),
        exc_info=(exc_type, exc_value, exc_traceback),
    )

    print("\nA fatal error occurred in this Python program")
    print(
        "The error info was: {}".format(
            "".join(
                traceback.format_exception(exc_type, exc_value, exc_traceback)
            ).strip()
        )
    )
    print("Please report this to {} and provide the file {}".format("us", default_loc))

    sys.exit(-1)


def override_excepthook(excepthook=None):
    """
    Change sys.excepthook behaviour.
    
    Parameters
    ----------
    excepthook : function, optional
        This is what sys.excepthook will be overridden by.
        See https://docs.python.org/3/library/sys.html#sys.excepthook
        for the function specification.
        If None is passed, uses the default excepthook in this module.
    
    Returns
    -------
    None

    """
    if excepthook is None:
        excepthook = default_excepthook
    sys.excepthook = excepthook


def get_default_log_loc(name):
    default_loc = os.path.join(os.path.expanduser("~"), ".skm_python", name)

    return default_loc


def setup_text_logging(
    in_dir, loglevel, bname="logfile.log", append=False, logname=None
):
    """
    Pass logging file location to logging.

    Parameters
    ----------
    in_dir : str
        Directory to save log file to. Can be None to use bname directly.
    loglevel : str
        The name of the log level to use, e.g. "debug" or 10
    bname : str, optional, defaults to "logfile.log"
        The basename of the log file to save to.
    append: bool, optional, defaults to False
    logname : str, optional, defaults to None
        If provided, creates this logger. Otherwise uses the root logger.

    Returns
    -------
    None

    """
    try:
        numeric_level = int(loglevel)
    except BaseException:
        numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % loglevel)

    if in_dir is None:
        fname = bname
    else:
        fname = os.path.join(in_dir, bname)
    if not append:
        if os.path.isfile(fname):
            open(fname, "w").close()

    root = logging.getLogger(logname)
    root.setLevel(numeric_level)
    file_handler = logging.FileHandler(fname)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(levelname)s: %(asctime)s %(message)s",
            datefmt="%d/%m/%Y %I:%M:%S %p",
        )
    )
    root.addHandler(file_handler)
    # Encoding only supported in 3.9+
    # logging.basicConfig(
    #     filename=fname,
    #     # encoding="utf-8",
    #     level=numeric_level,
    #     format="%(levelname)s: %(asctime)s %(message)s",
    #     datefmt="%d/%m/%Y %I:%M:%S %p",
    # )
    mpl_logger = logging.getLogger("matplotlib")
    mpl_logger.setLevel(level=logging.WARNING)

    # print("See {} for {} level logs".format(fname, loglevel))


class FileStdoutLogger:
    """A logger that prints to stdout and to a file."""

    def __init__(self, name="stdout_logger"):
        self.name = name
        self.logger = None
        self.create_logger()

    def init_logging(self):
        self.logger.setLevel(logging.INFO)
        out_loc = self.get_default_log_location()
        output_file_handler = logging.FileHandler(out_loc)
        stdout_handler = logging.StreamHandler(sys.stdout)

        self.logger.addHandler(output_file_handler)
        self.logger.addHandler(stdout_handler)

    def create_logger(self):
        if self.logger is None:
            self.logger = logging.getLogger(self.name)
        if len(self.get_handlers()) == 0:
            self.init_logging()

    def print(self, msg):
        self.logger.info(msg)

    def get_default_log_location(self):
        home = os.path.expanduser("~")
        out_loc = os.path.join(home, ".skm_python", f"{self.name}.log")
        os.makedirs(os.path.dirname(out_loc), exist_ok=True)

        return out_loc

    def read_log_file(self):
        loc = self.get_default_log_location()
        if os.path.exists(loc):
            with open(loc, "r") as f:
                out = f.read().strip()
            return out
        else:
            return "No log file exists."

    def clear_log_file(self):
        # handlers = self.logger.handlers[:]
        # for handler in handlers:
        #     handler.close()
        #     self.logger.removeHandler(handler)

        loc = self.get_default_log_location()
        if os.path.exists(loc):
            open(loc, "w").close()

    def get_handlers(self):
        return self.logger.handlers[:]


class FileLogger:
    """A logger that prints to a file."""

    def __init__(self, name="main", level="warning"):
        self.name = name
        self.logger = None
        self.level = level
        self.create_logger()

    def init_logging(self):
        out_loc = self.get_default_log_location()
        setup_text_logging(None, self.level, out_loc, append=True, logname=self.name)

    def create_logger(self):
        if self.logger is None:
            self.logger = logging.getLogger(self.name)
        if len(self.get_handlers()) == 0:
            self.init_logging()

    def info(self, msg, **kwargs):
        self.logger.info(msg, **kwargs)

    def warning(self, msg, **kwargs):
        self.logger.warning(msg, **kwargs)

    def error(self, msg, **kwargs):
        self.logger.error(msg, **kwargs)

    def critical(self, msg, **kwargs):
        self.logger.critical(msg, **kwargs)

    def debug(self, msg, **kwargs):
        self.logger.debug(msg, **kwargs)

    def set_level(self, loglevel):
        try:
            numeric_level = int(loglevel)
        except BaseException:
            numeric_level = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError("Invalid log level: %s" % loglevel)

        self.logger.setLevel(numeric_level)
        filename = self.get_default_log_location()
        print("See {} for {} level logs".format(filename, loglevel))

    def get_default_log_location(self):
        home = os.path.expanduser("~")
        out_loc = os.path.join(home, ".skm_python", f"{self.name}.log")
        os.makedirs(os.path.dirname(out_loc), exist_ok=True)

        return out_loc

    def read_log_file(self):
        loc = self.get_default_log_location()
        if os.path.exists(loc):
            with open(loc, "r") as f:
                out = f.read().strip()
            return out
        else:
            return "No log file exists."

    def clear_log_file(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

        loc = self.get_default_log_location()
        if os.path.exists(loc):
            os.remove(loc)

    def get_handlers(self):
        return self.logger.handlers[:]


def print_memory_usage(as_string=False) -> str:
    """
    Print memory usage information
    
    Parameters
    ----------
    as_string : bool, optional
        Just return the string representation, don't print.
        By default, False.
    
    Returns
    -------
    usage : str
        String about memory usage
    """
    str_ = f"RAM memory usage stats: {psutil.virtual_memory()}"
    if not as_string:
        print(str_)
    return str_
