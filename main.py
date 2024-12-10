import httpx
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


def get_models():
    res_models = httpx.get("https://targon.com/api/models")
    res_req = httpx.get("https://targon.com/api/stats/dail-requests")
    models = res_models.json()
    reqs = res_req.json()
    total_models = len(models)
    return f"Daily Stats\n{total_models} Models\n{reqs} Requests"


cg = CoinGeckoAPI()


def get_coin_prices():
    cg = CoinGeckoAPI()
    tao = cg.get_price(ids="bittensor", vs_currencies="usd")["bittensor"]["usd"]
    eth = cg.get_price(ids="ethereum", vs_currencies="usd")["ethereum"]["usd"]
    akt = cg.get_price(ids="akash-network", vs_currencies="usd")["akash-network"]["usd"]
    return f"{{67}} Tao Price:  {tao:.2f} {{68}}\n{{67}} Eth Price: {eth:.2f} {{68}}\n{{67}} AKT Price:    {akt:.2f} {{68}}"


dotenv.load_dotenv()

rw_client = vesta.ReadWriteClient(os.getenv("VEST_KEY", ""))
vbml_client = vesta.VBMLClient()

tick = 0

default = ""

while True:
    try:
        now_utc = datetime.now(pytz.utc).replace(microsecond=0)
        now_chicago = now_utc.astimezone(chicago_tz)
        curtime = str(now_chicago.strftime("%Y-%m-%d\n%H:%M:%S"))
        match tick:
            case tick if tick % 10 == 0:
                component_text = get_models()
            case tick if tick % 5 == 0:
                component_text = get_coin_prices()
            case _:
                component_text = default

        default = component_text
        print(tick, component_text)
        component = Component(
            f"{curtime}\n{component_text}",
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
