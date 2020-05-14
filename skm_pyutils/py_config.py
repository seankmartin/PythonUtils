"""Config file and logging related utility functions."""
import os
import sys
import logging
import configparser
from pprint import pprint
import argparse


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
            open(fname, 'w').close()
    logging.basicConfig(
        filename=fname, level=logging.DEBUG)
    mpl_logger = logging.getLogger("matplotlib")
    mpl_logger.setLevel(level=logging.WARNING)


def read_cfg(location, verbose=True):
    """
    Read config file at location using ConfigParser.

    Parameters
    ----------
    location : str
        Where the config file is located
    verbose : bool, optional, defaults to True
        Should print the contents of the read config file.

    Returns
    -------
    ConfigParser
        The python ConfigParser object after reading the cfg.

    """
    config = configparser.ConfigParser()
    config.read(location)

    if verbose:
        print_cfg(config, "Program started with configuration")
    return config


def print_cfg(config, msg=""):
    """
    Print the contents of a ConfigParser object.

    Parameters
    ----------
    config : ConfigParser
        The ConfigParser to print the contents of.
    msg: str, optional, defaults to ""
        Message to print before printing the config file.

    Returns
    -------
    None

    """
    if msg != "":
        print(msg)
    config_dict = [{x: tuple(config.items(x))} for x in config.sections()]
    pprint(config_dict, width=120)


def parse_args(parser, verbose=True):
    """
    Parse command line arguments into a Namespace.

    Parameters
    ----------
    verbose : bool, optional, defaults to True
        Should print the values of the command line args.

    Returns
    -------
    Namespace
        Parsed arguments.

    Raises
    ------
    ValueError
        If any arguments are passed which are not used in program.

    """
    args, unparsed = parser.parse_known_args()

    if len(unparsed) != 0:
        raise ValueError(
            "Unrecognised command line arguments passed {}".format(
                unparsed))

    if verbose:
        if len(sys.argv) > 1:
            print("Command line arguments", args)
    return args


def log_exception(ex, more_info=""):
    """
    Log an expection and additional info.

    Parameters
    ----------
    ex: Exception
        The python exception that occured
    more_info:
        Additional string to log

    Returns
    -------
    None

    """
    template = "{0} because exception of type {1} occurred. Arguments:\n{2!r}"
    message = template.format(more_info, type(ex).__name__, ex.args)
    logging.error(message)


def read_python(path):
    path = os.path.realpath(os.path.expanduser(path))
    if not os.path.exists(path):
        raise ValueError("{} does not exist to read".format(path))
    with open(path, 'r') as f:
        contents = f.read()
    metadata = {}
    exec(contents, {}, metadata)
    metadata = {k.lower(): v for (k, v) in metadata.items()}
    return metadata


def split_dict(in_dict, index):
    new_dict = {}
    for key, value in in_dict.items():
        if isinstance(value, list):
            new_dict[key] = value[index]
    return new_dict
