MAM_ID = "" # Create session, https://www.myanonamouse.net/preferences/index.php?view=security
AUTO_EXTRACT_DIR = "" # Automatically extract the downloaded torrents to specified directory (leave blank to disable)
CHECK_SIZE = False # Check size against values below
MIN_SIZE = 25 * 1024 # Size in KiB, 1 MiB = 1024
MAX_SIZE = 300 * 1024 # Size in KiB, 1 MiB = 1024
SKIP = ['sSat', 'unsat'] # sSat, unsat, inactHnr, inactUnsat, upInact, inactSat, seedUnsat, seedHnr, leeching, upAct
SEARCH = { # https://www.myanonamouse.net/api/endpoint.php/1/tor/js/loadSearchJSONbasic.php
    "tor": {
        "searchType": "fl-VIP" # fl, nVIP, VIP, nMeta, inactive, active, all
    }
}

