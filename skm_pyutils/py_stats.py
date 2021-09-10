"""Statistics functions and paper reporting."""

import numpy as np
import pingouin

from skm_pyutils.py_plot import UnicodeGrabber


def corr(x, y, fmt_kwargs, **kwargs):
    """
    Compute correlation between x and y.

    Also returns a formatted string representation.

    Parameters
    ----------
    x : array_like
        First set of observations.
    y: array_like
        Second set of observations.
    fmt_kwargs : dict
        A dictionary of kwargs to control the formatting.
        value - the name of the values being tested
        unit - the unit of the values being tested
        group1 - the name of x
        group2 - the name of y
        signif - the significance level (float)
        n_decimals - the number of decimal places to print (int)
        n_pdecimals - the number of decimal places to print for p (int)
        show_quartiles - include quartiles in report (bool)
        do_print - print the report string (bool)
    **kwargs : keyword arguments
        These are passed to pingouin.corr

    Returns
    -------
    pd.DataFrame
        The dataframe of results
    str
        A string to describe the test result for reporting

    See also
    --------
    pinouin.corr

    """
    vname = fmt_kwargs.get("value", "values")
    unit_name = fmt_kwargs.get("unit", "")
    if unit_name != "":
        unit_name = " " + unit_name + ", "
    else:
        unit_name = ", "
    group1_name = fmt_kwargs.get("group1", "1")
    group2_name = fmt_kwargs.get("group2", "2")
    signif_level = fmt_kwargs.get("signif", 0.05)
    n_decimals = fmt_kwargs.get("n_decimals", 2)
    n_pdecimals = fmt_kwargs.get("n_pdecimals", 3)
    show_quartiles = fmt_kwargs.get("show_quartiles", True)
    do_print = fmt_kwargs.get("do_print", True)

    sided = kwargs.get("alternative", "two-sided")
    method = kwargs.get("method", "pearson")

    results_df = pingouin.corr(x, y, **kwargs)

    n = results_df["n"].values[0]
    r = np.round(results_df["r"].values[0], n_decimals)
    P = np.round(results_df["p-val"].values[0], n_pdecimals)
    power = np.round(results_df["power"].values[0], n_decimals)
    ci = np.round(np.array(results_df["CI95%"].values[0]), n_decimals)

    if method == "pearson":
        co_eff_name = "r"
        corr_name = "Pearson"
    elif method == "spearman":
        co_eff_name = "\u03A1"
        corr_name = "spearman"
    elif method == "kendall":
        co_eff_name = "\u03A4"
        corr_name = "Kendall"

    if r < 0:
        type_corr = "negative"
    if r == 0:
        type_corr = "no"
    if r > 0:
        type_corr = "positive"

    if sided == "two-sided":
        tailed = "(two-tailed)."
    else:
        tailed = "(one-tailed)."

    if P < signif_level:
        differ_str = "was significant"
    else:
        differ_str = "was not significant"

    if show_quartiles:
        result_str = (
            f"There was a {type_corr} {corr_name} correlation of {co_eff_name} = {r} [{ci[0]}, {ci[1]}] 95% CI"
        )
    else:
        result_str = (
            f"There was a {type_corr} {corr_name} correlation of {co_eff_name} = {r}"
        )
    relation_str = f" between {group1_name} and {group2_name} {vname}"
    stats_str = f"; this {differ_str} with \u0070 = {P}, N = {n} and test power of {power} {tailed}"

    final_str = result_str + relation_str + stats_str

    if do_print:
        print(final_str)

    return results_df, final_str


def mwu(x, y, fmt_kwargs, **kwargs):
    """
    Compute the Mann-Whitney U Test.

    Also returns a formatted string for paper reporting.

    Parameters
    ----------
    x : array_like
        First set of observations.
    y: array_like
        Second set of observations.
    fmt_kwargs : dict
        A dictionary of kwargs to control the formatting.
        value - the name of the values being tested
        unit - the unit of the values being tested
        group1 - the name of x
        group2 - the name of y
        signif - the significance level (float)
        n_decimals - the number of decimal places to print (int)
        n_pdecimals - the number of decimal places to print for p (int)
        show_quartiles - include quartiles in report (bool)
        do_print - print the report string (bool)
    **kwargs : keyword arguments
        These are passed to pingouin.mwu which then passes to scipy.stats.mannwhitneyu

    Returns
    -------
    pd.DataFrame
        The dataframe of results
    str
        A string to describe the test result for reporting

    See also
    --------
    pinouin.mwu
    scipy.stats.mannwhitneyu

    """
    vname = fmt_kwargs.get("value", "values")
    unit_name = fmt_kwargs.get("unit", "")
    if unit_name != "":
        unit_name = " " + unit_name + ", "
    else:
        unit_name = ", "
    group1_name = fmt_kwargs.get("group1", "1")
    group2_name = fmt_kwargs.get("group2", "2")
    signif_level = fmt_kwargs.get("signif", 0.05)
    n_decimals = fmt_kwargs.get("n_decimals", 2)
    n_pdecimals = fmt_kwargs.get("n_pdecimals", 3)
    show_quartiles = fmt_kwargs.get("show_quartiles", True)
    do_print = fmt_kwargs.get("do_print", True)

    sided = kwargs.get("alternative", "two-sided")

    results_df = pingouin.mwu(x, y, **kwargs)
    U = results_df["U-val"].values[0]
    P = np.round(results_df["p-val"].values[0], n_pdecimals)
    cl = np.round(results_df["CLES"].values[0], n_decimals)
    median1 = np.round(np.median(x), n_decimals)
    lowerq1, higherq1 = np.round(np.percentile(x, [25, 75]), n_decimals)
    lowerq2, higherq2 = np.round(np.percentile(y, [25, 75]), n_decimals)
    median2 = np.round(np.median(y), n_decimals)

    sample_size1 = len(x)
    sample_size2 = len(y)
    n1 = "n" + UnicodeGrabber.to_sub(1)
    n2 = "n" + UnicodeGrabber.to_sub(2)
    if sample_size1 == sample_size2:
        sample_str = f"{n1} = {n2} = {sample_size1}"
    else:
        sample_str = f"{n1} = {sample_size1}, {n2} = {sample_size2}"

    stats_str = (
        "(Mann-Whitney "
        + "\u0055"
        + f" = {U}, CLES = {cl}, {sample_str}, "
        + "\u0070"
        + f" = {P}"
    )

    if sided == "two-sided":
        stats_str += " two-tailed)."
    else:
        stats_str += " one-tailed)."

    if P < signif_level:
        differ_str = "differed significantly"
    else:
        differ_str = "did not differ significantly"

    if show_quartiles:
        results_str = (
            f"Median [quartiles] {vname} in groups {group1_name} and {group2_name} were "
            + f"{median1} [{lowerq1}, {higherq1}] and {median2} [{lowerq2}, {higherq2}]"
            f"{unit_name}respectively; "
            f"the distributions in the two groups {differ_str} {stats_str}"
        )
    else:
        results_str = (
            f"Median {vname} in groups {group1_name} and {group2_name} were "
            + f"{median1} and {median2}"
            f"{unit_name}respectively; "
            f"the distributions in the two groups {differ_str} {stats_str}"
        )

    if do_print:
        print(results_str)

    return results_df, results_str
