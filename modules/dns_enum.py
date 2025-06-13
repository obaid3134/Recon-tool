# modules/dns_enum.py
import dns.resolver
from utils import print_log

def resolve_dns(domain):
    dns_data = {}

    records = ["A", "AAAA", "MX", "NS", "TXT"]

    for record_type in records:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            dns_data[record_type] = [rdata.to_text() for rdata in answers]
            print_log(f"Found {record_type} records: {dns_data[record_type]}")
        except dns.resolver.NoAnswer:
            print_log(f"No {record_type} record found for {domain}", "WARNING")
        except dns.resolver.NXDOMAIN:
            print_log(f"Domain {domain} does not exist", "ERROR")
            break
        except Exception as e:
            print_log(f"Error querying {record_type} for {domain}: {e}", "ERROR")

    return dns_data
