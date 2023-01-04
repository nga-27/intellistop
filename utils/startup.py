""" startup.py

Functions for app prints on running script
"""
from pathlib import Path
import time


MAIN = "\033[1;35m"
OTHER = "\033[1;34m"
COPY_WRITE = "\033[1;32m"
NORMAL = "\033[0;37m"

OUTLINE_COLOR = "\033[0;34m"
AUTHOR_COLOR = "\033[0;35m"


def pull_version_from_setup() -> str:
    """pull_version_from_setup

    Pull the VERSION value from the setup.py file

    Returns:
        str: version value
    """
    setup_path = Path("setup.py").resolve()
    with open(setup_path, 'r', encoding='utf-8') as setup_file:
        data = setup_file.readlines()
    return data[24][11:16]


def start_header() -> None:
    """ Primary User Input Controller """
    version = pull_version_from_setup()

    print(" ")
    print(f"{OUTLINE_COLOR}----------------------------------")
    print(f"-{NORMAL}         Intellistops           {OUTLINE_COLOR}-")
    print("-                                -")
    print(f"-{AUTHOR_COLOR}            nga-27              {OUTLINE_COLOR}-")
    print("-                                -")
    print(f"-{NORMAL}       version: {version}           {OUTLINE_COLOR}-")
    print(f"----------------------------------{NORMAL}")
    print(" ")

    time.sleep(1)


def logo_renderer():
    """ Render logo from logo.txt file """
    MAIN_LOGO_LINES = 8 # pylint: disable=invalid-name
    logo_path = Path("utils/logo.txt").resolve()
    if logo_path.exists():
        with open(logo_path, 'r', encoding='utf-8') as logo_file:
            logo_lines = logo_file.readlines()
        print(" ")

        for i, line in enumerate(logo_lines):
            if i < MAIN_LOGO_LINES:
                line = line.replace("\n", "")
                line = line.replace("{", f"{OTHER}")
                line = f"{MAIN}{line}{NORMAL}"
            else:
                line = f"{COPY_WRITE}{line}{NORMAL}"
            print(line)

        print("\r\n\r\n")
        time.sleep(1)
