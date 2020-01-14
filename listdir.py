import os

import skm_pyutils.py_path


def main(location):
    res = skm_pyutils.py_path.get_all_files_in_dir(
        location, return_absolute=False, recursive=True)
    for r in res:
        print(r)


if __name__ == "__main__":
    location = os.getcwd()
    main(location)
