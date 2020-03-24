"""Utilities for saving structures to disk."""
import os
import csv

import numpy as np

from skm_pyutils.py_path import make_path_if_not_exists
from skm_pyutils.py_config import log_exception


def arr_to_str(name, arr):
    out_str = name
    for val in arr:
        if isinstance(val, str):
            val = val.replace(" ", "_")
            out_str = "{},{}".format(out_str, val)
        else:
            out_str = "{},{:4f}".format(out_str, val)
    return out_str


def save_mixed_dict_to_csv(in_dict, out_dir, out_name="results.csv"):
    """
    Save a dictionary with mixed value types to a csv.

    Currently dict, np.ndarray, and list are supported values.
    Each key in the dictionary is saved as a row in the output csv.

    Args:
        in_dict (dict): The dictionary to save to a csv.
        out_dir (str): The directory to save the csv to.
        out_name (str, optional): Defaults to "results.csv".

    Returns:
        None

    """
    out_loc = os.path.join(out_dir, out_name)
    make_path_if_not_exists(out_loc)
    print("Saving mixed dict data to {}".format(out_loc))
    with open(out_loc, "w") as f:
        for key, val in in_dict.items():
            if isinstance(val, dict):
                out_str = arr_to_str(key, val.values())
            elif isinstance(val, np.ndarray):
                out_str = arr_to_str(key, val.flatten())
            elif isinstance(val, list):
                out_str = arr_to_str(key, val)
            else:
                raise ValueError("Unrecognised type {} quitting".format(
                    type(val)))
            f.write(out_str + "\n")


def save_dicts_to_csv(filename, in_dicts):
    """
    Save a list of dictionaries to a csv, cols=vals, rows=dicts.

    The headers are set as the maximal set of keys in in_dicts.
    It is assumed that all other dicts will have a subset of these keys.
    Each entry in the dict is saved to a row of the csv, so it is assumed
    the values in the dict are mostly floats / ints / etc.

    Parameters
    ----------
    filename : str
        The name of the csv file to save results to.
    in_dicts : List
        A list of dictionaries to save to csv.

    Returns
    -------
    None

    """
    # first, find the dict with the most keys
    max_key = in_dicts[0].keys()
    for in_dict in in_dicts:
        names = in_dict.keys()
        if len(names) > len(max_key):
            max_key = names

    # Then append other keys if still missing keys
    for in_dict in in_dicts:
        names = in_dict.keys()
        for name in names:
            if name not in max_key:
                max_key.append(name)
    max_key_friendly = [k.replace(" ", "_") for k in max_key]

    try:
        print("Saving summary data to {}".format(filename))
        make_path_if_not_exists(filename)
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=max_key)
            writer.writerow(dict(zip(max_key, max_key_friendly)))
            for in_dict in in_dicts:
                writer.writerow(in_dict)

    except Exception as e:
        log_exception(e, "When {} saving to csv".format(filename))
