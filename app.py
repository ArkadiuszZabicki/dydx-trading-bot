from dydx3 import Client
from dydx3.constants import API_HOST_SEPOLIA
from dydx3.constants import NETWORK_ID_MAINNET
from web3 import Web3
from pprint import pprint
from datetime import datetime, timedelta

# public_client = Client(
#     host='http://localhost:8080',
# )
# public_client.public.get_markets()

# Constants

ETHEREUM_ADDRESS = '0xCc91ce56c9ca9cAAb0085929536A16Fe84b759d8'
ETH_PRIVATE_KEY = "0x006b3205574f6d437ac3f71f8ae8c0d4bbafb3b89cce7a79a4462449e57e28a2"
STARK_PRIVATE_KEY = '0550f1beb2b224e1796b61f31eeef07f775341204c8e816f140c265c0229731e'
DYDX_API_KEY = 'e9e440db-c06d-a6d0-984d-0e58c6f93f2d'
DYDX_API_SECRET = '5iPNXwk5Or2PgWvNixDgEmLU6EBYbkfrGwAf7NZO'
DYDX_API_PASSPHRASE = "ckVb2Ftlz-stGJldN6_b"

# HTTP Provider
HTTP_PROVIDER = 'https://eth-sepolia.g.alchemy.com/v2/LVbGmwBdnH5jBQuj_LOAuFYm1aRWXyGm'

# Create client connection

client = Client(
    host = API_HOST_SEPOLIA,
    
    api_key_credentials = {
        'key': DYDX_API_KEY,
        'secret': DYDX_API_SECRET,
        'passphrase': DYDX_API_PASSPHRASE
    },
    stark_private_key = STARK_PRIVATE_KEY,
    eth_private_key = ETH_PRIVATE_KEY,
    default_ethereum_address = ETHEREUM_ADDRESS,
    web3 = Web3(Web3.HTTPProvider(HTTP_PROVIDER))
)

# Check connection
account = client.private.get_account()
account_id = account.data['account']['id']
quote_balance = account.data['account']['quoteBalance']

print('Connection successful')
print('Account id: ' + account_id)
print('Quote balance: ' + quote_balance)

# OHLC Candlestic data

candles = client.public.get_candles(
    market = 'BTC-USD',
    resolution = '1HOUR',
    limit = 3
    )

#pprint(candles.data)

# GET position id

account_response = client.private.get_account()
position_id = account_response.data['account']['positionId']

print(position_id)
print(account_response.data['account'])

# GET expiration time
server_time = client.public.get_time()
expiration = datetime.fromisoformat(server_time.data['iso'].replace('Z', '')) + timedelta(seconds=3600 + 70)
server_time.data

#Place an order
place_order = client.private.create_order(
    position_id=position_id, # required for creating the order signature
    market="BTC-USD",
    side="BUY",
    order_type="MARKET",
    post_only=False,
    size='0.001',
    price='100000',
    limit_fee='0.015',
    expiration_epoch_seconds=expiration.timestamp(),
    time_in_force="FOK", 
    reduce_only=False
)
    
#PPrint order



print(position_id)
print(server_time.data)
print(expiration)
pprint(place_order.data)
