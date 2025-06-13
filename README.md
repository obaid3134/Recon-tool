
# Custom Reconnaissance Tool

A lightweight, modular reconnaissance tool developed in Python for automating initial information gathering during penetration testing engagements.

---

## Features

  - **Passive Recon**
  - WHOIS Lookup
  - DNS Enumeration (A, MX, TXT, NS)
  - Subdomain Enumeration using `crt.sh` and `AlienVault OTX`

  - **Active Recon**
  - Socket-Based Port Scanning
  - Banner Grabbing
  - Nmap Scanning (Top ports or Full scan)
  - Technology Detection using WhatWeb

  - **Reporting**
  - Timestamped `.txt` report with all results
  - Includes IP resolution, summaries, and module output

  - **Extras**
  - Modular design (call modules individually)
  - CLI logging verbosity (`--verbose`, `--quiet`)
  - Environment-safe API key handling using `.env`

---

## Installation

```bash
git clone https://github.com/yourusername/recon-tool.git
cd recon-tool
pip install -r requirements.txt
```

Make sure the following are installed:

- Python 3.x
- `nmap`, `whatweb`, and `whois` (install via apt or equivalent)

```bash
sudo apt install whatweb nmap whois
```

---

## Usage

Basic usage:

```bash
python3 main.py example.com --all
```

Individual module usage:

```bash
python3 main.py example.com --dns --whois
```

Verbose output:

```bash
python3 main.py example.com --all --verbose
```

Quiet mode (errors only):

```bash
python3 main.py example.com --all --quiet
```

---

## .env Setup

Create a `.env` file in the root directory with:

```env
OTX_API_KEY=your_alienvault_api_key_here
```


## 📝 Sample Report

Output reports are saved as:

```
reports/example.com_YYYY-MM-DD_HHMM.txt
```

---

## License

MIT License

---

## Author

Developed by [Obaid3134] as part of a cybersecurity internship project.


