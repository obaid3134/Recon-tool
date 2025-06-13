# report_generator.py

import os
from datetime import datetime
import socket

class ReportWriter:
    def __init__(self, target_domain):
        self.target_domain = target_domain
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.resolved_ip = self.resolve_ip()
        self.filename = f"report_{self.target_domain}_{self.timestamp}.txt"
        self.file = open(self.filename, "w", encoding="utf-8")
        self.write_intro()

    def resolve_ip(self):
        try:
            return socket.gethostbyname(self.target_domain)
        except socket.error:
            return "Unable to resolve IP"

    def write_intro(self):
        self.file.write(f"Reconnaissance Report for: {self.target_domain}\n")
        self.file.write(f"Timestamp: {self.timestamp}\n")
        self.file.write(f"Resolved IP: {self.resolved_ip}\n")
        self.file.write("=" * 60 + "\n\n")

    def write_section_header(self, title):
        border = "═" * 60
        padded_title = f" {title.upper()} ".center(60, "═")
        self.file.write(padded_title + "\n\n")

    def write_line(self, line):
        self.file.write(line + "\n")

    def write(self, section, content):
        self.write_section_header(section)
        if isinstance(content, (dict, list)):
            self.write_line(str(content))
        else:
            self.write_line(content)
        self.write_line("=" * 60 + "\n")

    def close(self):
        self.file.write("\nEnd of report.\n")
        self.file.write("=" * 60 + "\n")
        self.file.close()

