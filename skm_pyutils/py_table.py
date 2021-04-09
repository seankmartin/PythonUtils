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
        headers = ["V{}".format(i) for i in range(len(in_list[0]))]

    if transpose:
        df = pd.DataFrame(in_list).T
        df.columns = headers
    else:
        df = pd.DataFrame.from_records(in_list, columns=headers)
    return df
