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
chicago_tz = pytz.timezone('America/Chicago')

# Format the output

dotenv.load_dotenv()

rw_client = vesta.ReadWriteClient(os.getenv('VEST_KEY', ''))
vbml_client = vesta.VBMLClient()

tick = 1
cg = CoinGeckoAPI()
tao = cg.get_price(ids='bittensor', vs_currencies='usd')['bittensor']['usd']
eth = cg.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']

while True:
    if tick % 5 == 0:
        cg = CoinGeckoAPI()
        tao = cg.get_price(ids='bittensor', vs_currencies='usd')['bittensor']['usd']
        eth = cg.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']

    now_utc = datetime.now(pytz.utc)
    now_chicago = now_utc.astimezone(chicago_tz)
    now_chicago.strftime("%Y-%m-%d %H:%M:%S %Z")

    component = Component(
            f"{now_chicago}\n{{67}} Tao Price:  {tao} {{68}}\n{{67}} Eth Price: {eth} {{68}}",
        justify="center",
        align="center",
        width=22,
        height=6,
    )

    rw_client.write_message(vbml_client.compose([component]))
    time.sleep(1)
