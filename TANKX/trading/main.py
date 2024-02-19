import redis
import json
from extended_threading import StoppableThread
import os 


redis_client = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT)

REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME')

def process_triangle(triangle):
    A, B, C = triangle.split("_")[0], triangle.split("_")[1], triangle.split("_")[2]
    #print(A,B,C)
    #try:
    bid_A = float(redis_client.hget(A, "bid"))
    bid_B = float(redis_client.hget(B, "bid"))
    bid_C = float(redis_client.hget(C, "bid"))

    ask_A = float(redis_client.hget(A, "ask"))
    ask_B = float(redis_client.hget(B, "ask"))
    ask_C = float(redis_client.hget(C, "ask"))
    #print(A,B,C)
    
    print("{A}, {B}, {C} triangular bid artibrage",bid_A*bid_B/bid_C)
    print("{A}, {B}, {C} triangular ask artibrage",ask_A*ask_B/ask_C)
    #except:pass



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
   