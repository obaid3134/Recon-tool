import subprocess
from utils import print_log

def run_nmap_scan(target, fast_mode=True):
    print_log(f"Running Nmap scan on {target} {'[FAST MODE]' if fast_mode else '[FULL SCAN]'}")
    flags = "-T4 -F" if fast_mode else "-T4 -p-"

    try:
        result = subprocess.run(
            ["nmap"] + flags.split() + [target],
            capture_output=True,
            text=True,
            shell=False  # More secure
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"[ERROR] Nmap scan failed: {result.stderr}"

    except Exception as e:
        return f"[ERROR] Exception while running Nmap: {e}"
