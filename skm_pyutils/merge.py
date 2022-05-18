"""This module holds routine for merging outputs files and folders."""

import argparse
import os
import re
import shutil
import warnings

import numpy as np

from skm_pyutils.py_path import get_all_files_in_dir


def merge_files(in_dir, all_result_ext=None):
    """
    Merge all files with the given extension recursively from in_dir.

    Parameters
    ----------
    in_dir : str
        The path to where to start merging from.
    all_result_ext : str, optional
        The extension to look for, by default None, which takes all

    Returns
    -------
    None

    """
    all_file_loc = os.path.join(in_dir, "all_results_merged")
    os.makedirs(all_file_loc, exist_ok=True)
    print("Copying all results into {}".format(all_file_loc))
    dirs = [
        os.path.join(in_dir, o)
        for o in os.listdir(in_dir)
        if os.path.isdir(os.path.join(in_dir, o)) and o != "all_results_merged"
    ]
    for d in dirs:
        name = d[len(in_dir) :]
        name = "--".join(name.split(os.sep))
        # print("Copying contents of {}".format(d))
        all_files = get_all_files_in_dir(
            d, ext=all_result_ext, recursive=True, return_absolute=True
        )
        if all_result_ext is None:
            all_files = [
                f
                for f in all_files
                if os.path.splitext(f)[1]
                in [".png", ".jpg", ".svg", ".png", ".gif", ".tiff"]
            ]

        all_names = [
            "--".join(f[len(in_dir + os.sep) :].split(os.sep)) for f in all_files
        ]
        for f, o_name in zip(all_files, all_names):
            out_name = os.path.join(all_file_loc, o_name)
            shutil.copy(f, out_name)


def csv_merge(in_dir, keep_headers=True, insert_newline=True, stats=True, delim=","):
    """
    Merge all csv files recursively from in_dir into one file.

    Parameters
    ----------
    in_dir : str
        The directory to start the merging from.
    keep_headers : bool, optional
        Keep the headers in the csv file, by default True
    insert_newline : bool, optional
        Write things on new lines, by default True
    stats : bool, optional
        Do average and std of numerical values, by default True
    delim : str, optional
        What delimiter to use, by default ","

    Returns
    -------
    None

    """
    data_start_col = 2
    csv_files = get_all_files_in_dir(in_dir, ext="csv", recursive=True)
    try:
        o_name = os.path.join(in_dir, f"merge--{os.path.basename(in_dir)}.csv")
    except BaseException:
        o_name = os.path.join(in_dir, f"merge.csv")
    print("Merging csv results into {}".format(o_name))
    if os.path.isfile(o_name):
        csv_files = csv_files[1:]
    with open(o_name, "w") as output:
        for i, f in enumerate(csv_files):
            # print("Merging {}".format(f))
            with open(f, "r") as open_file:
                file_data = open_file.read()
                lines = file_data.split("\n")
                if keep_headers or (i == 0):
                    for i, line in enumerate(lines):
                        output.write(line)
                        if i != len(lines) - 1:
                            output.write("\n")
                else:
                    for i, line in enumerate(lines[1:]):
                        output.write(line)
                        if i != len(lines) - 2:
                            output.write("\n")

                if stats:
                    file_data = re.sub('"[^"]+"', "NAN", file_data)
                    lines = file_data.split("\n")[:-1]
                    split_up = []
                    for line in lines[1:]:
                        if line != "":
                            split_up.append(line.split(",")[data_start_col:])
                    data = np.zeros(shape=(len(split_up), len(split_up[0])))
                    for i, row in enumerate(split_up):
                        for j, val in enumerate(row):
                            try:
                                to_write = float(val.strip())
                            except BaseException:
                                to_write = np.nan
                            data[i, j] = to_write
                    if np.sum(data) == 0:
                        # print("No data to average in merge")
                        # Added pass to make code valid
                        pass
                    else:
                        check = data[-1]
                        if np.sum(check) == 0:
                            raise RuntimeError(
                                "Excel sheet to merge has trailing blank lines"
                            )
                        with warnings.catch_warnings():
                            warnings.filterwarnings(
                                action="ignore", message="Mean of empty slice"
                            )
                            warnings.filterwarnings(
                                action="ignore",
                                message="Degrees of freedom <= 0 for slice.",
                            )
                            avg = np.nanmean(data, axis=0)
                            std = np.nanstd(data, axis=0)
                        avg_str = (
                            "Average," + "," + ",".join(str(val) for val in avg) + "\n"
                        )
                        std_str = (
                            "Std," + "," + ",".join(str(val) for val in std) + "\n"
                        )
                        output.write(avg_str)
                        output.write(std_str)

                if insert_newline:
                    output.write("\n")


def cli():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Command line arguments")
    parser.add_argument("directory", type=str, help="The directory to merge in")
    parser.add_argument(
        "--do_csv", "-n", action="store_true", help="should merge csv files"
    )
    parser.add_argument(
        "--do_images", "-i", action="store_true", help="should merge images"
    )
    parser.add_argument(
        "--image_extension",
        "-e",
        type=str,
        default=None,
        help="the image extension to look for (without .)",
    )

    parsed, unparsed = parser.parse_known_args()
    if len(unparsed) > 0:
        raise ValueError("Unexpected arguments {}".format(unparsed))

    if parsed.do_csv:
        print("----------CSV MERGE-----------")
        csv_merge(parsed.directory)

    if parsed.do_images:
        print("----------IMAGE MERGE-----------")
        merge_files(parsed.directory, all_result_ext=parsed.image_extension)


if __name__ == "__main__":
    cli()
