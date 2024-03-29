
import os
# To get the value of an environment variable
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')
MAX_NUMBER_OF_SYMBOLS = int(os.getenv('MAX_NUMBER_OF_SYMBOLS'))



from binance import ThreadedWebsocketManager
import json
import numpy as np
import redis
from utils import get_triangles_and_symbols

with open("all_triangles.json", "r") as json_file:
    all_triangles = json.load(json_file)
# Define a function that will handle incoming WebSocket messages
    


redis_client = redis.Redis(host='redis', port=6379)

discrepancy_dict = {f"{A}_{B}_{C}":0 for A,B,C in all_triangles}




cnt = 0
print(cnt,"cnt")
def process_message(msg):
    global cnt
    global discrepancy_dict
    #global redis_client
    if cnt%100 == 0:
        discrepancy_dict = dict(sorted(discrepancy_dict.items(), key=lambda item: item[1],reverse=True))
        top_n_triangles, top_n_symbols = get_triangles_and_symbols(discrepancy_dict, MAX_NUMBER_OF_SYMBOLS)
        
        redis_client.set('top_n_triangles', json.dumps(top_n_triangles))
        redis_client.set('top_n_symbols', json.dumps(list(top_n_symbols)))
    
    
    msg_dict = {}
    for i in msg:
        msg_dict[i['s']] = i
    msg_symbols = set(list(msg_dict.keys()))
    for triangle in all_triangles:
        A,B,C = triangle[0], triangle[1], triangle[2]
        import logging
        #logging.warning(f"{A}_{B}_{C}")
        #logging.warning(list(msg_symbols)[:2])
        pair_A, pair_B, pair_C = A+B, B+C, A+C
        if set([pair_A, pair_B, pair_C]) <= msg_symbols:
            
            
            bid_arbitrage = np.abs(1-float(msg_dict[pair_A]['b']) *float(msg_dict[pair_B]['b']) / float(msg_dict[pair_C]['b']))
            ask_arbitrage = np.abs(1-float(msg_dict[pair_A]['a']) *float(msg_dict[pair_B]['a'] )/ float(msg_dict[pair_C]['a']))
            discrepancy_dict[f"{A}_{B}_{C}"] += bid_arbitrage + ask_arbitrage
            


    
twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
twm.start()
twm.start_ticker_socket(callback=process_message)

twm.join()