import requests
import pandas as pd
import numpy as np
import asyncio
import datetime
import time
import pytz


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 30)

BOOK_LIST = []

### Rationale: Python
# keep getting orderbook from binance,
async def get_binance_book():
    rest_url = f"https://data.binance.com/api/v3/depth"

    params = {
        "symbol": "OSMOUSDT",
        "limit": 20
    }
    for _ in range(10):
        try:
            snapshot = requests.get(rest_url, params=params).json()
            await asyncio.sleep(0.1)
        except requests.exceptions.JSONDecodeError as e:
            snapshot = None
        # a dictionary of side: price, quantity orderbook
        snapshot["time"] = get_gmt_time()
        BOOK_LIST.append(snapshot)
    return BOOK_LIST


async def get_block_time():
    try:
        block_request = requests.get(
            'https://osmosis-lcd.quickapi.com/cosmos/base/tendermint/v1beta1/blocks/latest').json()
        await asyncio.sleep(2)
    except requests.exceptions.JSONDecodeError as e:
        # print("Error: ", e)
        blockTime = None
        blockNumber = None
    

    blockNumber = int(block_request['block']['header']['height'])
    blockTime = block_request['block']['header']['time']
    blockTime = blockTime.replace('Z', '')[0:26]
    blockTime = datetime.datetime.strptime(blockTime, "%Y-%m-%dT%H:%M:%S.%f")
    return blockNumber, blockTime
    # print(f"Block Number: {blockNumber}, Block Time: {blockTime}")



def get_gmt_time():
    gmt = pytz.timezone('GMT')
    gmt_time = datetime.datetime.now(gmt).strftime("%Y-%m-%d %H:%M:%S.%f")
    gmt_time = datetime.datetime.strptime(gmt_time, "%Y-%m-%d %H:%M:%S.%f")
    return gmt_time

# def formatted_time_compare(time1, time2):
#     datetime1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S.%f")
#     datetime2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S.%f")
#     print(type(datetime1))
#     return datetime1 < datetime2

async def main():
    # result_queue = multiprocessing.Queue()

   while True:
        l1 = asyncio.create_task(get_binance_book())
        l2 = asyncio.create_task(get_block_time())
        # Wait for the tasks to finish
        templist = await l1
        print(templist)
        print(f"the length of the orderbook list is {len(templist)}")
        # print(snapshot)
        blockNumber, blockTime = await l2
        print(f"Block Number: {blockNumber}, Block Time: {blockTime}")




    # sleep_time = 0.5

    # df_osmosis = pd.DataFrame(columns=['block_time', 'block_height'])
    
    # if not result_queue.empty():
    #     block_info = result_queue.get()
    #     print(f"the block_info is {block_info}.")
    #     block_time = block_info[0]
    #     block_height = block_info[1]
    #     current_update = {'block_time': block_time, 'block_height': block_height}
    #     df_osmosis = df_osmosis.append(current_update, ignore_index=True)

    #     df_binance = pd.DataFrame(columns=['bids', 'asks', 'lastUpdateId', 'time', 'flag'])
    #     binance_snapshot = result_queue.get()
    #     df_binance = df_binance.append(binance_snapshot, ignore_index=True)

    # while True:
    #     binance_snapshot = result_queue.get()
    #     print(binance_snapshot)
    #     df_binance = df_binance.append(binance_snapshot, ignore_index=True)
    #     # print(df_binance)
    #     # df_binance.loc[-1].at['flag'] = False
    #     if not result_queue.empty():
    #         block_info = result_queue.get()
    #         block_time = block_info[0]
    #         block_height = block_info[1]
    #         # if block_time is the same as last time (during sleep_time, no block is formed) or if block_time returns None due to Server issue
    #         if block_time == df_osmosis.iloc[-1]['block_time'] or block_time == None:
    #             continue
    #         # if block_time==df['block_time'].iloc[-1] and block_height==df['block_height'].iloc[-1]:
    #         current_update = {'block_time': block_time, 'block_height': block_height} # type = dict
    #         df_osmosis = df_osmosis.append(current_update, ignore_index=True)
    #     # df_osmosis.drop_duplicates(subset=None,keep='last',inplace=True)
    #     # print(df_osmosis)

    #     # get the subset of df_binance where time < block_time
    #     subset = df_binance.loc[df_binance['time'] < block_time]
    #     try:
    #         max_time_idx = subset['time'].idxmax() 
    #         df_binance.at[max_time_idx, 'flag'] = True
    #         print(max_time_idx)
    #     except:
    #         time.sleep(sleep_time)
    #         continue
    #     time.sleep(sleep_time)

if __name__ == "__main__":
    asyncio.run(main())