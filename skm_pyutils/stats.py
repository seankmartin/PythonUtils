"""Statistics functions and paper reporting."""

import matplotlib.pyplot as plt
import numpy as np
import pingouin
import seaborn as sns

from skm_pyutils.plot import UnicodeGrabber
from skm_pyutils.table import list_to_df


def plot_dists(x, y, ax=None, **fmt_kwargs):
    """Plot distrubtions of two arrays."""
    palette = fmt_kwargs.get("palette", "dark")
    context = fmt_kwargs.get("context", "paper")
    group1_name = fmt_kwargs.get("group1", "1")
    group2_name = fmt_kwargs.get("group2", "2")
    vname = fmt_kwargs.get("value", "values")
    sns.set_palette(palette)
    if context == "paper":
        sns.set_context(
            "paper", font_scale=1.4, rc={"lines.linewidth": 3.2},
        )
    else:
        sns.set_context(context)

    if ax is None:
        figure, ax = plt.subplots()
    else:
        figure = None
    despine = fmt_kwargs.get("despine", True)
    trim = fmt_kwargs.get("trim", True)
    offset = fmt_kwargs.get("offset", None)

    df_list = []
    for val in x:
        df_list.append([val, group1_name])
    for val in y:
        df_list.append([val, group2_name])

    df = list_to_df(df_list, headers=[vname, "group"])
    sns.kdeplot(data=df, x=vname, hue="group", multiple="stack", ax=ax)

    ax.set_xlabel(vname)
    if despine:
        sns.despine(offset=offset, trim=trim)

    return figure

def plot_corr(x, y, ax=None, **fmt_kwargs):
    """Plot correlation between two arrays."""
    value1_name = fmt_kwargs.get("value1", "1")
    value2_name = fmt_kwargs.get("value2", "2")
    palette = fmt_kwargs.get("palette", "dark")
    context = fmt_kwargs.get("context", "paper")
    sns.set_palette(palette)
    if context == "paper":
        sns.set_context(
            "paper", font_scale=1.4, rc={"lines.linewidth": 3.2},
        )
    else:
        sns.set_context(context)

    if ax is None:
        figure, ax = plt.subplots()
    else:
        figure = None
    despine = fmt_kwargs.get("despine", True)
    trim = fmt_kwargs.get("trim", True)
    offset = fmt_kwargs.get("offset", None)

    sns.regplot(x=x, y=y, ax=ax, truncate=False, order=1)

    extents_x = (0.97 * np.min(x), np.max(x) * 1.03)
    extents_y = (0.97 * np.min(y), np.max(y) * 1.03)

    ax.set_xlim(extents_x)
    ax.set_ylim(extents_y)
    ax.set_xlabel(value1_name)
    ax.set_ylabel(value2_name)
    if despine:
        sns.despine(offset=offset, trim=trim)

    return figure

def corr(x, y, fmt_kwargs=None, do_plot=False, ax=None, **kwargs):
    """
    Compute correlation between x and y.

    Based on the method passed as a keyword arg. By default Pearsons.
    Also returns a formatted string representation.

    Parameters
    ----------
    x : array_like
        First set of observations.
    y: array_like
        Second set of observations.
    fmt_kwargs : dict, optional
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
    do_plot : bool, optional
        Whether or not to plot the result.
    ax : axes object, optional
        An axes to plot into.
    **kwargs : keyword arguments
        These are passed to pingouin.corr
        Of particular is method - the correlation to run.

    Returns
    -------
    dict with keys:
        "results" : pd.DataFrame
            The dataframe of results
        "output" : str
            A string to describe the test result for reporting
        "figure" : matplotlib.pyplot.figure or None
            The returned figure plotted into.

    See also
    --------
    pinouin.corr

    """
    if fmt_kwargs is None:
        fmt_kwargs = {}
    group = fmt_kwargs.get("group", "")
    if group != "":
        group = " " + group
    unit_name = fmt_kwargs.get("unit", "")
    if unit_name != "":
        unit_name = " " + unit_name + ", "
    else:
        unit_name = ", "
    value1_name = fmt_kwargs.get("value1", "1")
    value2_name = fmt_kwargs.get("value2", "2")
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

    lin_reg_df = pingouin.linear_regression(x, y, as_dataframe=False)
    lm_adjr2 = np.round(lin_reg_df["adj_r2"], n_decimals)

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
        tailed = "(two-tailed)"
    else:
        tailed = "(one-tailed)"

    if P < signif_level:
        differ_str = "was significant"
    else:
        differ_str = "was not significant"

    if show_quartiles:
        result_str = f"There was a {type_corr} {corr_name} correlation of {co_eff_name} = {r} [{ci[0]}, {ci[1]}] 95% CI"
    else:
        result_str = (
            f"There was a {type_corr} {corr_name} correlation of {co_eff_name} = {r}"
        )
    relation_str = f" between {value1_name} and {value2_name}{group}"
    stats_str = f"; this {differ_str} (\u0070 = {P}, N = {n}, power = {power} {tailed}"
    pow2 = UnicodeGrabber.get("pow2")
    lin_reg_str = f", linear regression R{pow2} = {lm_adjr2})"

    final_str = result_str + relation_str + stats_str + lin_reg_str

    if do_print:
        print(final_str)

    figure = None
    if do_plot:
        figure = plot_corr(x, y, ax=ax, **fmt_kwargs)

    results = {
        "results": results_df,
        "output": final_str,
        "figure": figure,
    }

    return results


