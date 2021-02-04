import pandas as pd


def list_to_df(in_list, headers=None):
    """Convert a list to a dataframe with the given headers."""
    if headers is None:
        headers = ["V{}".format(i) for i in range(len(in_list[0]))]
    results_df = pd.DataFrame.from_records(in_list, columns=headers)
    return results_df
