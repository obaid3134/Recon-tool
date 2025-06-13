# modules/whatweb_detect.py

import subprocess
from utils import print_log

def run_whatweb(domain):
    try:
        print_log(f"Running WhatWeb on {domain}")
        result = subprocess.run(
            ["whatweb", domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            print(result.stdout)
            return result.stdout.strip()  # ✅ Return the output for report
        else:
            error_msg = f"WhatWeb error: {result.stderr}"
            print_log(error_msg, "ERROR")
            return error_msg  # ✅ Return error message for report

    except FileNotFoundError:
        error_msg = "WhatWeb is not installed. Please install it using: sudo apt install whatweb"
        print_log(error_msg, "ERROR")
        return error_msg  # ✅ Return message so report doesn't fail
