
import json
import csv
import subprocess
import pandas as pd


## The capture_output=True, which means that the output of the command will be captured and stored 
# in the stdout attribute of the result object. The text=True, the output is returned as a string 
# instead of bytes. "-o json" tells the command to output the results in JSON format

#/Users/bethie/go/bin/osmosisd q gamm pools --height 8292971 -o json

p1 = subprocess.run(["/Users/bethie/go/bin/osmosisd", "query", "gamm", "pools",
                              "-o", "json"], capture_output=True, text=True)


#print(p1.stdout)

# Load the JSON object from the stdout
data = json.loads(p1.stdout) # data is a dictionary
data_list = list(data) # list of dictionary keys
#print(data_list)
values = [] # list to store values

for key in data_list:
    value = data[key]
    values.append(value)

pools_data = values[0] # a list of dictionaries (pool), individual pools are dictionaries pools_data[i]
# for example pools_data[0] is a dictionary of the first pool (OSMO-ATOM)
osmo_atom = pools_data[0] # a dictionary of the first pool (OSMO-ATOM)

# get current pool assets (denom, pool balance, weight)
osmo_atom_pool_asset1 = osmo_atom['pool_assets'][0] # a dictionary of the first pool asset
osmo_atom_pool_asset2 = osmo_atom['pool_assets'][1] # a dictionary of the second pool asset

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
print(osmo_atom_pool_asset2)

header1 = list(osmo_atom_pool_asset1.keys()) # get a list of keys of the dictionary (atom_pool_asset1)
df_1 = pd.DataFrame(osmo_atom_pool_asset1, columns=header1, index=[0])

header2 = list(osmo_atom_pool_asset2.keys()) # get a list of keys of the dictionary (atom_pool_asset2)
df_2 = pd.DataFrame(osmo_atom_pool_asset1, columns=header2, index=[0])


df = pd.concat([df_1, df_2], axis=1)

print(df)

# with open('output.csv', mode='w') as csv_file:
#     # Create a CSV writer object
#     writer = csv.writer(csv_file)

#     # Write the header row to the CSV
#     writer.writerow(header)

#     # Write each row to the CSV
#     re_values = list(osmo_atom_pool_asset1.values())
#     writer.writerow(re_values)

#     # for key in osmo_atom_pool_asset2:
#     #     print(osmo_atom_pool_asset2[key])

