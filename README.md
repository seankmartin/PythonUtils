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

```Bash
pdf-merge -h
dir-list -h
```

For example

```Bash
pdf-merge -d . -r -o merged.pdf
dir-list . -r -e .txt -o txt_file_list.txt
copy-files input_dir output_dir -re .*results.*.png
```

## Modules

- array : Small numpy style functions.
- config : Config utils, e.g read a full .py python file as configuration using exec.
- log: Logging utils, e.g. logging exceptions to disk and stdout.
- merge : combine csv files together, or grab files of a particular type from recursive folders and merge into one folder
- path: Path utils, e.g. finding all files in a directory with given extension recursively.
- pdf : PDF utils, e.g. merging all PDFs files in a directory, or pdfs with given pages
- plot : Plotting utils, e.g. automatically handled gridding of plots, with color management.
- print : Printing utils, e.g. pretty printing a dictionary, or HDF5 file.
- profile : Code profiling, e.g. profiling code for runtime performance.
- save : Saving outputs, e.g. a full dictionary recursively.
- stats : Hyptothesis tests etc.
- tables : Pandas dataframe utils.