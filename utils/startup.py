""" startup.py

Functions for app prints on running script
"""
from pathlib import Path
import time
from typing import Tuple, List
import json
from importlib.metadata import version

from intellistop.libs.storage import STORAGE_PATH


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


def handle_commands(command: str) -> Tuple[bool, List[str], bool]:
    """handle_commands

    Handle commands that are input on startup

    Args:
        command (str): command string to handle

    Returns:
        bool: whether the command was recognized and handled
    """
    tickers_to_use = []
    is_valid_command = True
    should_plot = True
    should_store_data = False
    cmd = command.replace("--", "")
    if cmd == "HELP":
        print("Available commands:\r\n")
        print("--HELP: Show this help message")
        print("--NO_PLOT: Disable plotting of results")
        print("--STORE: Store the entered tickers for future use")
        print("--USE_STORE: Use the stored tickers from the last run\r\n")
        return True, tickers_to_use, should_store_data, should_plot
    elif cmd == "NO_PLOT":
        should_plot = False
        return is_valid_command, tickers_to_use, should_store_data, should_plot
    elif cmd == "STORE":
        should_store_data = True
        return is_valid_command, tickers_to_use, should_store_data, should_plot
    elif cmd == "USE_STORE":
        if Path(STORAGE_PATH).exists():
            with open(STORAGE_PATH, 'r', encoding='utf-8') as store_file:
                stored_data = json.load(store_file)
            tickers_to_use = stored_data.get("ticker_list", [])
        else:
            print(f"No storage file found at '{STORAGE_PATH}'.")
        return is_valid_command, tickers_to_use, should_store_data, should_plot
    else:
        print(f"ERROR: Unrecognized command '{cmd}' in input. Exiting...")
        is_valid_command = False
        return is_valid_command, tickers_to_use, should_store_data, should_plot


def save_to_store(ticker_list: List[str]) -> None:
    """save_to_store

    Save ticker list to storage file

    Args:
        ticker_list (List[str]): list of tickers to save
    """
    data_store = {}
    with open(STORAGE_PATH, 'r', encoding='utf-8') as store_file:
        data_store = json.load(store_file)
    data_store["ticker_list"] = ticker_list
    with open(STORAGE_PATH, 'w', encoding='utf-8') as store_file:
        json.dump(data_store, store_file)


def handle_startup() -> Tuple[list, str, bool, bool]:
    """handle_startup

    returns the fund list content

    Returns:
        Tuple[list, str, bool, bool]: fund string list, raw input string, has_error, should_plot
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
    should_store_data = False
    for fund in fund_list:
        if "--" in fund:
            is_valid, tickers_to_use, should_store_data, should_plot = handle_commands(fund)
            if not is_valid:
                return [], "", True, True
            if len(tickers_to_use) > 0:
                returnable_fund_list.extend(tickers_to_use)
        else:
            returnable_fund_list.append(fund)
    returnable_fund_set = set(returnable_fund_list)
    if len(returnable_fund_set) == 0:
        print("ERROR: No valid fund tickers entered on input. Exiting...")
        return [], "", True, True
    if should_store_data:
        save_to_store(list(returnable_fund_set))
    returnable_fund_list = list(returnable_fund_set)
    return returnable_fund_list, fund_raw, False, should_plot
