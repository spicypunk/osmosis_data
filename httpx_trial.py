import httpx
r = httpx.get('https://api.osmosis.zone/pools/v2/volume/678/chart')
print(r.text)