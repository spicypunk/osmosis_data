import asyncio
from websockets import connect
import aiofiles
import sys
import json
import httpx
import datetime
import pytz


async def orderbook_download(pair):
    
    pair_lower = pair.lower()
    websocket_url = f"wss://stream.binance.com:9443/ws/{pair_lower}@depth"
    rest_url = f"https://data.binance.com/api/v3/depth"

    params = {
        "symbol": pair.upper(),
        "limit" : 20
    }
    
    async with httpx.AsyncClient() as client:
        while True:
            snapshot = await client.get(rest_url, params=params)
            snapshot = snapshot.json()
            snapshot["time"] = datetime.datetime.now(pytz.timezone('GMT')).strftime("%Y-%m-%d %H:%M:%S.%f")
            print(snapshot)

            async with aiofiles.open(f"{pair_lower}-snapshots.txt", mode = 'a') as f:
                await f.write(json.dumps(snapshot) + '\n')


    # async with connect(websocket_url) as websocket:
    #     while True:
    #         data = await websocket.recv()
    #         print(data)

    #         async with aiofiles.open(f"{pair_lower}-updates.txt", mode = 'a') as f:
    #             await f.write(data + '\n')

    pass

asyncio.run(orderbook_download("OSMOUSDT"))