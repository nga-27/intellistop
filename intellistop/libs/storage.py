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
    tickers = "tickers"
    version = "version"
    update_date = "update_date"

class StorageKeysEnum(Enum):
    conservative_stop = "conservative_stop"
    current_stop = "current_stop"
    current_vf = "current_vf"
    max_vf = "max_vf"
    min_vf = "min_vf"
    update_date = "update_date"


class Storage:
    stored_data: dict = {
        StorageKeysTopEnum.tickers.value: {},
        StorageKeysTopEnum.version.value: "1",
        StorageKeysTopEnum.update_date.value: datetime.datetime.now().isoformat()
    }

    def __init__(self):
        temp_path = os.path.join(os.getcwd(), STORAGE_DIR_NAME)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        if os.path.exists(STORAGE_PATH):
            with open(STORAGE_PATH, 'r', encoding='utf-8') as store_file:
                self.stored_data = json.load(store_file)

    def store(self):
        self.stored_data[StorageKeysTopEnum.update_date.value] = datetime.datetime.now().isoformat()
        with open(STORAGE_PATH, 'w') as store_file:
            json.dump(self.stored_data, store_file)

    def update_ticker(self, ticker: str, new_data: NewTickerDataStorageType):
        if ticker not in self.stored_data[StorageKeysTopEnum.tickers.value]:
            self.stored_data[StorageKeysTopEnum.tickers.value][ticker] = {}
        self.stored_data[StorageKeysTopEnum.tickers.value]\
            [ticker][StorageKeysEnum.current_vf.value] = new_data.current_vf
        self.stored_data[StorageKeysTopEnum.tickers.value]\
            [ticker][StorageKeysEnum.current_stop.value]  = new_data.current_stop
        
        if StorageKeysEnum.max_vf.value not in \
            self.stored_data[StorageKeysTopEnum.tickers.value][ticker] or \
            self.stored_data[StorageKeysTopEnum.tickers.value][ticker]\
                [StorageKeysEnum.max_vf.value] < new_data.current_vf:
            self.stored_data[StorageKeysTopEnum.tickers.value][ticker]\
                [StorageKeysEnum.max_vf.value] = new_data.current_vf
            
        if StorageKeysEnum.min_vf.value not in \
            self.stored_data[StorageKeysTopEnum.tickers.value][ticker] or \
            self.stored_data[StorageKeysTopEnum.tickers.value][ticker]\
                [StorageKeysEnum.min_vf.value] > new_data.current_vf:
            self.stored_data[StorageKeysTopEnum.tickers.value][ticker]\
                [StorageKeysEnum.min_vf.value] = new_data.current_vf
            
        self.stored_data[StorageKeysTopEnum.tickers.value][ticker]\
            [StorageKeysEnum.conservative_stop.value] = new_data.current_max_price * \
                (100.0 - self.stored_data[StorageKeysTopEnum.tickers.value][ticker]\
                [StorageKeysEnum.min_vf.value]) / 100.0
        
        self.stored_data[StorageKeysTopEnum.tickers.value][ticker]\
            [StorageKeysEnum.update_date.value] = datetime.datetime.now().isoformat()
        
    def get_stored_data_by_ticker(self, ticker: str) -> Union[dict, None]:
        return self.stored_data[StorageKeysTopEnum.tickers.value].get(ticker)
        