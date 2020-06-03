"""
This module handles printing items such as dicts.

One could alternatively use pprint for some of these.
"""
from pprint import pformat


def walk_dict(d, depth=0):
    """Walk a Dictionary."""
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        spaces = ("  ") * depth
        if hasattr(v, "items"):
            print(spaces + ("%s" % k))
            walk_dict(v, depth + 1)
        else:
            print(spaces + "%s %s" % (k, v))


def print_attrs(d, depth=0):
    """Walk through attributes and print them."""
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        spaces = ("  ") * depth
        spaces2 = ("  ") * (depth + 1)
        if len(v.attrs) != 0:
            print("{}{} has attrs:".format(spaces, k))
            for key, val in v.attrs.items():
                print("{}{} {}".format(spaces2, key, val))
        if hasattr(v, "items"):
            print(spaces + ("%s" % k))
            print_attrs(v, depth=depth + 1)


def print_h5(file_location):
    """Print a summary of a h5 file."""
    import h5py
    with h5py.File(file_location, 'r', libver='latest') as f:
        print("--------AVAILABLE METADATA--------")
        for key, val in f.attrs.items():
            print(key, val)
        print_attrs(f)
        print("\n--------AVAILABLE INFO--------")
        walk_dict(f)
        print()
