# main.py

import argparse
from modules import (
    whois_lookup, dns_enum, subdomain_enum, otx_enum,
    port_scan, nmap_scan, banner_grabber, whatweb_detect
)
from utils import print_log, set_verbosity
from report_generator import ReportWriter
from datetime import datetime

# Styled section headers with bold blue color and box layout
def print_section_header(title, report):
    box_width = 44
    padded_title = f" {title.upper()} "
    border_top = f"╔{'═' * box_width}╗"
    border_mid = f"║{padded_title.center(box_width)}║"
    border_bot = f"╚{'═' * box_width}╝"
    header = f"\n\033[1;34m{border_top}\n{border_mid}\n{border_bot}\033[0m\n"

    print(header)
    report.write_section_header(title)

# WHOIS Lookup
def run_whois(domain, report):
    print_section_header("WHOIS Lookup", report)
    whois_result = whois_lookup.whois_lookup(domain)
    print(whois_result)
    report.write("WHOIS Lookup", whois_result)

# DNS Enumeration
def run_dns(domain, report):
    print_section_header("DNS Enumeration", report)
    dns_result = dns_enum.resolve_dns(domain)
    print(dns_result)
    report.write("DNS Enumeration", dns_result)

# Subdomain Enumeration
def run_subdomain_enum(domain, report):
    print_section_header("Subdomain Enumeration", report)
    subdomains_crtsh = subdomain_enum.get_subdomains_crtsh(domain)
    subdomains_otx = otx_enum.get_subdomains_otx(domain)
    master_subdomains = sorted(set(subdomains_crtsh + subdomains_otx))

    output = ""
    if master_subdomains:
        print_log(f"Found {len(master_subdomains)} unique subdomains.")
        for sub in master_subdomains:
            output += f"- {sub}\n"
    else:
        output = "No subdomains found or error occurred."
        print_log(output, "WARNING")

    print(output)
    report.write("Subdomain Enumeration", output)

# Socket-Based Port Scanning
def run_port_scan(domain, report, all_ports=False):
    print_section_header("Port Scanning (Socket-Based)", report)
    open_ports = port_scan.scan_ports(domain, all_ports=all_ports, timeout=0.2, thread_count=100)
    output = ""

    if open_ports:
        output = f"Open ports: {', '.join(str(p) for p in open_ports)}"
        print_log(output)
    else:
        output = "No open ports detected."
        print_log(output, "WARNING")

    report.write("Port Scanning", output)

# Banner Grabbing
def run_banner_grabbing(domain, report):
    print_section_header("Banner Grabbing (Socket-Based)", report)
    common_ports = [21, 22, 23, 25, 80, 110, 135, 139, 143, 443, 445, 3306, 8080]
    banners = banner_grabber.grab_banners(domain, common_ports)

    output = ""
    for port, banner in banners.items():
        line = f"[Port {port}] => {banner}"
        print(line)
        output += line + "\n"

    report.write("Banner Grabbing", output)

# Nmap Scan
def run_nmap_scan(domain, report, fast_mode=True):
    print_section_header("Nmap Scan", report)
    nmap_result = nmap_scan.run_nmap_scan(domain, fast_mode=fast_mode)
    print(nmap_result)
    report.write("Nmap Scan", nmap_result)

# Technology Detection via WhatWeb
def run_whatweb(domain, report):
    print_section_header("Technology Detection (WhatWeb)", report)
    whatweb_result = whatweb_detect.run_whatweb(domain)
    report.write("Technology Detection", whatweb_result)

# ======================
# Main Execution Starts Here
# ======================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom Reconnaissance Tool")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--whois", action="store_true", help="Perform WHOIS lookup")
    parser.add_argument("--dns", action="store_true", help="Perform DNS enumeration")
    parser.add_argument("--subdomains", action="store_true", help="Enumerate subdomains")
    parser.add_argument("--ports", action="store_true", help="Perform socket-based port scan")
    parser.add_argument("--banners", action="store_true", help="Perform banner grabbing")
    parser.add_argument("--nmap", action="store_true", help="Run Nmap (top ports only)")
    parser.add_argument("--nmap-full", action="store_true", help="Run full Nmap scan")
    parser.add_argument("--whatweb", action="store_true", help="Detect technologies using WhatWeb")
    parser.add_argument("--all", action="store_true", help="Run all modules")
    parser.add_argument("--all-ports", action="store_true", help="Scan all 65535 ports")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--quiet", action="store_true", help="Suppress all logs except errors")

    args = parser.parse_args()
    set_verbosity(verbose=args.verbose, quiet=args.quiet)

    domain = args.domain
    report = ReportWriter(domain)

    try:
        if args.all or args.whois:
            run_whois(domain, report)
        if args.all or args.dns:
            run_dns(domain, report)
        if args.all or args.subdomains:
            run_subdomain_enum(domain, report)
        if args.all or args.ports:
            run_port_scan(domain, report, all_ports=args.all_ports)
        if args.all or args.banners:
            run_banner_grabbing(domain, report)
        if args.all or args.nmap or args.nmap_full:
            run_nmap_scan(domain, report, fast_mode=not args.nmap_full)
        if args.all or args.whatweb:
            run_whatweb(domain, report)
    finally:
        report.close()
