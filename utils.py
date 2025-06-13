import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Default fallback API key (use your real key here)
DEFAULT_OTX_API_KEY = "your_actual_otx_key_here"

# Logging level control
VERBOSE = True
QUIET = False

def set_verbosity(verbose=False, quiet=False):
    global VERBOSE, QUIET
    VERBOSE = verbose
    QUIET = quiet

def get_otx_api_key():
    return os.getenv("OTX_API_KEY", DEFAULT_OTX_API_KEY)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_log(message, level="INFO"):
    if QUIET and level != "ERROR":
        return
    if not VERBOSE and level == "DEBUG":
        return
    print(f"[{get_timestamp()}] [{level}] {message}")
