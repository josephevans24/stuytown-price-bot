#!/usr/bin/env python
# coding: utf-8

# In[12]:


 #!/usr/bin/env python3
"""
Pull the BeamLiving inventory JSON and e-mail yourself when
a 2-bedroom ≤ PRICE_CAP appears.
"""

import os, requests, smtplib, ssl
from email.message import EmailMessage
from datetime import datetime, timezone

PRICE_CAP = float(os.getenv("PRICE_CAP", 6500))

URL = (
    "https://pd-di.beamliving.com/api/units"
    "?Order=low-price&Flex=false&Bedrooms=2"
    "&page=0&itemsOnPage=50"
    "&PropertyName=Stuyvesant+Town_Peter+Cooper+Village"
)

resp = requests.get(URL, timeout=20).json()
units = resp["unitModels"]

matches = [
    u for u in units
    if u["bedrooms"] == 2 and u["price"] <= PRICE_CAP
]

if not matches:
    print(f"{datetime.now(timezone.utc)} – no matches")
    raise SystemExit(0)

lines = [
    f'{u["building"]["buildingName"]} {u["unitNumber"]} – ${u["price"]:,}'
    for u in matches
]

body = f"StuyTown alert (≤ ${int(PRICE_CAP):,}):\n" + "\n".join(lines)

msg = EmailMessage()
msg["Subject"] = "StuyTown price alert"
msg["From"]    = os.getenv("EMAIL_FROM")
msg["To"]      = os.getenv("EMAIL_TO")
msg.set_content(body)

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")), context=ctx) as s:
    s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
    s.send_message(msg)

print("E-mail sent:\n", body)


# In[ ]:




