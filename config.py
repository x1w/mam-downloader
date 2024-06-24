MAM_ID = "" # Create session, https://www.myanonamouse.net/preferences/index.php?view=security
AUTO_EXTRACT_DIR = "" # Automatically extract the downloaded torrents to specified directory (leave blank to disable)
SKIP = ['sSat', 'unsat'] # sSat, unsat, inactHnr, inactUnsat, upInact, inactSat, seedUnsat, seedHnr, leeching, upAct
SEARCH = { # https://www.myanonamouse.net/api/endpoint.php/1/tor/js/loadSearchJSONbasic.php
    "tor": {
        "searchType": "fl-VIP", # fl, nVIP, VIP, nMeta, inactive, active, all
        "minSize": 25, # 0 to disable
        "maxSize": 200, # 0 to disable
        "unit": 1048576 # 1 = 1 Byte, 1024 = 1 KiB, 1048576 = 1 MiB, 1073741824 = 1 GiB
    }
}

