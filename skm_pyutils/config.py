"""Config file and logging related utility functions."""
import configparser
import json
import os
import sys
from pprint import pprint

import yaml


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
    if not os.path.exists(location):
        raise ValueError(f"Config file {location} does not exist")

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
            "Unrecognised command line arguments passed {}".format(unparsed)
        )

    if verbose:
        if len(sys.argv) > 1:
            print("Command line arguments", args)
    return args


def read_python(path, dirname_replacement=""):
    """
    Execute a python script at path.

    The script is expected to have items visible at global scope,
    which are stored as metadata.

    Note
    ----
    The string "__thisdirname__" is magic and will be replaced by the
    absolute path to the directory containing the script.
    The string "__dirname__" is also magic and will be replaced by
    the value of dirname_replacement.

    Parameters
    ----------
    path : string
        The location of the python script.
    dirname_replacement : string, optional, optional, defaults to None
        What to replace __dirname__ with.
        By default, None will replace __dirname__ with dirname of path.

    Returns
    -------
    dict
        The scripts global scope variables stored in a dictionary.

    """

    def normalise_path(pth):
        s = os.path.abspath(pth)
        s = s.replace(os.sep, "/")
        return s

    path = os.path.realpath(os.path.expanduser(path))
    if not os.path.exists(path):
        raise ValueError("{} does not exist to read".format(path))
    with open(path, "r") as f:
        contents = f.read()
    if dirname_replacement != "":
        contents = contents.replace("__dirname__", normalise_path(dirname_replacement))
    else:
        contents = contents.replace(
            "__dirname__", normalise_path(os.path.dirname(path))
        )
    contents = contents.replace(
        "__thisdirname__", normalise_path(os.path.dirname(path))
    )
    metadata = {}
    try:
        exec(contents, {}, metadata)
    except Exception as e:
        import traceback
        print("QUITTING: An error occurred reading {}".format(path))
        traceback.print_exc()
        exit(-1)
    metadata = {k.lower(): v for (k, v) in metadata.items()}
    return metadata

def read_yaml(path):
    with open(path, 'r') as stream:
        parsed_yaml=yaml.safe_load(stream)
    return parsed_yaml


def read_json(path):
    with open(path, 'r') as stream:
        parsed_json = json.load(stream)
    return parsed_json

def split_dict(in_dict, index):
    """
    Grab the value at index from each list in the dictionary.

    Parameters
    ----------
    in_dict : dict
        The dictionary to grab from
    index : int
        The index in the lists to pull from

    Returns
    -------
    dict
        The original dictionary but with index values pulled out.

    """
    new_dict = {}
    for key, value in in_dict.items():
        if isinstance(value, list):
            new_dict[key] = value[index]
    return new_dict
