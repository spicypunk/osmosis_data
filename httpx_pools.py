import httpx
import json
import pandas as pd
import logging
import time

df_pool = pd.DataFrame()

heightest_block = 8292971


for block_height in range(8292950, heightest_block+1):
    retry_count = 0
    while retry_count < 5:
        try:
            response = httpx.get(
                'https://osmosisarchive-lcd.quickapi.com/osmosis/gamm/v1beta1/pools/1'
            )
            response.raise_for_status()  # Raise an exception for non-200 status codes
            response = response.json() # parse response into a dictionary
        except (httpx.HTTPError, json.JSONDecodeError) as e:
            print(f"Error: {e}. Retrying in {60} seconds...")
            retry_count += 1
            time.sleep(60)
            continue  # Continue to the next iteration of the loop if an exception occurs
    if retry_count == 5:
        print(f"Max retries exceeded for block height {block_height}. Skipping...")
        continue
    
    pool_assets = response["pool"]['pool_assets']
    #print(pool_assets)


    # get current pool assets (denom, pool balance, weight)
    osmo_atom_pool_asset1 = pool_assets[0] # a dictionary of the first pool asset
    osmo_atom_pool_asset2 = pool_assets[1] # a dictionary of the second pool asset

    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    osmo_atom_pool_asset1 = flatten_dict(osmo_atom_pool_asset1)
    osmo_atom_pool_asset2 = flatten_dict(osmo_atom_pool_asset2)

    header0 = ['block_height']
    df_0 = pd.DataFrame({'block_height': block_height}, columns=header0, index=[0])
    

    header1 = list(osmo_atom_pool_asset1.keys()) # get a list of keys of the dictionary (atom_pool_asset1)
    df_1 = pd.DataFrame(osmo_atom_pool_asset1, columns=header1, index=[0])


    header2 = header1
    df_2 = pd.DataFrame(osmo_atom_pool_asset2, columns=header2, index=[0])

    df = pd.concat([df_0, df_1, df_2], axis=1)


    df_pool = pd.concat([df_pool, df], axis=0)
    

print(df_pool)