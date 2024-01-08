from datetime import datetime, timedelta
import time
from pprint import pprint
from func_utils import format_number
# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
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
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK", 
        reduce_only=reduce_only
    )

    return place_order.data

# Abort all positions
def abort_all_positions(client):
    print('Cancelling all orders')
    client.private.cancel_all_orders()

    # Protect API
    time.sleep(0.5)

    # Get markets for reference of tick size

    markets = client.public.get_markets().data
    print('Getting market data')
    #pprint(markets)
    time.sleep(0.5)

    # Get all open positions
    positions = client.private.get_positions(status='OPEN')
    print(positions)
    all_positions = positions.data['positions']
    print(all_positions)
    # Handle all open positions
    close_orders = []
    if len(all_positions) > 0:
        #Loop through each position
        for position in all_positions:
            market = position['market']

            side = 'BUY'
            if position['side'] == 'LONG':
                side = 'SELL'
            print(market, side)

            price = float(position['entryPrice'])
            accept_price = price * 1.7 if side == 'BUY' else price * 0.3
            tick_size = markets['markets'][market]['tickSize']
            accept_price = format_number(accept_price, tick_size)

            order = place_market_order(
                client,
                market,
                side,
                position['sumOpen'],
                accept_price,
                True
            )

            close_orders.append(order)

            time.sleep(0.2)
    return close_orders


