,
import os

# To get the value of an environment variable
api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')
MAX_NUMBER_OF_SYMBOLS = os.getenv('MAX_NUMBER_OF_SYMBOLS')



from binance import ThreadedWebsocketManager
import json
import numpy as np
import redis
from utils import get_triangles_and_symbols
import logging
import time
time.sleep(3)

with open("all_triangles.json", "r") as json_file:
    all_triangles = json.load(json_file)
# Define a function that will handle incoming WebSocket messages
    


redis_client = redis.Redis(host='redis', port=6379)

discrepancy_dict = {f"{A}_{B}_{C}":0 for A,B,C in all_triangles}

#def update_redis(top_n_triangles, top_n_symbols):



cnt = 0
print(cnt,"cnt")
def process_message(msg):
    global cnt
    global discrepancy_dict
    #global redis_client
    if cnt%100 == 0:
        discrepancy_dict = dict(sorted(discrepancy_dict.items(), key=lambda item: item[1],reverse=True))
        top_n_triangles, top_n_symbols = get_triangles_and_symbols(discrepancy_dict, MAX_NUMBER_OF_SYMBOLS)
        #logging.warning("top_n_triangles")
        #logging.warning(top_n_triangles[:3])
        #logging.warning(list(top_n_symbols)[:3])
        
        redis_client.set('top_n_triangles', json.dumps(top_n_triangles))
        redis_client.set('top_n_symbols', json.dumps(list(top_n_symbols)))
    
    
    msg_dict = {}
    for i in msg:
        msg_dict[i['s']] = i
    msg_symbols = set(list(msg_dict.keys()))
    for triangle in all_triangles:
        A,B,C = triangle[0], triangle[1], triangle[2]
        #logging.warning(set([A+B, B+C, A+C]))
        #logging.warning(msg_symbols)
        if set([A, B, C]) <= msg_symbols:
            
            #logging.warning("HEY")
            #logging.warning(msg_dict[A+B])
            #logging.warning(type(msg_dict[A+B]['b']))
            bid_arbitrage = np.abs(1-float(msg_dict[A]['b']) *float(msg_dict[B]['b']) / float(msg_dict[C]['b']))
            ask_arbitrage = np.abs(1-float(msg_dict[A]['a']) *float(msg_dict[B]['a'] )/ float(msg_dict[C]['a']))
            discrepancy_dict[f"{A}_{B}_{C}"] += bid_arbitrage + ask_arbitrage
            


    
twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
twm.start()
twm.start_ticker_socket(callback=process_message)

twm.join()