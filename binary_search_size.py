import pandas as pd

# last block 8751002
# 
# next block 8751003
# 

# last order book before block 8751002
data = {"lastUpdateId": 37100665, "bids": [["0.88500000", "512.85000000"], ["0.88400000", "1685.41000000"], ["0.88300000", "2346.80000000"], ["0.88200000", "1800.04000000"], ["0.88100000", "1604.43000000"], ["0.88000000", "1417.84000000"], ["0.87900000", "59581.78000000"], ["0.87800000", "5956.70000000"], ["0.87700000", "8533.32000000"], ["0.87600000", "5829.77000000"], ["0.87500000", "9531.54000000"], ["0.87400000", "389.09000000"], ["0.87300000", "1872.47000000"], ["0.87200000", "596.33000000"], ["0.87100000", "2746.19000000"], ["0.87000000", "1364.11000000"], ["0.86900000", "1710.14000000"], ["0.86800000", "1017.46000000"], ["0.86700000", "25.44000000"], ["0.86600000", "577.37000000"]], "asks": [["0.88600000", "119.97000000"], ["0.88700000", "2520.97000000"], ["0.88800000", "6862.83000000"], ["0.88900000", "3859.50000000"], ["0.89000000", "2051.45000000"], ["0.89100000", "22563.99000000"], ["0.89200000", "3002.28000000"], ["0.89300000", "561.80000000"], ["0.89400000", "2880.73000000"], ["0.89500000", "10328.47000000"], ["0.89600000", "1468.95000000"], ["0.89700000", "2020.84000000"], ["0.89800000", "392.34000000"], ["0.89900000", "558.04000000"], ["0.90000000", "1176.46000000"], ["0.90100000", "483.50000000"], ["0.90200000", "1771.15000000"], ["0.90300000", "23.23000000"], ["0.90400000", "1216.03000000"], ["0.90500000", "568.95000000"]], "time": "2023-03-17 21:28:23.209057"}


# on block 8751002
USDC_balance = 10554054313213
OSMO_balance = 11938272258924
weight = 536870912000000
swap_fee = 0.002000000000000000

osmosis_price = USDC_balance / OSMO_balance # 0.884
highest_bid_price = 0.885

bids = data["bids"]

balanceIn = USDC_balance
balanceOut = OSMO_balance
sp_goal = highest_bid_price
sp_now = osmosis_price # 0.884


# bid_price > Osmosis
#     buy on Osmosis and sell on Binance

# Osmosis: USDC -> OSMO ; Binance: OSMO -> USDC
# tokenIn = USDC
# tokenOut = OSMO

# assuming infinite liquidity on Osmosis, 

# given the osmosis price, find out how much I can trade on binance before the price gets same
def find_max_size_binance():
    i = 0
    max_size = 0
    while float(bids[i][0]) > osmosis_price:
        max_size += float(bids[i][1])
        i += 1
    return max_size

# on Biance: given the amount of OSMO, calculate how much USDC out
def binance_usdc_out(size):
    # trades on each layer
    usdc_out = 0
    # print(f"on Binance: trade in {size} OSMOS")
    size = size * 0.999 # 0.1% fee on binance
    for i in range(len(bids)):
        price = float(bids[i][0])
        depth = float(bids[i][1])
        if size > depth:
            usdc_out += depth * price
            size -= depth
            # print(f"the current size is {size}")
        else:
            # print(f"the size left is {size}")
            usdc_out += size * price
            break
    # print(f"On binance gives {usdc_out} USDC out")
    return usdc_out

def etherToNum(amount):
    return amount/1000000


# profit in USDC
def calculate_profit(size):
    usdc_in_osmosis = size
    # osmosis_price = 0.884
    osmo_out_osmosis = etherToNum(balanceOut) * (1-(etherToNum(balanceIn)/(etherToNum(balanceIn) + usdc_in_osmosis*0.998))) # 0.2% fee on Osmosis
    osmo_price = size / osmo_out_osmosis
    print(f"the amount of OSMO out of osmosis is {osmo_out_osmosis}, with price of {osmo_price}")
    usdc_out_binance = binance_usdc_out(osmo_out_osmosis)
    print(f"sell OSMO on binance get {usdc_out_binance} USDC")
    osmo_profit = usdc_out_binance - size
    return osmo_profit




# a recursive method to find max profit
# def find_optimal_size(min, max):
#     testing_size = ((max - min) / 2) + min
#     if calculate_profit(testing_size - 100) < calculate_profit(testing_size) and calculate_profit(testing_size + 100) < calculate_profit(testing_size):
#         return testing_size
#     else: 
#         if calculate_profit(testing_size - 100) > calculate_profit(testing_size) and calculate_profit(testing_size + 100) < calculate_profit(testing_size):
#             return find_optimal_size(min, testing_size-100)
#         elif calculate_profit(testing_size - 100) < calculate_profit(testing_size) and calculate_profit(testing_size + 100) > calculate_profit(testing_size):
#             return find_optimal_size(testing_size + 100, max)




def main():
    maxAmountIn = find_max_size_binance()
    print(f"the max amount of USDC I can trade in is {maxAmountIn}")
    # trade_size = find_optimal_size(0, maxAmountIn)
    print(f"the optimal trade size is {maxAmountIn} USDC into Osmosis")
    profit = calculate_profit(maxAmountIn)
    print(f"the profit of the arb is {profit}")


if __name__ == "__main__":
    main()