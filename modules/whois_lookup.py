# modules/whois_lookup.py
import whois
from utils import print_log

def whois_lookup(domain):
    print_log(f"Performing WHOIS lookup for {domain}")
    try:
        data = whois.whois(domain)
        return str(data)
    except Exception as e:
        return f"[!] WHOIS Lookup failed: {str(e)}"
