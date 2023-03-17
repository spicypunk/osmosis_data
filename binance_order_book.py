import requests
import pandas as pd
import datetime
import time
import pytz

# keep getting orderbook from binance, 
def get_binance_book(book_list):
    r = requests.get("https://data.binance.com/api/v3/depth",
                 params=dict(symbol="OSMOUSDT"))
    results = r.json()
    # a dictionary of side: price, quantity orderbook
    frame = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"],
                             dtype=float).assign(time=pd.Timestamp.now())
          for side in ["bids", "asks"]}
    book_list.append(frame)

def get_block_time():
    blockTime, blockNumber = None, None
    try: 
        block_request = requests.get('https://osmosis-lcd.quickapi.com/cosmos/base/tendermint/v1beta1/blocks/latest').json()
        blockNumber = int(block_request['block']['header']['height'])
        blockTime = block_request['block']['header']['time']
        blockTime = blockTime.replace('Z', '')[0:19]
        blockTime = datetime.datetime.strptime(blockTime,"%Y-%m-%dT%H:%M:%S")

    except Exception as e:
        print(f"an error retrieving blocktime has occured: {e}" )
        if blockTime is None:
            raise ValueError('Failed to get block time')
    return blockTime, blockNumber

def get_gmt_time():
    gmt = pytz.timezone('GMT')
    gmt_time = datetime.datetime.now(gmt)
    return gmt_time


def main():
    book_list = []
    saved_block_time, saved_block_height = get_block_time()
    print(f"saved_block_time is {saved_block_time}, height is {saved_block_height}")
    while True:
        get_binance_book(book_list)
        print(book_list)
        time.sleep(0.1)
        block_time, block_height = get_block_time()
        print(f"the block height is {block_height}")
        print(f"the block time is {block_time}")

    
        if block_time > saved_block_time:
            # print(f"the block height is {block_height}")
            # print(f"the block time is {block_time}")
            # # print(book_list)
            saved_block_time = block_time
            book_list = []
            break



if __name__ == "__main__":
    main()