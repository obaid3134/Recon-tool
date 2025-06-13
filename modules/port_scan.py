# modules/port_scan.py

import socket
import threading
from queue import Queue
from utils import print_log

print_lock = threading.Lock()

def scan_port(target, port, open_ports, timeout):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        result = s.connect_ex((target, port))
        if result == 0:
            with print_lock:
                print_log(f"Port {port} is open.")
                open_ports.append(port)
        s.close()
    except:
        pass

def scan_ports(target, all_ports=False, timeout=0.2, thread_count=100):
    ports_to_scan = range(1, 65536) if all_ports else [
        21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 8080
    ]

    open_ports = []
    queue = Queue()

    def thread_worker():
        while not queue.empty():
            port = queue.get()
            scan_port(target, port, open_ports, timeout)
            queue.task_done()

    print_log(f"Starting port scan on {target} ({'all ports' if all_ports else 'common ports'})")

    for port in ports_to_scan:
        queue.put(port)

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=thread_worker)
        t.start()
        threads.append(t)

    queue.join()
    return sorted(open_ports)
