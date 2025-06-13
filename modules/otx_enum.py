# modules/otx_enum.py
import requests
from utils import print_log, get_otx_api_key

def get_subdomains_otx(domain):
    api_key = get_otx_api_key()
    headers = {
        "X-OTX-API-KEY": api_key
    }
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"

    print_log(f"Querying AlienVault OTX for subdomains of {domain}")

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            print_log(f"OTX request failed with status code {response.status_code}", "ERROR")
            return []

        data = response.json()
        subdomains = set()

        for entry in data.get("passive_dns", []):
            hostname = entry.get("hostname", "")
            if hostname.endswith(domain):
                subdomains.add(hostname)

        return sorted(subdomains)

    except Exception as e:
        print_log(f"Error fetching subdomains from OTX: {e}", "ERROR")
        return []
