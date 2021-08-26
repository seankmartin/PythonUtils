"""Utilities for saving structures to disk."""
import os
import csv

import numpy as np

from skm_pyutils.py_path import make_path_if_not_exists
from skm_pyutils.py_log import log_exception

def val_to_str(val):
    if isinstance(val, str):
        out_str = val.replace(" ", "_")
    elif isinstance(val, float):
        out_str = "{:4f}".format(val)
    elif isinstance(val, int):
        out_str = str(val)
    else:
        str_val = str(val).replace("\n", " ").replace(",", "")
        out_str = '"{}"'.format(str_val)
    return out_str

def arr_to_str(name, arr):
    out_str = name
    for val in arr:
        str_val = val_to_str(val)
        out_str = "{}, {}".format(out_str, str_val)

    return out_str


def save_mixed_dict_to_csv(in_dict, out_dir, out_name="results.csv", save=True):
    """
    Save a dictionary with mixed value types to a csv.

    Currently dict, np.ndarray, and list are supported values.
    Each key in the dictionary is saved as a row in the output csv.

    Args:
        in_dict (dict): The dictionary to save to a csv.
        out_dir (str): The directory to save the csv to.
        out_name (str, optional): Defaults to "results.csv".
        save (bool, optional): Defaults to True.

    Returns:
        The string representation of the data saved to csv.

    """
    full_str = ""
    if save:
        out_loc = os.path.join(out_dir, out_name)
        make_path_if_not_exists(out_loc)
        print("Saving mixed dict data to {}".format(out_loc))
        f = open(out_loc, "w")

    for key, val in in_dict.items():
        if isinstance(val, dict):
            out_str = ""
            for k2, val2 in val.items():
                name = "{} -- {}".format(key, k2)
                out_str += arr_to_str(name, val2) + "\n"
            out_str = out_str[:-1]
        elif isinstance(val, np.ndarray):
            out_str = arr_to_str(key, val.flatten())
        elif isinstance(val, list):
            out_str = arr_to_str(key, val)
        else:
            out_str = "{},{}".format(key, val_to_str(val))
        full_str += out_str + "\n"
        if save:
            f.write(out_str + "\n")
    
    if save:
        f.close()

    return full_str


def save_dicts_to_csv(filename, in_dicts, do_sort=True):
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
    do_sort : bool, optional
        Whether to sort the keys after appending, by default True.

    Returns
    -------
    None

    """
    # first, find the dict with the most keys
    if len(in_dicts) == 0:
        return
    max_key = list(in_dicts[0].keys())
    for in_dict in in_dicts:
        names = in_dict.keys()
        if len(names) > len(max_key):
            max_key = list(names)

    # Then append other keys if still missing keys
    did_append = False
    for in_dict in in_dicts:
        names = in_dict.keys()
        for name in names:
            if name not in max_key:
                did_append = True
                max_key.append(name)
    if did_append and do_sort:
        max_key = sorted(max_key)
    max_key_friendly = [k.replace(" ", "_") for k in max_key]

    try:
        print("Saving summary data to {}".format(filename))
        make_path_if_not_exists(filename)
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=max_key)
            writer.writerow(dict(zip(max_key, max_key_friendly)))
            for in_dict in in_dicts:
                writer.writerow(in_dict)

    except Exception as e:
        log_exception(e, "When {} saving to csv".format(filename))
