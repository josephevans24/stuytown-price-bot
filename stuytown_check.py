#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!/usr/bin/env python3
import os, requests
from twilio.rest import Client
from datetime import datetime, timezone

PRICE_CAP = float(os.getenv("PRICE_CAP", 6500))

URL = (
    "https://pd-di.beamliving.com/api/units"
    "?Order=low-price&Flex=false&Bedrooms=2"
    "&page=0&itemsOnPage=50"
    "&PropertyName=Stuyvesant+Town_Peter+Cooper+Village"
)

resp = requests.get(URL, timeout=20)
resp.raise_for_status()
units = resp.json()["unitModels"]   # list of dicts

matches = [
    u for u in units
    if u["bedrooms"] == 2 and u["price"] <= PRICE_CAP
]

if not matches:
    print(f"{datetime.now(timezone.utc)} – no matches")
    quit(0)

lines = [
    f'{u["building"]["buildingName"]} {u["unitNumber"]} – ${u["price"]:,}'
    for u in matches
]

body = f"StuyTown alert (≤ ${int(PRICE_CAP):,}):\n" + "\n".join(lines)

client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
client.messages.create(
    body=body,
    from_=os.getenv("TWILIO_FROM"),
    to=os.getenv("TWILIO_TO")
)

print("SMS sent:\n", body)


# In[ ]:




