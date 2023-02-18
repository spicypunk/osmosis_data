import httpx
import json
import pandas as pd
import asyncio


# Sometimes faulty: missing rows for dataframe, might the problem be the async?
limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
httpx_client = httpx.Client(limits=limits)

async def fetch_data(block_height):
    tries = 0
    while tries < 5:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"https://osmosisarchive-lcd.quickapi.com/osmosis/gamm/v1beta1/pools/1?height={block_height}")
                if response.status_code == 200:
                    response = response.json() # parse response into the dictionary
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
                elif response.status_code == 429:
                    print(f"Too many requests at block height {block_height}. Retrying in 2 seconds.")
                    await asyncio.sleep(2)
                else:
                    print(f"HTTP error occurred at block height {block_height}: {response.status_code}")
                    tries += 1
                    await asyncio.sleep(2)
                
        except (httpx.HTTPError, json.JSONDecodeError) as e:
            if httpx.HTTPError:
                print(f"HTTP error occurred at block height {block_height}: {e}")
            elif json.JSONDecodeError:
                print(f"JSONDecode error occurred at block height {block_height}: {e}")
            tries += 1
            await asyncio.sleep(2)
    return None

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
    for block_height in range(8292900, heightest_block+1):
        tasks.append(asyncio.ensure_future(fetch_data(block_height)))
    df_list = await asyncio.gather(*tasks)
    for df in df_list:
        if df is not None:
            df_pool = pd.concat([df_pool, df], axis=0)
    print(df_pool)

if __name__ == "__main__":
    asyncio.run(main())
