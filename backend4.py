from flask import Flask
import time
import asyncio

app = Flask(__name__)

@app.route('/thread_task')
def index_thread():
	print("one")
	# time.sleep(4)
	print("two")
	return "thread backend 4"


@app.route('/async_task')
async def index_async():
	print("one")
	# await asyncio.sleep(4)
	print("two")
	return "async backend 4"

if __name__ == '__main__':
    app.run(port=5004)
