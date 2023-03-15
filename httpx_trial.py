import httpx
r = httpx.get('https://osmosisarchive-lcd.quickapi.com/osmosis/blocks')
print(r.text)