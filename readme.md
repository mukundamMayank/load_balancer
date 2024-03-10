How to Run?

1) Use python3 backend<1..5> .py to first run all the backend servers.
2) Use python3 lb.py to run load balancers
3) Use "for i in {1..<number of requests>}; do curl http://localhost:5000/async_task & done" to run the asyncio tasks & "or i in {1..<number of requests>}; do curl http://localhost:5000/thread_task & done" to run thread tasks. This is a bash command so you just need to come inside the directory & run this command.
4) Make sure to make changes in lb.py to the for loop while creating threads & appending tasks to asyncio, according to number of requests.