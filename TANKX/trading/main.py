import redis
import json
from extended_threading import StoppableThread
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME')
redis_client = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT)


def process_triangle(triangle):
    A, B, C = triangle.split("_")[0], triangle.split("_")[1], triangle.split("_")[2]
    try:    
        bid_A = float(redis_client.hget(A, "bid"))
        bid_B = float(redis_client.hget(B, "bid"))
        bid_C = float(redis_client.hget(C, "bid"))
        opportunity = bid_A*bid_B/bid_C
        if opportunity>1:
            print(f"{A}, {B}, {C} triangular bid artibrage",opportunity)
    except TypeError:
        pass

    try:
        ask_A = float(redis_client.hget(A, "ask"))
        ask_B = float(redis_client.hget(B, "ask"))
        ask_C = float(redis_client.hget(C, "ask"))
        opportunity = ask_A*ask_B/ask_C
        if opportunity<1:
            print(f"{A}, {B}, {C} triangular ask artibrage",opportunity)
        

    except TypeError:
        pass




threads = {}


while True:
    best_triangles = json.loads(redis_client.get('top_n_triangles'))
    best_triangles_set = set(['_'.join(triangle) for triangle in best_triangles])

    to_be_run = best_triangles_set- set(threads.keys())
    to_be_stopped =  set(threads.keys()) - best_triangles_set


    # Create and start the thread with a target function
    for triangle in to_be_run:
        thread_key = triangle
        threads[thread_key] = StoppableThread(target=process_triangle, args= (triangle,))
        threads[thread_key].start()
    
    for triangle in to_be_stopped:
        thread_key = triangle
        threads[thread_key].stop()
        threads[thread_key].join()
        del threads[thread_key]
   