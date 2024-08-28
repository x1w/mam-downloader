import os
from sys import platform
from dotenv import load_dotenv
load_dotenv()

MAM_ID = os.getenv("MAM_ID") # Create session, https://www.myanonamouse.net/preferences/index.php?view=security
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK") # Will send information about script run if set
AUTO_EXTRACT_DIR = "/pool/share/torrents" if platform == "linux" else "" # Automatically extract the downloaded torrents to specified directory (leave blank to disable)
AUTO_DEL_BATCH = True # Automatically delete batches, after auto extracted
AUTO_MILLIONARES_VAULT = True # Automatically purchase millionare's vault if available
AUTO_SPEND_POINTS = True # Automatically spend remaining bonus points on upload
AUTO_STATS_INTERVAL =  3600 # Automatically show download, upload, ratio, etc on interval
SKIP = ['sSat', 'unsat'] # sSat, unsat, inactHnr, inactUnsat, upInact, inactSat, seedUnsat, seedHnr, leeching, upAct
SEARCH = { # https://www.myanonamouse.net/api/endpoint.php/1/tor/js/loadSearchJSONbasic.php
    "tor": {
        "searchType": "fl-VIP", # fl, nVIP, VIP, nMeta, inactive, active, all
        "minSize": 25, # 0 to disable
        "maxSize": 200, # 0 to disable
        "unit": 1048576 # 1 = 1 Byte, 1024 = 1 KiB, 1048576 = 1 MiB, 1073741824 = 1 GiB
    }
}

