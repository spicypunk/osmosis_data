import json
import csv
import subprocess
import pandas as pd
import asyncio

# Function to run the subprocess asynchronously
async def run_subprocess(cmd):
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, stderr=stderr.decode())
    return stdout.decode().strip()

# Define the function that performs the CLI interaction
# /Users/bethie/go/bin/osmosisd query gamm pool 678 --height 6639544
async def interact_with_cli(block_height):
    cmd = ["/Users/bethie/go/bin/osmosisd", "query", "gamm", "pools", "--height", str(block_height), "-o", "json"]
    output = await run_subprocess(cmd)
    data = json.loads(output)
    data_list = list(data)
    values = []

    for key in data_list:
        value = data[key]
        values.append(value)

    pools_data = values[0]
    osmo_atom = pools_data[0]
    osmo_atom_pool_asset1 = osmo_atom['pool_assets'][0]
    osmo_atom_pool_asset2 = osmo_atom['pool_assets'][1]

    # flatten out the nested dictionary
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

    header1 = list(osmo_atom_pool_asset1.keys())
    df_1 = pd.DataFrame(osmo_atom_pool_asset1, columns=header1, index=[0])

    header2 = list(osmo_atom_pool_asset2.keys())
    df_2 = pd.DataFrame(osmo_atom_pool_asset1, columns=header2, index=[0])

    df = pd.concat([df_1, df_2], axis=1)

    return df

async def main():
    df_pool = pd.DataFrame()
    heightest_block = 8292971
    tasks = []

    # Create a list of tasks to run the subprocess calls in parallel
    for block_height in range(6292900, heightest_block+1):
        tasks.append(asyncio.create_task(interact_with_cli(block_height)))

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    # Combine the results into a single DataFrame
    df_pool = pd.concat(results, axis=0)

    print(df_pool)

# Run the main function asynchronously
asyncio.run(main())