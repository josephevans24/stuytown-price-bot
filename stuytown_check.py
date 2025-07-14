#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python3
import os, re, json, requests
from datetime import datetime, timezone
from twilio.rest import Client
from bs4 import BeautifulSoup          # new dependency

PRICE_CAP = float(os.getenv("PRICE_CAP", 6500))
LIST_URL  = ("https://www.stuytown.com/nyc-apartments-for-rent/"
             "?Order=low-price&Bedrooms=2&Flex=false")

html = requests.get(LIST_URL, timeout=20).text

# ---- pull JSON blob -------------------------------------------------
m = re.search(r"window\.__PRELOADED_STATE__\s*=\s*({.*?});", html, re.S)
if not m:
    raise RuntimeError("Failed to locate JSON state in page")

state = json.loads(m.group(1))
units  = state["listings"]["units"]          # path confirmed via dev-tools

matches = [u for u in units
           if u["bedrooms"] == 2 and u["marketRent"] <= PRICE_CAP]

if not matches:
    print(f"{datetime.now(timezone.utc)} – no matches")
    quit(0)

lines = [f'{u["buildingName"]} {u["unitName"]} – ${u["marketRent"]:,}'
         for u in matches]
body = f"StuyTown alert (≤ ${int(PRICE_CAP):,}):\n" + "\n".join(lines)

client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
client.messages.create(
    body=body,
    from_=os.getenv("TWILIO_FROM"),
    to=os.getenv("TWILIO_TO")
)

print("SMS sent:\n", body)


# In[ ]:




