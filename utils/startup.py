""" startup.py

Functions for app prints on running script
"""
from pathlib import Path
import time
from typing import Tuple, List
from importlib.metadata import version


MAIN = "\033[1;35m"
OTHER = "\033[1;34m"
COPY_WRITE = "\033[1;32m"
NORMAL = "\033[0;37m"

OUTLINE_COLOR = "\033[0;34m"
AUTHOR_COLOR = "\033[0;35m"


def start_header() -> None:
    """ Primary User Input Controller """
    version_val = version('intellistop')

    print(" ")
    print(f"{OUTLINE_COLOR}----------------------------------")
    print(f"-{NORMAL}         Intellistops           {OUTLINE_COLOR}-")
    print("-                                -")
    print(f"-{AUTHOR_COLOR}            nga-27              {OUTLINE_COLOR}-")
    print("-                                -")
    print(f"-{NORMAL}       version: {version_val}           {OUTLINE_COLOR}-")
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


def handle_startup() -> Tuple[list, str, bool, bool]:
    """handle_startup

    returns the fund list content

    Returns:
        Tuple[list, str, bool]: fund string list, raw input string, has_error
    """
    print("")
    logo_renderer()
    start_header()
    print("")
    fund_raw = input("Enter a fund ticker [or tickers separated by a space or comma]: ").upper()
    print("")

    if len(fund_raw) == 0:
        print("ERROR: No fund ticker entered on input. Exiting...")
        return [], "", True, True

    should_plot = True
    fund_list: List[str] = []
    fund_stripped = fund_raw.strip()
    commas = fund_stripped.split(',')
    for fund in commas:
        space_split = fund.split(' ')
        for item in space_split:
            if len(item) > 0:
                fund_list.append(item.strip())
    returnable_fund_list = []
    for fund in fund_list:
        if "--" in fund:
            cmd = fund.replace("--", "")
            if cmd == "NO_PLOT":
                should_plot = False
            else:
                print(f"ERROR: Unrecognized command '{cmd}' in input. Exiting...")
                return [], "", True, True
        else:
            returnable_fund_list.append(fund)
    returnable_fund_set = set(returnable_fund_list)
    if len(returnable_fund_set) == 0:
        print("ERROR: No valid fund tickers entered on input. Exiting...")
        return [], "", True, True
    returnable_fund_list = list(returnable_fund_set)
    return returnable_fund_list, fund_raw, False, should_plot
