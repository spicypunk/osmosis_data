#!/myenv python3

import requests
import pandas as pd
import numpy as np

import datetime
import time
import pytz
from multiprocessing import Process, Queue, Value, Array

### Rationale: Python
# keep getting orderbook from binance, 
def get_binance_book():
    rest_url = f"https://data.binance.com/api/v3/depth"

    params = {
        "symbol": "OSMOUSDT",
        "limit": 20
    }

    try:
        snapshot = requests.get(rest_url, params=params).json()
    except requests.exceptions.JSONDecodeError as e:
        snapshot = None
        return snapshot
    # a dictionary of side: price, quantity orderbook
    snapshot["time"] = datetime.datetime.now(pytz.timezone('GMT')).strftime("%Y-%m-%d %H:%M:%S.%f")
    time.sleep(0.5)
    return snapshot

def get_block_time():
    try:
        block_request = requests.get(
            'https://osmosis-lcd.quickapi.com/cosmos/base/tendermint/v1beta1/blocks/latest').json()
    except json.decoder.JSONDecodeError as e:
        blockTime = None
        blockNumber = None
        return blockTime, blockNumber

    blockNumber = int(block_request['block']['header']['height'])
    blockTime = block_request['block']['header']['time']
    blockTime = blockTime.replace('Z', '')[0:26]
    blockTime = datetime.datetime.strptime(blockTime, "%Y-%m-%dT%H:%M:%S.%f")
    time.sleep(1.5)

    # except Exception as e:
    #     print(f"an error retrieving blocktime has occured: {e}" )
    #     if blockTime is None:
    #         raise ValueError('Failed to get block time')

    return blockTime, blockNumber


def get_gmt_time():
    gmt = pytz.timezone('GMT')
    gmt_time = datetime.datetime.now(gmt)
    return gmt_time


def main():
    df_binance = pd.DataFrame(columns=['bids', 'asks', 'lastUpdateId', 'time'])
    binance_snapshot = get_binance_book()
    df_binance = df_binance.append(binance_snapshot, ignore_index=True)
    while True:
        binance_snapshot = get_binance_book()
        df_binance = df_binance.append(binance_snapshot, ignore_index=True)
        print(df_binance)

    df_osmosis = pd.DataFrame(columns=['block_time', 'block_height'])
    block_time, block_height = get_block_time()
    current_update = {'block_time': block_time, 'block_height': block_height}
    df_osmosis = df_osmosis.append(current_update, ignore_index=True)

    while True:
        block_time, block_height = get_block_time()
        # if block_time==df['block_time'].iloc[-1] and block_height==df['block_height'].iloc[-1]:
        current_update = {'block_time': block_time, 'block_height': block_height}
        df_osmosis = df_osmosis.append(current_update, ignore_index=True)
        print(df)
        df_osmosis.drop_duplicates()


if __name__ == "__main__":
    q = Queue()
    p = Process(target=main, args=())
    p.start()
    p.join()