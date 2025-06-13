# modules/banner_grabber.py

import socket
from utils import print_log

def grab_banner(ip, port, timeout=1):
    try:
        with socket.socket() as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            banner = s.recv(1024).decode(errors="ignore").strip()
            return banner if banner else "No banner received"
    except Exception as e:
        return f"Error: {str(e)}"

def grab_banners(ip, ports):
    print_log(f"Grabbing banners for {ip}")
    banners = {}
    for port in ports:
        banner = grab_banner(ip, port)
        banners[port] = banner
    return banners
