"""PDF file related utilities."""

import argparse
import os
from datetime import datetime

from PyPDF2 import PdfFileMerger

from skm_pyutils.config import parse_args
from skm_pyutils.path import get_all_files_in_dir


def pdf_cat(input_files, output_location):
    """
    Concatenate PDF files.

    Parameters
    ----------
    input_files : list of str
        Paths to files to concatenate.
    output_location : str, optional
        The path to the output merged PDF location.

    Returns
    -------
    None

    """
    if output_location is None:
        now = datetime.now()
        # current_time = now.strftime("%H-%M-%S")
        whole_time = now.strftime("%Y-%m-%d--%H-%M-%S")
        output_location = f"pdf_merge_{whole_time}.pdf"

    merger = PdfFileMerger(strict=False)
    n_merged = 0
    for pdf in input_files:
        if os.path.exists(pdf):
            print(f"Merging {pdf}")
            merger.append(pdf)
            n_merged += 1
        else:
            print(f"Warning: {pdf} does not exist")
    print(f"Saving merged output of {n_merged} files to {output_location}")
    merger.write(output_location)
    merger.close()


def merge_all_pdfs_in_dir(input_dir, out_name=None, recursive=False):
    """
    Merge all PDFs in the given directory.

    Parameters
    ----------
    input_dir : str
        The path to the directory.
    out_name : str, optional
        The name of the output file.
    recursive : bool, optional
        Whether to recurse through subdirectories. Defaults to False.
    
    Returns
    -------
    None

    """
    if out_name is None:
        now = datetime.now()
        # current_time = now.strftime("%H-%M-%S")
        whole_time = now.strftime("%Y-%m-%d--%H-%M-%S")
        out_name = f"pdf_merge_{whole_time}.pdf"
        out_name = os.path.abspath(os.path.join(input_dir, out_name))

    pdf_files = get_all_files_in_dir(
        input_dir, ext=".pdf", recursive=recursive, return_absolute=True
    )

    pdf_cat(pdf_files, out_name)


def pdf_merge_ranges(input_files, ranges, output_location=None):
    """
    Merge pdfs from given list pased on page ranges.

    Easiest way to do ranges is to import PageRange,
    and then range like PageRange("0:4") or "0:-1".

    Parameters
    ----------
    input_files : list of str
        The pdf files to merge.
    ranges : list of page ranges
        The pdf page ranges
    output_location : str, optional
        Where to output the merged pdf, defaults to None.

    Returns
    -------
    None

    """
    if output_location is None:
        now = datetime.now()
        # current_time = now.strftime("%H-%M-%S")
        whole_time = now.strftime("%Y-%m-%d--%H-%M-%S")
        output_location = f"pdf_merge_{whole_time}.pdf"

    merger = PdfFileMerger(strict=False)
    n_merged = 0
    for pdf, r in zip(input_files, ranges):
        if os.path.exists(pdf):
            print(f"Merging {pdf} over range {r}")
            merger.append(pdf, pages=r)
            n_merged += 1
        else:
            print(f"Warning: {pdf} does not exist")
    print(f"Saving merged output of {n_merged} files to {output_location}")
    merger.write(output_location)
    merger.close()

def cli_entry():
    """Command line interface entry point."""
    parser = argparse.ArgumentParser(description="PDF merger command line")

    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        default="",
        help="Directory to merge the pdf files from.",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Whether to recurse into subdirectories.",
    )
    parser.add_argument(
        "--item", "-i", action="append", type=str, help="Individual PDF files to merge."
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None, help="Name of merged output PDF file."
    )

    parsed = parse_args(parser, verbose=False)

    if os.path.exists(parsed.directory):
        merge_all_pdfs_in_dir(
            parsed.directory, out_name=parsed.output, recursive=parsed.recursive
        )
    elif parsed.item is not None:
        pdf_cat(parsed.item, parsed.output)
    else:
        raise ValueError("Please pass items or a valid directory")


if __name__ == "__main__":
    cli_entry()
