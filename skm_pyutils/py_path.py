"""Path related utility functions."""
import os
import re
import argparse
import shutil
from collections import OrderedDict

from skm_pyutils.py_config import parse_args


def make_path_if_not_exists(fname):
    """Make directory structure for given fname if it does not exist."""
    if os.path.dirname(fname) != "":
        os.makedirs(os.path.dirname(fname), exist_ok=True)


def make_dir_if_not_exists(dirname):
    """Make the directory dirname if it does not exist."""
    os.makedirs(dirname, exist_ok=True)


def has_ext(filename, ext, case_sensitive_ext=False):
    """
    Check if the filename ends in the extension.

    Parameters
    ----------
    filename : str
        The name of the file.
    ext : str
        The extension, may have leading dot (e.g txt == .txt).
    case_sensitive_ext: bool, optional. Defaults to False,
        Whether to match the case of the file extension.

    Returns
    -------
    bool
        Indicates if the filename has the extension

    """
    if ext is None:
        return True
    if ext[0] != ".":
        ext = "." + ext
    if case_sensitive_ext:
        return filename[-len(ext) :] == ext
    else:
        return filename[-len(ext) :].lower() == ext.lower()


def get_all_files_in_dir(
    in_dir,
    ext=None,
    return_absolute=True,
    recursive=False,
    verbose=False,
    re_filter=None,
    case_sensitive_ext=False,
):
    """
    Get all files in the directory with the given extensions.

    Parameters
    ----------
    in_dir : str
        The absolute path to the directory
    ext : str, optional. Defaults to None.
        The extension of files to get.
    return_absolute : bool, optional. Defaults to True.
        Whether to return the absolute filename or not.
    recursive: bool, optional. Defaults to False.
        Whether to recurse through directories.
    verbose: bool, optional. Defaults to False.
        Whether to print the files found.
    re_filter: str, optional. Defaults to None
        a regular expression used to filter the results
    case_sensitive_ext: bool, optional. Defaults to False,
        Whether to match the case of the file extension

    Returns
    -------
    List
        A list of filenames with the given parameters.

    """
    if not os.path.isdir(in_dir):
        raise ValueError("Non existant directory " + str(in_dir))

    def match_filter(f):
        if re_filter is None:
            return True
        search_res = re.search(re_filter, f)
        return search_res is not None

    def ok_file(root_dir, f):
        return (
            has_ext(f, ext, case_sensitive_ext=case_sensitive_ext)
            and os.path.isfile(os.path.join(root_dir, f))
            and match_filter(f)
        )

    def convert_to_path(root_dir, f):
        return os.path.abspath(os.path.join(root_dir, f)) if return_absolute else f

    if verbose:
        print("Adding following files from {}".format(in_dir))

    if recursive:
        onlyfiles = []
        for root, _, filenames in os.walk(in_dir):
            start_root = root[: len(in_dir)]

            if len(root) == len(start_root):
                end_root = ""
            else:
                if in_dir.endswith(os.sep):
                    end_root = root[len(in_dir) :]
                else:
                    end_root = root[len(in_dir + os.sep) :]
            for filename in filenames:
                filename = os.path.join(end_root, filename)
                if ok_file(start_root, filename):
                    to_add = convert_to_path(start_root, filename)
                    if verbose:
                        print(to_add)
                    onlyfiles.append(to_add)

    else:
        onlyfiles = [
            convert_to_path(in_dir, f)
            for f in sorted(os.listdir(in_dir))
            if ok_file(in_dir, f)
        ]
        if verbose:
            for f in onlyfiles:
                print(f)

    if verbose:
        print()
    return onlyfiles


def get_dirs_matching_regex(start_dir, re_filters=None, return_absolute=True):
    """
    Recursively get all directories from start_dir that match regex.

    Parameters
    ----------
    start_dir : str
        The path to the directory to start at.
    re_filter : list of str, optional. Defaults to None.
        The list of regular expressions to match.
        Returns all directories if passed as None.

    Returns
    -------
    list
        A list of directories matching the regex.

    """
    if not os.path.isdir(start_dir):
        raise ValueError("Non existant directory " + str(start_dir))

    def match_filter(f):
        if re_filters is None:
            return True
        for re_filter in re_filters:
            search_res = re.search(re_filter, f.replace(os.sep, "/"))
            if search_res is None:
                return False
        return True

    dirs = []
    for root, _, _ in os.walk(start_dir):
        start_root = root[: len(start_dir)]

        if len(root) == len(start_root):
            end_root = ""
        else:
            if start_dir.endswith(os.sep):
                end_root = root[len(start_dir) :]
            else:
                end_root = root[len(start_dir + os.sep) :]

        if match_filter(end_root):
            to_add = root if return_absolute else end_root
            dirs.append(to_add)
    return dirs


