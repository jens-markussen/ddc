import socket
import threading
from queue import Queue

target = "diskenc.cfire"   # change this
start_port = 1
end_port = 10240
threads = 100

q = Queue()

def scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((target, port))
        print(f"Port {port} OPEN")
        s.close()
    except:
        pass

def worker():
    while not q.empty():
        port = q.get()
        scan(port)
        q.task_done()

for port in range(start_port, end_port + 1):
    q.put(port)

thread_list = []
for _ in range(threads):
    t = threading.Thread(target=worker)
    t.start()
    thread_list.append(t)

q.join()

print("Scan complete")