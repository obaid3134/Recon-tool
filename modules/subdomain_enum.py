# modules/subdomain_enum.py
import requests
from utils import print_log
import json

def get_subdomains_crtsh(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    print_log(f"Querying crt.sh for subdomains of {domain}")

    try:
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            print_log(f"crt.sh request failed with status code {response.status_code}", "ERROR")
            return []

        # Parse JSON
        raw_data = json.loads(response.text)
        subdomains = set()

        for entry in raw_data:
            name_value = entry.get("name_value", "")
            for sub in name_value.split("\n"):
                if sub.endswith(domain):
                    subdomains.add(sub.strip())

        return sorted(subdomains)

    except Exception as e:
        print_log(f"Error fetching subdomains from crt.sh: {e}", "ERROR")
        return []
