import vesta
import dotenv
import os
import time
from pycoingecko import CoinGeckoAPI
from vesta.vbml import Component
from datetime import datetime
import pytz

# Get the current time in UTC

# Convert to Chicago timezone
chicago_tz = pytz.timezone("America/Chicago")

# Format the output

dotenv.load_dotenv()

rw_client = vesta.ReadWriteClient(os.getenv("VEST_KEY", ""))
vbml_client = vesta.VBMLClient()

tick = 1
cg = CoinGeckoAPI()
tao = cg.get_price(ids="bittensor", vs_currencies="usd")["bittensor"]["usd"]
eth = cg.get_price(ids="ethereum", vs_currencies="usd")["ethereum"]["usd"]
akt = cg.get_price(ids="akash-network", vs_currencies="usd")["akash-network"]["usd"]
while True:
    try:
        if tick % 5 == 0:
            cg = CoinGeckoAPI()
            tao = cg.get_price(ids="bittensor", vs_currencies="usd")["bittensor"]["usd"]
            eth = cg.get_price(ids="ethereum", vs_currencies="usd")["ethereum"]["usd"]
            akt = cg.get_price(ids="akash-network", vs_currencies="usd")[
                "akash-network"
            ]["usd"]

        now_utc = datetime.now(pytz.utc).replace(microsecond=0)
        now_chicago = now_utc.astimezone(chicago_tz)
        now_chicago.strftime("%Y-%m-%d\n%H:%M:%S")[:-6]

        component = Component(
            f"{now_chicago}\n{{67}} Tao Price:  {tao:.2f} {{68}}\n{{67}} Eth Price: {eth:.2f} {{68}}\n{{67}} AKT Price:    {akt:.2f} {{68}}",
            justify="center",
            align="center",
            width=22,
            height=6,
        )

        rw_client.write_message(vbml_client.compose([component]))
        tick += 1
        time.sleep(16)
    except Exception as e:
        print(e)
