""" storage class to handle historical events """
import os
import json
import datetime
from typing import Union
from enum import Enum

from .lib_types import NewTickerDataStorageType


STORAGE_FILE_NAME = "__internal_intellistop.json"
STORAGE_DIR_NAME = "output"
STORAGE_PATH = os.path.join(os.getcwd(), STORAGE_DIR_NAME, STORAGE_FILE_NAME)

# Keys in dictionary!
class StorageKeysTopEnum(Enum):
    """ StorageKeysTopEnum """
    TICKERS = "tickers"
    VERSION = "version"
    UPDATE_DATE = "update_date"

class StorageKeysEnum(Enum):
    """ StorageKeysEnum """
    CONSERVATIVE_STOP = "conservative_stop"
    CURRENT_STOP = "current_stop"
    CURRENT_VF = "current_vf"
    MAX_VF = "max_vf"
    MIN_VF = "min_vf"
    UPDATE_DATE = "update_date"


class Storage:
    """ Storage class for storing historical data """
    stored_data: dict = {
        StorageKeysTopEnum.TICKERS.value: {},
        StorageKeysTopEnum.VERSION.value: "1",
        StorageKeysTopEnum.UPDATE_DATE.value: datetime.datetime.now().isoformat()
    }

    def __init__(self):
        temp_path = os.path.join(os.getcwd(), STORAGE_DIR_NAME)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        if os.path.exists(STORAGE_PATH):
            with open(STORAGE_PATH, 'r', encoding='utf-8') as store_file:
                self.stored_data = json.load(store_file)

    def store(self):
        """ store data to json """
        self.stored_data[StorageKeysTopEnum.UPDATE_DATE.value] = datetime.datetime.now().isoformat()
        with open(STORAGE_PATH, 'w', encoding='utf-8') as store_file:
            json.dump(self.stored_data, store_file)

    def update_ticker(self, ticker: str, new_data: NewTickerDataStorageType):
        """ update ticker info with historical and new data """
        if ticker not in self.stored_data[StorageKeysTopEnum.TICKERS.value]:
            self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker] = {}
        self.stored_data[StorageKeysTopEnum.TICKERS.value]\
            [ticker][StorageKeysEnum.CURRENT_VF.value] = new_data.current_vf
        self.stored_data[StorageKeysTopEnum.TICKERS.value]\
            [ticker][StorageKeysEnum.CURRENT_STOP.value]  = new_data.current_stop

        if StorageKeysEnum.MAX_VF.value not in \
            self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker] or \
            self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker]\
                [StorageKeysEnum.MAX_VF.value] < new_data.current_vf:
            self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker]\
                [StorageKeysEnum.MAX_VF.value] = new_data.current_vf

        if StorageKeysEnum.MIN_VF.value not in \
            self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker] or \
            self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker]\
                [StorageKeysEnum.MIN_VF.value] > new_data.current_vf:
            self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker]\
                [StorageKeysEnum.MIN_VF.value] = new_data.current_vf

        self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker]\
            [StorageKeysEnum.CONSERVATIVE_STOP.value] = new_data.current_max_price * \
                (100.0 - self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker]\
                [StorageKeysEnum.MIN_VF.value]) / 100.0

        self.stored_data[StorageKeysTopEnum.TICKERS.value][ticker]\
            [StorageKeysEnum.UPDATE_DATE.value] = datetime.datetime.now().isoformat()

    def get_stored_data_by_ticker(self, ticker: str) -> Union[dict, None]:
        """ get the stored data """
        return self.stored_data[StorageKeysTopEnum.TICKERS.value].get(ticker)
        