from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pathlib import Path
import threading
import time
import os
from threading import Thread
from random import randint

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    html = Path("templates/index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)



@app.get("/get-tools", response_class=HTMLResponse)
def get_tools(method: str):

    if method == "thread":
        return """
        <label>ابزار همزمانی:</label>
        <select id="tool" name="tool">
            <option value="lock">1- Lock</option>
            <option value="rlock">2- RLock</option>
            <option value="semaphore">3- Semaphore</option>
            <option value="condition">4- Condition</option>
            <option value="event">5- Event</option>
            <option value="barrier">6- Barrier</option>
            <option value="queue">7- Queue</option>
        </select>
        """

    if method == "process":
        return """
        <label>ابزار همزمانی:</label>
        <select id="tool" name="tool">
            <option value="spawn">1- Spawning</option>
            <option value="name">2- Naming</option>
            <option value="background">3- Background</option>
            <option value="kill">4- Killing</option>
            <option value="subclass">5- Subclass</option>
            <option value="queue">6- Queue</option>
            <option value="sync">7- Synchronizing</option>
            <option value="pool">8- Pool</option>
        </select>
        """

    return ""



@app.post("/run", response_class=HTMLResponse)
def run(
    method: str = Form(...),
    tool: str = Form(...),
    scenario: str = Form(...),
):

  
    if method == "thread" and tool == "lock" and scenario == "1":

        threadLock = threading.Lock()
        logs = []

        class MyThreadClass(Thread):
            def __init__(self, name, duration):
                Thread.__init__(self)
                self.name = name
                self.duration = duration

            def run(self):
                threadLock.acquire()
                logs.append(f" ---> {self.name} running (PID={os.getpid()})")
                time.sleep(self.duration)
                logs.append(f" ---> {self.name} over")
                threadLock.release()

        threads = [
            MyThreadClass(f"Thread#{i}", randint(1, 3))
            for i in range(1, 10)
        ]

        start = time.time()

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        total = time.time() - start
        logs.append("End")
        logs.append(f"--- {total:.2f} seconds ---")

        html_output = "<br>".join(logs)

        return f"""
        <div class="result">
            <h4>خروجی:</h4>
            <pre>{html_output}</pre>
        </div>
        """

    
    return f"""
    <div class="result">
        <pre>برای {method} با همزمانی {tool} سناریوی {scenario} تعریف نشده است.</pre>
    </div>
    """