def get_base_dir_to_files(
    filenames, start_dir, ext=None, re_filter=None, print_info=True
):
    """
    Get the base directory of a set of filenames.

    If multiple matches are found, returns all matching filenames.

    Parameters
    ----------
    filenames : list of str
        The filenames to search for.
    start_dir : str
        Where to start the search.
    ext : str, optional
        The extension of the filenames, by default None.
    re_filter : str, optional. 
        A regex to use to find files, by defaults None.
    print_info : bool, optional
        Whether to print info of the search, by default True.

    Returns
    -------
    OrderedDict
        Dictionary of matching file base paths.
    set
        A set of files with no matches
    set
        A set of files with multiple matches
    """
    filenames = list(filenames)
    files_to_check = get_all_files_in_dir(
        start_dir, ext=ext, re_filter=re_filter, recursive=True
    )
    found_dict = OrderedDict()

    for f in files_to_check:
        base = os.path.basename(f)
        dirs = os.path.dirname(f)
        if base in filenames:
            if base not in found_dict.keys():
                found_dict[base] = []
            found_dict[base].append(dirs)

    no_match = []
    multi_match = []
    found = list(found_dict.keys())
    num_found = 0
    for v in filenames:
        if v not in found:
            no_match.append(v)
        else:
            num_found += 1
            if len(found_dict[v]) > 1:
                multi_match.append(v)

    found_dict = OrderedDict(
        sorted(found_dict.items(), key=lambda x: filenames.index(x[0]))
    )

    if print_info:
        to_print = "Found {} files out of {}, {} have multiple matches".format(
            num_found, len(filenames), len(set(multi_match))
        )
        print(to_print)

    return found_dict, set(no_match), set(multi_match)


def cli_entry():
    """Command line interface entry point."""
    parser = argparse.ArgumentParser(description="Directory list command line")

    parser.add_argument(
        "directory", type=str, help="Directory to find files from.",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Whether to recurse into subdirectories.",
    )
    parser.add_argument(
        "--extension", "-e", type=str, default=None, help="Extension to look for."
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None, help="Name of output txt file."
    )

    parsed = parse_args(parser, verbose=False)

    if os.path.exists(parsed.directory):
        files = get_all_files_in_dir(
            parsed.directory,
            ext=parsed.extension,
            return_absolute=False,
            recursive=parsed.recursive,
        )
        output = (
            parsed.output
            if parsed.output is not None
            else os.path.join(parsed.directory, "current_contents.txt")
        )
        with open(output, "w") as f:
            for fname in files:
                f.write(f"{fname}\n")
    else:
        raise ValueError("Please pass a valid directory")


def cli_copy_files_in_dir():
    parser = argparse.ArgumentParser(description="Directory list command line")

    parser.add_argument(
        "input_directory", type=str, help="Directory to find files from.",
    )
    parser.add_argument(
        "output_directory", type=str, help="Directory to copy files to."
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Whether to recurse into subdirectories.",
    )
    parser.add_argument(
        "--extension", "-e", type=str, default=None, help="Extension to look for."
    )
    parser.add_argument(
        "--regular_expression",
        "-re",
        type=str,
        default=None,
        help="Regular expression to filter files by.",
    )
    parser.add_argument(
        "--move", "-mv", action="store_true", help="Move files instead of copying them."
    )
    parser.add_argument(
        "--dummy",
        "-d",
        action="store_true",
        help="Dummy run, only print files that would be copied.",
    )

    parsed = parse_args(parser, verbose=False)

    if os.path.exists(parsed.input_directory):
        files = get_all_files_in_dir(
            parsed.input_directory,
            ext=parsed.extension,
            return_absolute=False,
            recursive=parsed.recursive,
            re_filter=parsed.regular_expression,
        )
        if parsed.dummy:
            name = "move" if parsed.move else "copy"
            print(f"Would {name} these files to {parsed.output_directory}:")
            for f in files:
                print(f)
            return

        os.makedirs(parsed.output_directory, exist_ok=True)
        for fname in files:
            output_loc = os.path.join(parsed.output_directory, fname)
            input_loc = os.path.join(parsed.input_directory, fname)
            if parsed.move:
                shutil.move(input_loc, output_loc)
            else:
                shutil.copy(input_loc, output_loc)
    else:
        raise ValueError("Please pass a valid directory")


if __name__ == "__main__":
    # cli_entry()
    cli_copy_files_in_dir()
