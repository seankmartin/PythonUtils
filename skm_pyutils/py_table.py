"""Utilities for pandas dataframes."""
import os

import numpy as np
import pandas as pd


def list_to_df(in_list, transpose=False, headers=None):
    """
    Convert a list to a dataframe with the given headers.

    Tranpose handles the list shape.
    If transpose is False, list is assumed to be like
    [
        (row 1) [1_1, 1_2, ..., 1_N]
        ...
        (row M) [M_1, M_2, ..., M_N]
    ]
    Otherwise, the list is assumed to be like
    [
        (col 1) [1_1, 2_1, ..., M_1]
        ...
        (col N) [1_N, 2_N, ..., M_N]
    ]
    
    Parameters
    ----------
    in_list : list
        The list to convert.
    tranpose : bool, optional
        Whether to transpose the list, by default False.
    headers : list, optional
        A list of headers for the data. By default is V1, V2, ... VN.

    Returns
    -------
    pandas.DataFrame

    """
    if headers is None:
        if not transpose:
            headers = ["V{}".format(i) for i in range(len(in_list[0]))]
        else:
            headers = ["V{}".format(i) for i in range(len(in_list))]

    if transpose:
        df = pd.DataFrame(in_list).T
        df.columns = headers
    else:
        df = pd.DataFrame.from_records(in_list, columns=headers)
    return df


def df_from_file(filename):
    """
    Read a pandas.DataFrame from filename.

    Parameters
    ----------
    filename : str
        The path to the file to read

    Returns
    -------
    pandas.DataFrame or TextParser
        The read data

    """
    ext = os.path.splitext(filename)[1]
    if ext == ".psv":
        df = pd.read_csv(filename, delimiter="|")
    elif ext == ".csv":
        df = pd.read_csv(filename)
    elif ext == ".xlsx":
        df = pd.read_excel(filename)
    else:
        raise ValueError(f"Unsupported file extension {ext}")
    return df


def df_to_file(df, filename, index=False, **kwargs):
    """
    Save a pandas.DataFrame to filename.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe to save.
    filename : str
        The path of the file to save to.
    index : bool
        Whether to write row names, by default False.
    kwargs : keyword arguments
        Passed to pandas method.

    Returns
    -------
    None

    """

    def get_to_retry():
        print("{} may currently be in use, try closing it".format(filename))
        retry = True
        continue_ = True
        while retry:
            done = input("When closed, please enter y to retry, or q to quit:\n")
            if len(done) == 0:
                retry = True
            elif done.strip().lower() == "y":
                retry = False
            elif done.strip().lower() == "q":
                retry = False
                continue_ = False
        if continue_:
            print("Retrying saving to {}".format(filename))
        return continue_

    ext = os.path.splitext(filename)[1]
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if ext == ".psv":
        try:
            df.to_csv(filename, sep="|", index=index, **kwargs)
        except PermissionError:
            continue_ = get_to_retry()
            if continue_:
                df.to_csv(filename, sep="|", index=index, **kwargs)
    elif ext == ".csv":
        try:
            df.to_csv(filename, sep=",", index=index, **kwargs)
        except PermissionError:
            continue_ = get_to_retry()
            if continue_:
                df.to_csv(filename, sep=",", index=index, **kwargs)
    elif ext == ".xlsx":
        try:
            df.to_excel(filename, index=index, **kwargs)
        except PermissionError:
            continue_ = get_to_retry()
            if continue_:
                df.to_excel(filename, index=index, **kwargs)
    else:
        raise ValueError(f"Unsupported file extension {ext}")


def df_subset_from_rows(df, rows):
    """
    Get a subset of a dataframe based on row indices.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to subset from.
    rows : list-like of int
        The rows to grab.
    
    Returns
    -------
    pandas.DataFrame

    """
    df_subset = df.iloc[rows].copy().reset_index()
    return df_subset


def show_interactive_table(table, notebook=False) -> None:
    import dtale

    ## TODO maybe should have a config for notebook version
    if notebook:
        dtale.show(table)
    else:
        dtale.show(table).open_browser()


def filter_table(table: "pd.DataFrame", filter_dict: "dict[str, list]", and_: "bool" = True) -> "pd.DataFrame":
    """
    Filter a table based on a dictionary with possible values.
    
    Parameters
    ----------
    table: pd.DataFrame
        The table to filter
    filter_dict: dict[str, list]
        The dictionary to filter with.
        key = column in df, val = possible values for that column
    and_: bool, optional
        Whether to combine with logical_and or with logical_or,
        By default logical_and.
    
    Returns
    -------
    filtered_dataframe : pd.DataFrame
        The filtered_dataframe

    """
    filters = []
    for k, v in filter_dict.items():
        filters.append(table[k].isin(v))
    if and_:
        full_mask = np.logical_and.reduce(np.array(filters))
    else:
        full_mask = np.logical_or.reduce(np.array(filters))
    filtered_table = table[full_mask]
    return filtered_table
    