import requests
import datetime

# class HeightFinder:
#     def __init__(self):
#         self = self

# from block get timestamp
# https://osmosis-mainnet-rpc.allthatnode.com:1317/blocks/3

def unix_to_timestamp(unix):
    str_num = str(unix)[:-3]
    timestamp = datetime.datetime.utcfromtimestamp(int(str_num))
    print(type(timestamp))
    return timestamp

def get_block_timestamp(height): 
    block = {}
    response = requests.get(f'https://osmosis-mainnet-rpc.allthatnode.com:1317/blocks/{height}').json() # find another link
    timestamp = response['block']['header']['time']
    timestamp = timestamp.replace('Z', '')[0:19]
    timestamp = datetime.datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S")
    return timestamp


def estimate_block_height_by_timestamp(timestamp):
    target_timestamp = timestamp
    averageBlockTime = 6.2
    block_request = requests.get('https://osmosis-lcd.quickapi.com/cosmos/base/tendermint/v1beta1/blocks/latest').json()
    blockNumber = int(block_request['block']['header']['height'])
    blockTime = block_request['block']['header']['time']
    blockTime = blockTime.replace('Z', '')[0:19]
    blockTime = datetime.datetime.strptime(blockTime,"%Y-%m-%dT%H:%M:%S")
    
    
    lowerLimitStamp = target_timestamp - datetime.timedelta(seconds=6)
    higherLimitStamp = target_timestamp
    
    requestsMade = 1

    while blockTime > target_timestamp:
        delta = blockTime - target_timestamp
        delta = delta.total_seconds()
        decreaseBlocks = int(delta / 6) # make this average block time for more precise results
        if decreaseBlocks < 1:
            if blockTime <= target_timestamp:
                break
            else:
                blockNumber = blockNumber - 1
                blockTime = get_block_timestamp(blockNumber)
                break
        blockNumber = blockNumber - decreaseBlocks
        print(blockNumber)
        blockTime = get_block_timestamp(blockNumber)
        requestsMade += 1

    if blockTime < lowerLimitStamp:

        while blockTime < lowerLimitStamp:
            blockNumber += 10
            
            blockTime = get_block_timestamp(blockNumber)
    
    if blockTime > higherLimitStamp:
        while blockTime > lowerLimitStamp:
            blockNumber -= 1
            
            blockTime = get_block_timestamp(blockNumber)
            
            requestsMade += 1       
    
    # print(f'Number of Requests made: {requestsMade}, the block height is: {blockNumber}')
    return blockNumber, blockTime


def main():
    date_object = unix_to_timestamp(1666951200000) # datetime.datetime.strptime("2022-10-28 10:00:00",'%Y-%m-%d %H:%M:%S') # 
    blockNumber, blockTime = estimate_block_height_by_timestamp(date_object)
    print('Block Number: ' + str(blockNumber))
    print('Block Time: ' + str(blockTime))


if __name__ == '__main__':
    main()