import vesta
import dotenv
import os
import time
from pycoingecko import CoinGeckoAPI
dotenv.load_dotenv()

rw_client = vesta.ReadWriteClient(os.getenv('VEST_KEY', ''))

while True:
    cg = CoinGeckoAPI()
    price = cg.get_price(ids='bittensor', vs_currencies='usd')['bittensor']['usd']
    time.sleep(5)
    message = vesta.encode_text(f"{{67}} Tao Price: {price} {{68}}")
    rw_client.write_message(message)
