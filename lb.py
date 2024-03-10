from flask import Flask
import requests
import threading
import random
import time
import heapq
import asyncio

app = Flask(__name__)

BACKEND_SERVERS = [
    {'url': 'http://localhost:6001', 'busy': False, 'number': 1, 'served_request':0, 'response_time':0, 'avg_response_time': 0},
    {'url': 'http://localhost:5002', 'busy': False, 'number': 2, 'served_request':0, 'response_time':0, 'avg_response_time': 0},
    {'url': 'http://localhost:5003', 'busy': False, 'number': 3, 'served_request':0, 'response_time':0, 'avg_response_time': 0},
    {'url': 'http://localhost:5004', 'busy': False, 'number': 4, 'served_request':0, 'response_time':0, 'avg_response_time': 0},
    {'url': 'http://localhost:5005', 'busy': False, 'number': 5, 'served_request':0, 'response_time':0, 'avg_response_time': 0}
]

## Round robin
def send_request():
    global server
    response = requests.get(BACKEND_SERVERS[server])
    print(" server number is " + str(server))
    server = (server+1)%(len(BACKEND_SERVERS))
    return response.text

## thread task
def send_request_thread(server):
    start = time.time()
    response = requests.get(server['url']+'/thread_task')
    end = time.time()
    server['response_time']+=(end-start)*1000
    # print(response.text)
    # return response.text

## async task
async def send_request_async(server):
    start = time.time()
    response = requests.get(server['url']+'/async_task')
    end = time.time()
    server['response_time'] += (end - start) * 1000
    server['busy'] = False
    server['served_request']-=1
    # print(response.text)
    # return response.text


@app.route('/thread_task')
def index_thread():
    program_start_time = time.perf_counter()
    threads = []
    for i in range(100):
        for server in BACKEND_SERVERS:
            if not server['busy'] and server['served_request']<20:
                server['busy'] = True
                server['served_request']+=1
                thread = threading.Thread(target=send_request_thread, args=(server,))
                thread.start()
                threads.append((thread, server))
                break

    for thread, server in threads:
        thread.join()
        server['busy'] = False
        server['served_request']-=1


    program_end_time = time.perf_counter() - program_start_time
    print(" total time for thread task is ", str(program_end_time))

    return "All requests completed"

@app.route('/async_task')
async def index_async():
    program_start_time = time.perf_counter()
    tasks = []
    for i in range(100):
        for server in BACKEND_SERVERS:
            if not server['busy'] and server['served_request'] < 20:
                server['busy'] = True
                server['served_request'] += 1
                tasks.append(send_request_async(server))

    responses = await asyncio.gather(*tasks)

    program_end_time = time.perf_counter() - program_start_time
    print(" total time for async task is  ", str(program_end_time))

    return "All requests completed"

if __name__ == '__main__':
    app.run(port=5000)