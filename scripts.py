import os
import sys


def _exec(*args):
    assert args
    return os.execlp(args[0], *args)


def analyzer():
    match sys.argv[1:]:
        case []:
            _exec("pyright")
        case _:
            print("USAGE: poetry run analyzer")
            sys.exit(1)


def bin():
    match sys.argv[1:]:
        case [module]:
            _exec("python", "-m", f"src.bins.{module}")
        case _:
            print("USAGE: poetry run --bin <module>")
            sys.exit(1)


def example():
    match sys.argv[1:]:
        case [module]:
            _exec("python", "-m", f"src.examples.{module}")
        case _:
            print("USAGE: poetry run --example <module>")
            sys.exit(1)


def test():
    match sys.argv[1:]:
        case []:
            _exec("python", "-u", "-m", "unittest", "discover", "-s", "src")
        case _:
            print("USAGE: poetry run test")
            sys.exit(1)


def fmt():
    match sys.argv[1:]:
        case []:
            _exec("python", "-m", "black", "src", "scripts.py")
        case _:
            print("USAGE: poetry run fmt")
            sys.exit(1)
