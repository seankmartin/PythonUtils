"""Utilities for code performance profiling."""
import os
import io
import argparse
import pstats
import cProfile

def profileit(name):
    """
    Decorator to profile code performance.

    Usage:
    @profileit("profile_for_func1_001");
    def func1(...)

    See https://stackoverflow.com/questions/5375624/a-decorator-that-profiles-a-method-call-and-logs-the-profiling-result/5376616

    """
    def inner(func):
        def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            s = io.StringIO()
            sortby = pstats.SortKey.CUMULATIVE
            ps = pstats.Stats(prof, stream=s).strip_dirs().sort_stats(sortby)
            ps.print_stats()
            with open(name, "w") as f:
                f.write(s.getvalue())
            return retval
        return wrapper
    return inner


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

def timeit(name):
    """Decorator to time code performance.
    
    Parameters
    ----------
    name : str
        The name of the function to be timed.
    
    Returns
    -------
    inner : function
        The wrapper function.
    
    Usage
    -----
    @timeit("func1")
    def func1(...):
        ...
    
    """
    def inner(func):
        def wrapper(*args, **kwargs):
            t1 = perf_counter()
            func(*args, **kwargs)
            t2 = perf_counter()

            print(f"{name} took {t2 - t1:.2f} seconds")

        return wrapper

    return inner


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
