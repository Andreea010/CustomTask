import time
import flask
import threading
import requests
import random

queue = []
app = flask.Flask(__name__)
extractor_threads = 4
generator_threads = 8
counter = 0


@app.put("/api/")
def func():
    global queue
    queue.append(flask.request.json)
    print(queue.pop())

def produce():
    global queue
    global counter
    while True:
        while start_condition:
            counter = random.randint(1, 10)
            queue.post(counter)
            time.sleep(random.random())

def extract(Consumer):
    global queue
    while True:
            requests.post(Consumer, json=produce())


generators = [threading.Thread(target=produce) for i in range(generator_threads)]
start_condition = False

if __name__ == '__main__':
    for thread in generators:
        thread.start()
    app.run(host='127.0.0.1', port=5001)