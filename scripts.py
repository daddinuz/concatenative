import sys
import subprocess


def analyzer():
    match sys.argv[1:]:
        case []:
            subprocess.run(["pyright"])
        case _:
            print("USAGE: poetry run analyzer")
            sys.exit(1)


def example():
    match sys.argv[1:]:
        case [module]:
            subprocess.run(["python", "-m", f"src.examples.{module}"])
        case _:
            print("USAGE: poetry run --example <module>")
            sys.exit(1)


def test():
    match sys.argv[1:]:
        case []:
            subprocess.run(["python", "-u", "-m", "unittest", "discover", "-s", "src"])
        case _:
            print("USAGE: poetry run test")
            sys.exit(1)


def fmt():
    match sys.argv[1:]:
        case []:
            subprocess.run(["python", "-m", "black", "src", "scripts.py"])
        case _:
            print("USAGE: poetry run fmt")
            sys.exit(1)
