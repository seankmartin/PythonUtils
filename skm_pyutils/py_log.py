"""
Logging related functions.
"""
import datetime
import logging
import traceback
import os
import sys

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


def setup_text_logging(in_dir, bname="logfile.log", append=False):
    """
    Pass logging file location to logging.

    Parameters
    ----------
    in_dir : str
        Directory to save log file to.
    bname : str, optional, defaults to "logfile.log"
        The basename of the log file to save to.
    append: bool, optional, defaults to False

    Returns
    -------
    None

    """
    fname = os.path.join(in_dir, bname)
    if not append:
        if os.path.isfile(fname):
            open(fname, "w").close()
    logging.basicConfig(filename=fname, level=logging.DEBUG)
    mpl_logger = logging.getLogger("matplotlib")
    mpl_logger.setLevel(level=logging.WARNING)
