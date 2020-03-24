"""Path related utility functions."""
import os
import re


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
        return filename[-len(ext):] == ext
    else:
        return filename[-len(ext):].lower() == ext.lower()


def get_all_files_in_dir(
        in_dir, ext=None, return_absolute=True,
        recursive=False, verbose=False, re_filter=None,
        case_sensitive_ext=False):
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
            has_ext(f, ext, case_sensitive_ext=case_sensitive_ext) and
            os.path.isfile(os.path.join(root_dir, f)) and match_filter(f))

    def convert_to_path(root_dir, f):
        return os.path.join(root_dir, f) if return_absolute else f

    if verbose:
        print("Adding following files from {}".format(in_dir))

    if recursive:
        onlyfiles = []
        for root, _, filenames in os.walk(in_dir):
            start_root = root[:len(in_dir)]

            if len(root) == len(start_root):
                end_root = ""
            else:
                end_root = root[len(in_dir + os.sep):]
            for filename in filenames:
                filename = os.path.join(end_root, filename)
                if ok_file(start_root, filename):
                    to_add = convert_to_path(start_root, filename)
                    if verbose:
                        print(to_add)
                    onlyfiles.append(to_add)

    else:
        onlyfiles = [
            convert_to_path(in_dir, f) for f in sorted(os.listdir(in_dir))
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
    re_filter : str, optional. Defaults to None.
        The regular expression to match.
        Returns all directories is passed as None.

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
            search_res = re.search(re_filter, f)
            if search_res is None:
                return False
        return True

    dirs = []
    for root, _, _ in os.walk(start_dir):
        start_root = root[:len(start_dir)]

        if len(root) == len(start_root):
            end_root = ""
        else:
            end_root = root[len(start_dir + os.sep):]

        if match_filter(end_root):
            to_add = root if return_absolute else end_root
            dirs.append(to_add)
    return dirs
