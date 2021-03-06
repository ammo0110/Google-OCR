"""
API instruction manual at https://cloud.google.com/vision/docs/ocr
"""

import requests
import json
import sys
import base64

import threading
import queue

def request_document(api_key, infp):
    # Get image file in base64 encoding
    content = base64.b64encode(infp.read()).decode()
    url = "https://vision.googleapis.com/v1/images:annotate?key={:s}".format(api_key)

    # Prepare request body
    request = {}
    request["image"] = {"content": content}
    request["features"] = [{"type": "DOCUMENT_TEXT_DETECTION"}]
    body = {"requests": [request]}

    # Send the request
    response = requests.post(url, data=json.dumps(body), headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return (True, json.loads(response.text))
    else:
        print("Error encountered, status code {:d}. Please check output file for more details".format(response.status_code))
        return (False, json.loads(response.text))

def full_annotate_text(api_key, infp, outfp=sys.stdout, paragraph_sep=1):
    retstatus, document = request_document(api_key, infp)
    if not retstatus:
        print(document, file=outfp)
        return
    # Since we will only send one request, we will always receive only one response
    response = document["responses"][0]
    # Structure of response is {pages:[blocks:[paragraphs:[words:[symbols:[text]]]]]}
    for page in response["fullTextAnnotation"]["pages"]:
        for block in page["blocks"]:
            for paragraph in block["paragraphs"]:
                words = []
                for word in paragraph["words"]:
                    symbols = []
                    for symbol in word["symbols"]:
                        symbols.append(symbol["text"])
                        try:
                            brktype = symbol["property"]["detectedBreak"]["type"]
                            symbols.append(" ")
                        except KeyError:
                            pass
                    words.append("".join(symbols))
                print("".join(words), file=outfp)
            # Blocks will be separated by blanks equal to paragraph_sep
            blanks = "\n" * paragraph_sep
            print(blanks, file=outfp)

def schedule_threads(api_key, inputf, outputf):
    q = queue.Queue()
    # Push all requests in the queue
    for t in zip(inputf, outputf):
        q.put_nowait(t)
    # Let's spin 5 threads
    workers = []
    for _ in range(5):
        w = WorkerThread(api_key, q)
        workers.append(w)
        w.start()
    # Wait for all processes to be completed
    q.join()
    # Stop worker threads
    for _ in range(len(workers)):
        q.put_nowait(None)
    for worker in workers:
        worker.join()

class WorkerThread(threading.Thread):

    def __init__(self, api_key, q):
        super().__init__()
        self.api_key = api_key
        self.q = q

    def run(self):
        while True:
            tpl = self.q.get()
            if tpl == None:
                break
            with open(tpl[0], "rb") as infp, open(tpl[1], "w") as outfp:
                full_annotate_text(self.api_key, infp, outfp)
            # Signal that the task is done
            self.q.task_done()
