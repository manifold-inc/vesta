import vesta
import dotenv
import os
import time
from pycoingecko import CoinGeckoAPI
from vesta.vbml import Component
dotenv.load_dotenv()

rw_client = vesta.ReadWriteClient(os.getenv('VEST_KEY', ''))
vbml_client = vesta.VBMLClient()

while True:
    cg = CoinGeckoAPI()
    tao = cg.get_price(ids='bittensor', vs_currencies='usd')['bittensor']['usd']
    eth = cg.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']

    component = Component(
            f"{{67}} Tao Price: {tao} {{68}}\n{{67}} Eth Price: {eth} {{68}}",
        justify="center",
        align="center",
        width=22,
        height=6,
    )

    rw_client.write_message(vbml_client.compose([component]))
    time.sleep(5)
