#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python3
import os, json, requests
from datetime import datetime, timezone
from twilio.rest import Client

PRICE_CAP = float(os.getenv("PRICE_CAP", 6500))

URL = ("https://www.stuytown.com/api/availability"
       "?beds=2&flex=false&sort=low-price")  # observed XHR endpoint

r = requests.get(URL, timeout=15)
r.raise_for_status()
units = [u for u in r.json()["units"]
         if u["bedrooms"] == 2 and u["marketRent"] <= PRICE_CAP]

if not units:
    print(f"{datetime.now(timezone.utc)} – no matches")
    quit(0)

lines = [f"{u['buildingName']} {u['unitName']} – ${u['marketRent']:,}"
         for u in units]
body = "StuyTown alert (≤ ${:,}):\n{}".format(int(PRICE_CAP),
                                              "\n".join(lines))

client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
client.messages.create(
    body=body,
    from_=os.getenv("TWILIO_FROM"),
    to=os.getenv("TWILIO_TO")
)
print(f"Sent SMS:\n{body}")

