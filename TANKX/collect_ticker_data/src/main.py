

import os

# To get the value of an environment variable
api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME')



from binance.client import Client
from binance import ThreadedWebsocketManager
import os
import redis
import json
import logging
#import nest_asyncio
#nest_asyncio.apply()

# Your existing code to initialize and start the ThreadedWebsocketManager goes here
import time
time.sleep(3)

# Initialize the client
client = Client(api_key, api_secret)
redis_client = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT)

# Placeholder for storing the latest data for each symbol



def write_to_redis(msg):
    """Process incoming bookTicker messages."""
    #print(msg["s"])
    redis_client.hset(msg["s"], "bid", msg["b"])
    redis_client.hset(msg["s"], "ask", msg["a"])

def remove_from_redis(symbol):
    """Remove bid and ask fields for a symbol from Redis."""
    
    # Remove specific fields for the symbol
    redis_client.delete(symbol)


# Initialize the ThreadedWebsocketManager
twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
twm.start()

# Start bookTicker websocket for each symbol
threads= {}

while True:
    try:

        symbols = set(json.loads(redis_client.get('top_n_symbols')))

    except:
        symbols = set()
    #logging.warning(list(symbols)[:3])
    to_be_run = symbols- set(threads.keys())
    to_be_stopped =  set(threads.keys()) - symbols
    #logging.warning("to_be_run")
    #logging.warning(to_be_run)
    #logging.warning("to_be_stopped")
    #logging.warning(to_be_stopped)

    for symbol in to_be_run:
        conn_key = twm.start_symbol_book_ticker_socket(callback=write_to_redis, symbol=symbol)
        threads[symbol] = conn_key

    for symbol in to_be_stopped:
        twm.stop_socket(threads[symbol])
        del threads[symbol]
        remove_from_redis(symbol)
    
    #logging.warning("len_threads")
#twm.join()
