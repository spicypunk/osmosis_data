import pandas as pd

# last block 8751002
# 
# next block 8751003
# 

# last order book before block 8751002

BINANCE_FEE = 0.001
OSMOSIS_FEE = 0.002

# bid_price > Osmosis
#     buy on Osmosis and sell on Binance
#  calculate_usdc_profit()

# Osmosis: USDC -> OSMO ; Binance: OSMO -> USDC
# tokenIn = USDC
# tokenOut = OSMO

# assuming infinite liquidity on Osmosis, 

# given the osmosis price, find out how much OSMO to trade in on binance before the price gets same
# also return the USDC amount
def binance_find_max_osmo_sell(bids, osmosis_price):
    i = 0
    max_size = 0
    usdc_out = 0
    while float(bids[i][0]) > osmosis_price:
        max_size += float(bids[i][1])
        usdc_out += float(bids[i][0]) * float(bids[i][1]) * (1 - BINANCE_FEE) # 0.1% fee on binance
        i += 1
    return max_size, usdc_out

# on Osmosis, given amount of OSMO out, calculate how much USDC for swap in
def osmosis_usdc_in(amountOut, balanceIn, balanceOut):
    AmountIn = balanceIn * ((balanceOut/(balanceOut-amountOut)) - 1) * (1 + OSMOSIS_FEE) # 0.2% fee on Osmosis
    return AmountIn


def etherToNum(amount):
    return amount/1000000


# profit in USDC
def calculate_usdc_profit1(bids, osmosis_price, balanceIn, balanceOut):
    osmo_in_binance, usdc_out_binance = binance_find_max_osmo_sell(bids, osmosis_price)
    # print(f"the max amount of USDC I can sell on binance is {osmo_in_binance}, get {usdc_out_binance} USDC")
    usdc_in_osmosis = osmosis_usdc_in(osmo_in_binance, balanceIn, balanceOut)
    profit_in_usdc = usdc_out_binance - usdc_in_osmosis
    return profit_in_usdc
    

# if ask_price < Osmosis
#     buy on Binance and sell on Osmosis

# Binance: USDC -> OSMO ; Osmosis: OSMO -> USDC
# tokenIn = OSMO
# tokenOut = USDC

# assuming infinite liquidity on Osmosis

# given the ask_price < osmosis_price, find the max amount of OSMO to buy, also return the USDC traded in
def binance_find_max_osmo_buy(asks, osmosis_price):
    i = 0
    max_size = 0
    usdc_in = 0
    while float(asks[i][0]) < osmosis_price:
        max_size += float(asks[i][1])
        usdc_in += float(asks[i][0]) * float(asks[i][1]) #* (1 + BINANCE_FEE) # 0.1% fee on binance
        i += 1
    return usdc_in, max_size

# on Osmosis, given amount of OSMO in, calculate how much USDC swapped out
def osmosis_usdc_out(amountIn, balanceIn, balanceOut):
    AmountOut = balanceOut * (1 - (balanceIn/(balanceIn+amountIn))) * (1 - OSMOSIS_FEE) # 0.2% fee on Osmosis
    return AmountOut

def calculate_usdc_profit2(asks, osmosis_price, balanceIn, balanceOut):
    usdc_in_binance, osmo_out_binance = binance_find_max_osmo_buy(asks, osmosis_price)
    # print(f"the max amount of USDC I can buy on binance is {usdc_in_binance}, get {osmo_out_binance} OSMO")
    usdc_out_osmosis = osmosis_usdc_out(osmo_out_binance, balanceIn, balanceOut)
    # print(f"getting {usdc_out_osmosis} USDC on Osmosis")
    profit_in_usdc = usdc_out_osmosis - usdc_in_binance
    return profit_in_usdc

def main():
    # on block 8751002
    data = {"lastUpdateId": 37100665, "bids": [["0.88500000", "512.85000000"], ["0.88400000", "1685.41000000"], ["0.88300000", "2346.80000000"], ["0.88200000", "1800.04000000"], ["0.88100000", "1604.43000000"], ["0.88000000", "1417.84000000"], ["0.87900000", "59581.78000000"], ["0.87800000", "5956.70000000"], ["0.87700000", "8533.32000000"], ["0.87600000", "5829.77000000"], ["0.87500000", "9531.54000000"], ["0.87400000", "389.09000000"], ["0.87300000", "1872.47000000"], ["0.87200000", "596.33000000"], ["0.87100000", "2746.19000000"], ["0.87000000", "1364.11000000"], ["0.86900000", "1710.14000000"], ["0.86800000", "1017.46000000"], ["0.86700000", "25.44000000"], ["0.86600000", "577.37000000"]], "asks": [["0.88600000", "119.97000000"], ["0.88700000", "2520.97000000"], ["0.88800000", "6862.83000000"], ["0.88900000", "3859.50000000"], ["0.89000000", "2051.45000000"], ["0.89100000", "22563.99000000"], ["0.89200000", "3002.28000000"], ["0.89300000", "561.80000000"], ["0.89400000", "2880.73000000"], ["0.89500000", "10328.47000000"], ["0.89600000", "1468.95000000"], ["0.89700000", "2020.84000000"], ["0.89800000", "392.34000000"], ["0.89900000", "558.04000000"], ["0.90000000", "1176.46000000"], ["0.90100000", "483.50000000"], ["0.90200000", "1771.15000000"], ["0.90300000", "23.23000000"], ["0.90400000", "1216.03000000"], ["0.90500000", "568.95000000"]], "time": "2023-03-17 21:28:23.209057"}
    USDC_balance = 10554054313213
    OSMO_balance = 11938272258924

    bids = data["bids"]
    asks = data["asks"]

    osmosis_price = USDC_balance / OSMO_balance # 0.887
    highest_bid_price = float(bids[0][0])
    lowest_ask_price = float(asks[0][0])


    # sp_goal = highest_bid_price
    sp_now = osmosis_price # 0.884

    
    # if bid_price > Osmosis: balanceIn = USDC_balance, balanceOut = OSMO_balance
    if highest_bid_price > osmosis_price:
        print("bid_price > Osmosis, buy on Osmosis and sell on Binance")
        profit = calculate_usdc_profit1(bids, osmosis_price, USDC_balance, OSMO_balance)
        if profit > 0:
            print(f"the profit of the arb is {profit}")
        else:
            print("the arb is not profitable")


    # if ask_price < Osmosis: balanceIn = OSMO_balance, balanceOut = USDC_balance
    elif lowest_ask_price < osmosis_price:
        print("ask_price < Osmosis, buy on Binance and sell on Osmosis")
        profit = calculate_usdc_profit2(asks, osmosis_price, OSMO_balance, USDC_balance)
        if profit > 0:
            print(f"the profit of the arb is {profit}")
        else:
            print("the arb is not profitable")
    else:
        print("no arbitrage opportunity")


if __name__ == "__main__":
    main()