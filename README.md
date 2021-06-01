# PythonUtils

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A module containing common scripts that I use in my research.
Documentation available at https://seankmartin.github.io/PythonUtils/html/skm_pyutils/index.html.

## Installation

`pip install skm_pyutils`

## Update documentation
`pdoc --html -o "docs\html" skm_pyutils --force`

## Command line running
```
pdf-merge -h
dir-list -h
```
For example
```
pdf-merge -d . -r -o merged.pdf
dir-list . -r -e .txt -o txt_file_list.txt
copy-files input_dir output_dir -re .*results.*.png
```

## Modules
- py_config : Config utils, e.g read a full .py python file as configuration using exec.
- py_log: Logging utils, e.g. logging exceptions to disk and stdout.
- py_path: Path utils, e.g. finding all files in a directory with given extension recursively.
- py_pdf : PDF utils, e.g. merging all PDFs files in a directory.
- py_plot : Plotting utils, e.g. automatically handled gridding of plots, with color management.
- py_print : Printing utils, e.g. pretty printing a dictionary, or HDF5 file.
- py_profile : Code profiling, e.g. profiling code for runtime performance.
- py_save : Saving outputs, e.g. a full dictionary recursively.
- py_tables : Pandas dataframe utils.