import time
import flask
import threading
import requests

queue = []
app = flask.Flask(__name__)
extractor_threads = 1

@app.post("/api/")
def func():
    global queue
    queue.append(flask.request.json)
    print(flask.request.json)
    return flask.jsonify({"status": "success"})

def extractor():
    global queue
    time.sleep(1)
    while True:
        if len(queue) > 0:
                item = queue.pop()
                requests.put("http://localhost:5001/api/", json=item)
                time.sleep(1)



extractors = [threading.Thread(target=extractor) for i in range(extractor_threads)]

if __name__ == '__main__':
    for thread in extractors:
        thread.start()
    app.run(host='127.0.0.1', port=5002)