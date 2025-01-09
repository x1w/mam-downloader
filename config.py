
# Session
MAM_ID = "" # MyAnonaMouse session, create one here: https://www.myanonamouse.net/preferences/index.php?view=security

# Webhook
DISCORD_WEBHOOK = "" # Discord webhook link for notifications (leave blank to disable)
STATS_NOTIFICATION_INTERVAL = 60 * 60 # Time in seconds the script should wait until sending another statistics update (False to disable)

# Automations
AUTO_EXTRACT_DIR = "" # Automatically extract the downloaded torrents to specified directory (leave blank to disable)
AUTO_DEL_BATCH = True # Automatically delete batch archive files once automatically extracted
AUTO_SPEND_POINTS = False # Automatically spend remaining bonus points on upload

# Torrent search criteria
# More information: https://www.myanonamouse.net/api/endpoint.php/1/tor/js/loadSearchJSONbasic.php
SKIP = ['sSat', 'unsat'] # sSat, unsat, inactHnr, inactUnsat, upInact, inactSat, seedUnsat, seedHnr, leeching, upAct
SEARCH = { 
    "tor": {
        "searchType": "fl-VIP", # fl-VIP, fl, nVIP, VIP, nMeta, inactive, active, all
        "minSize": 0, # 0 to disable
        "maxSize": 0, # 0 to disable
        "unit": 1048576 # 1 = 1 Byte, 1024 = 1 KiB, 1048576 = 1 MiB, 1073741824 = 1 GiB
    }
}

