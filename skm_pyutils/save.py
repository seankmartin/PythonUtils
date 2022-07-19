"""Utilities for saving structures to disk."""
import csv
import os
from typing import Union

import numpy as np

from skm_pyutils.log import log_exception
from skm_pyutils.path import make_path_if_not_exists


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
            if len(val) == 0:
                out_str = "{},Empty".format(key)
            else:
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


def data_dict_from_attr_list(
    input_item, attr_list: list, friendly_names: Union["list[str]", None] = None
):
    """
    From a list of attributes, return a dictionary.

    Each item in attr_list should be a tuple containing
    attributes, keys, or None.
    The elements of the tuple are then accessed iteratively, like
    item.tuple_el1.tuple_el2...
    If the element is an attribute, it is directly retrieved.
    If the element is a key in a dictionary, that is retrieved.
    If the element is None, it indicates a break.
    (This last option can be used to get functions without calling them,
    or to get a full dictionary instead of pulling out the key, value pairs.)

    The output also depends on what is retrieved, if a dictionary or a function.
    Functions are called with no arguments.
    Dictionaries have key value pairs, that are stored in the output dictionary.
    Both of these can be avoided by passing the last element of the tuple as None.

    As an example:
    item.results = {"addition": {"1 + 1": 2}}
    item.data.running_speed = [0.5, 1.4, 1.5]
    attr_list = [("results", "addition", None)]
    this_fn(attr_list) = {"results_addition": {"1 + 1" = 2}}
    attr_list = [("results", "addition"), ("data", "running_speed")]
    this_fn(attr_list) = {"1 + 1": 2, "data_running_speed": [0.5, 1.4, 1.5]}

    Parameters
    ----------
    input_item : Any
        The item to get data attributes from.
    attr_list : list
        The list of attributes to retrieve.
    friendly_names : list of str, optional
        What to name each retrieved attribute, (default None).
        Must be the same size as attr_list or None.

    Returns
    -------
    dict
        The retrieved attributes.

    Raises
    ------
    ValueError
        attr_list and friendly_names are not the same size.

    """
    if friendly_names is not None and len(friendly_names) != len(attr_list):
        raise ValueError("friendly_names and attr_list must be the same length")

    data_out = {}
    for i, attr_tuple in enumerate(attr_list):
        item = input_item
        for a in attr_tuple:
            if a is None:
                break
            item = (
                getattr(item, a) if isinstance(a, str) and hasattr(item, a) else item[a]
            )
            if callable(item):
                item = item()
        if isinstance(item, dict):
            for key, value in item.items():
                data_out[key] = value
        else:
            non_none_attrs = [x for x in attr_tuple if x is not None]
            if friendly_names is None:
                key = "_".join(non_none_attrs)
            else:
                key = friendly_names[i]
                if key is None:
                    key = "_".join(non_none_attrs)
            data_out[key] = item
    return data_out