def mwu(x, y, fmt_kwargs=None, do_plot=False, ax=None, **kwargs):
    """
    Compute the Mann-Whitney U Test.

    This is the independent t-test non-parametric version.
    Also returns a formatted string for paper reporting.

    Parameters
    ----------
    x : array_like
        First set of observations.
    y: array_like
        Second set of observations.
    fmt_kwargs : dict, optional
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
    do_plot : bool, optional
        Whether or not to plot the result.
    ax : axes object, optional
        An axes to plot into.
    **kwargs : keyword arguments
        These are passed to pingouin.corr

    Returns
    -------
    dict with keys:
        "results" : pd.DataFrame
            The dataframe of results
        "output" : str
            A string to describe the test result for reporting
        "figure" : matplotlib.pyplot.figure or None
            The returned figure plotted into.

    See also
    --------
    pinouin.mwu
    scipy.stats.mannwhitneyu

    """
    if fmt_kwargs is None:
        fmt_kwargs = {}
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
    median1 = np.round(np.nanmedian(x), n_decimals)
    lowerq1, higherq1 = np.round(np.nanpercentile(x, [25, 75]), n_decimals)
    lowerq2, higherq2 = np.round(np.nanpercentile(y, [25, 75]), n_decimals)
    median2 = np.round(np.nanmedian(y), n_decimals)

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

    figure = None
    if do_plot:
        figure = plot_dists(x, y, ax=ax, **fmt_kwargs)

    results = {
        "results": results_df,
        "output": results_str,
        "figure": figure,
    }

    return results


def wilcoxon(x, y, fmt_kwargs=None, do_plot=False, ax=None, **kwargs):
    """
    Compute the wilcoxon signed-rank test.

    This is the non-parametric paired t-test.
    Also returns a formatted string for paper reporting.

    Parameters
    ----------
    x : array_like
        First set of observations.
    y: array_like
        Second set of observations.
    fmt_kwargs : dict, optional
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
    do_plot : bool, optional
        Whether or not to plot the result.
    ax : axes object, optional
        An axes to plot into.
    **kwargs : keyword arguments
        These are passed to pingouin.corr

    Returns
    -------
    dict with keys:
        "results" : pd.DataFrame
            The dataframe of results
        "output" : str
            A string to describe the test result for reporting
        "figure" : matplotlib.pyplot.figure or None
            The returned figure plotted into.

    See also
    --------
    pinouin.wilcoxon
    scipy.stats.wilcoxon

    """
    if fmt_kwargs is None:
        fmt_kwargs = {}
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

    results_df = pingouin.wilcoxon(x, y, **kwargs)
    U = results_df["W-val"].values[0]
    P = np.round(results_df["p-val"].values[0], n_pdecimals)
    cl = np.round(results_df["CLES"].values[0], n_decimals)
    median1 = np.round(np.nanmedian(x), n_decimals)
    lowerq1, higherq1 = np.round(np.nanpercentile(x, [25, 75]), n_decimals)
    lowerq2, higherq2 = np.round(np.nanpercentile(y, [25, 75]), n_decimals)
    median2 = np.round(np.nanmedian(y), n_decimals)

    sample_size1 = len(x)
    sample_size2 = len(y)
    n1 = "n" + UnicodeGrabber.to_sub(1)
    n2 = "n" + UnicodeGrabber.to_sub(2)
    if sample_size1 == sample_size2:
        sample_str = f"{n1} = {n2} = {sample_size1}"
    else:
        sample_str = f"{n1} = {sample_size1}, {n2} = {sample_size2}"

    stats_str = (
        "(Wilcoxon signed-rank "
        + "W"
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

    figure = None
    if do_plot:
        figure = plot_dists(x, y, ax=ax, **fmt_kwargs)

    results = {
        "results": results_df,
        "output": results_str,
        "figure": figure,
    }

    return results
