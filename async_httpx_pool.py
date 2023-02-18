import httpx
import json
import pandas as pd
import asyncio


# Sometimes faulty: missing rows for dataframe, might the problem be the async?
limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
httpx_client = httpx.Client(limits=limits)

async def fetch_data(block_height):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://osmosisarchive-lcd.quickapi.com/osmosis/gamm/v1beta1/pools/1?height={block_height}")
            response = response.json() # parse response into the dictionary
    except json.JSONDecodeError as e:
        # Catch the exception and print an error message
        #print(f"Error decoding JSON data at block height {block_height}: {e}")
        return None

    pool_assets = response["pool"]['pool_assets']
    # get current pool assets (denom, pool balance, weight)
    osmo_atom_pool_asset1 = pool_assets[0] # a dictionary of the first pool asset
    osmo_atom_pool_asset2 = pool_assets[1] # a dictionary of the second pool asset
    osmo_atom_pool_asset1 = flatten_dict(osmo_atom_pool_asset1)
    osmo_atom_pool_asset2 = flatten_dict(osmo_atom_pool_asset2)
    header0 = ['block_height']
    df_0 = pd.DataFrame({'block_height': block_height}, columns=header0, index=[0])
    header1 = list(osmo_atom_pool_asset1.keys()) # get a list of keys of the dictionary (atom_pool_asset1)
    df_1 = pd.DataFrame(osmo_atom_pool_asset1, columns=header1, index=[0])
    header2 = header1
    df_2 = pd.DataFrame(osmo_atom_pool_asset2, columns=header2, index=[0])
    df = pd.concat([df_0, df_1, df_2], axis=1)
    return df

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

async def main():
    df_pool = pd.DataFrame()
    heightest_block = 8292971
    tasks = []
    for block_height in range(8292950, heightest_block+1):
        tasks.append(asyncio.ensure_future(fetch_data(block_height)))
    df_list = await asyncio.gather(*tasks)
    for df in df_list:
        if df is not None:
            df_pool = pd.concat([df_pool, df], axis=0)
    print(df_pool)

if __name__ == "__main__":
    asyncio.run(main())
