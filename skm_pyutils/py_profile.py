"""Utilities for code performance profiling."""
import argparse
import pstats


def default_stats(profile_location):
    """
    Print the result of code profling.

    See https://docs.python.org/2/library/profile.html
    
    Parameters
    ----------
    profile_location : str
        The path to a profile file.

    Returns
    -------
    None

    """
    if os.path.isfile(profile_location):
        p = pstats.Stats(profile_location)
        # p.strip_dirs().sort_stats(-1).print_stats()

        print("Biggest cumulative users")
        p.sort_stats("cumulative").print_stats(20)

        print("Biggest time users")
        p.sort_stats("time").print_stats(20)

        # p.sort_stats('time', 'cumulative').print_stats(.5, 'init')
        # p.print_callers(.5, 'init')

    else:
        raise FileNotFoundError(
            "{} does not exist".format(profile_location)
            + "You can create profile.out by running:"
            + "python -m cProfile -o <profile_location> <filename>"
        )


def main():
    parser = argparse.ArgumentParser("Command line interface")
    parser.add_argument(
        "profile_location", type=str, help="location of the profile file"
    )
    parsed, unparsed = parser.parse_known_args()

    if len(unparsed) > 0:
        raise ValueError("Unrecognised command line arguments")

    default_stats(parser.profile_location)


if __name__ == "__main__":
    main()
