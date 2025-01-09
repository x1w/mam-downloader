import requests
import config
import json
import os
import math
import time
import zipfile
from discord import SyncWebhook, Embed

session = requests.Session()
headers = {}
freshLoad = True
base_url = "https://www.myanonamouse.net"
data_dir = "storage"
storage_path = "storage/data.json"
data = {}

# Create data dir
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

# Load previously saved data
if os.path.exists(storage_path):
    with open(storage_path, 'rb') as f:
        data = json.loads(f.read())
        freshLoad = False

# Save data to prevent constant unneeded requests
def saveDataFile() -> bool:
    data['lastSaved'] = time.time()
    with open(storage_path, 'w') as f:
        json.dump(data, f)

def getUserDetails() -> dict:
    headers["cookie"] = f"mam_id={config.MAM_ID}"
    response = session.get(
            f"{base_url}/jsonLoad.php?snatch_summary", 
            headers=headers
        )

    # Invalid MAM_ID?
    if response.status_code != 200:
        return

    return response.json()

def getSnatchListIds(user: dict, type: str = 'sSat') -> list:
    results = []
    iteration = 0
    keepGoing = True
    previous = None
    
    # Increment through snatched until no results
    while keepGoing:
        response = session.get(
            f"{base_url}/json/loadUserDetailsTorrents.php?uid={user['uid']}&type={type}&iteration={str(iteration)}",
            headers=headers
        )
        unix = time.time()

        cur = response.json()
        # No results remaining, or unsat (returns all at once) - not sure if this is the case for users with 200 limit?
        if not cur['rows']:
            keepGoing = False
            continue
        
        # Filter ids from results
        ids = []
        for row in cur['rows']:
            ids.append(row['id'])

        # Ensure its not the same as last result
        if ids == previous:
            keepGoing = False
            continue

        previous = ids
        results.extend(ids)
        iteration += 1

    return results

def getTorrents(snatched: list = [], amount: int = 100):
    keepGoing = True
    iteration = 0 
    results = []
    
    while keepGoing:
        config.SEARCH['perpage'] = 100
        config.SEARCH['tor']['startNumber'] = iteration

        # Use search endpoint
        response = session.post(
            f"{base_url}/tor/js/loadSearchJSONbasic.php", 
            headers=headers,
            json=config.SEARCH
        )

        cur = response.json()

        # Stop loop if error occurs
        if 'error' in cur:
            keepGoing = False
            continue

        page_amt = len(cur['data'])
        print(f"Checking torrents {iteration}-{iteration+page_amt}")

        # Sort through data
        for torrent in cur['data']:
            id = str(torrent['id'])

            # Check if snatched already
            if id in snatched or id in results:
                continue

            # Add if desired count hasn't been reached
            if len(results) < amount:
                results.append(id)

        iteration += page_amt

        # Stop search if desired count reached, <future> or no more results
        if len(results) >= amount:
            keepGoing = False

    return results

def downloadBatch(ids: list):
    # Download in batches, the site only allows 100 at a time
    for i in range(0, len(ids), 100):
        batch = ids[i:i + 100]
        tids = '&'.join([f'tids[]={id}' for id in batch])

        response = session.get(
            f"{base_url}/DownloadZips.php?type=batch&{tids}", 
            headers={**headers, "Content-Type": "application/x-zip"},
            timeout=30
        )

        # Write result to zip file
        path = os.path.join(data_dir, f"batch_{time.time()}.zip")
        with open(path, 'wb') as f:
            f.write(response.content) 

        # Extract to specified dir
        if config.AUTO_EXTRACT_DIR:
            print(f"Extracting {path} to {config.AUTO_EXTRACT_DIR}")
            with zipfile.ZipFile(path, 'r') as f:
                f.extractall(config.AUTO_EXTRACT_DIR)
            if config.AUTO_DEL_BATCH:
                os.remove(path)

        time.sleep(5)

def sendWebhook(content: str = None, fields: dict = None):
    url = config.DISCORD_WEBHOOK
    # Skip if no url set in configuration
    if not url:
        return
    
    # Webhook
    webhook = SyncWebhook.from_url(config.DISCORD_WEBHOOK)
    embed = Embed(
        color=14858496,
        description=content,
    )
    embed.set_author(name="MyAnonaMouse Helper")
    embed.set_thumbnail(url="https://i.imgur.com/unDUs13.png")

    # Dynamically add fields
    if fields:
        for name, value in fields.items():
            embed.add_field(name=name, value=value, inline=True)

    webhook.send(embed=embed)

def main():
    # Check if we can get user details correctly
    user = getUserDetails()
    if not user:
        print("Invalid MyAnonaMouse session ID provided, set this value in config.py")
        return
        
    # Check if anything should be done 
    unsat = user['unsat']['count'] 
    limit = user['unsat']['limit']

    # Create data file with base data if doesn't exist
    if not data:
        data["lastDonate"] = 0
        data["statsLastSend"] = 0
        saveDataFile()

    # Send a webhook containing stats
    if config.STATS_NOTIFICATION_INTERVAL:
        elapsed = time.time() - data["statsLastSend"]
        if elapsed > config.STATS_NOTIFICATION_INTERVAL:
            # Calculate their ratio
            uploaded = user["uploaded_bytes"]
            downloaded =  user["downloaded_bytes"]
            ratio =  math.inf if downloaded == 0 else uploaded / downloaded

            sendWebhook(fields={
                "Uploaded": user['uploaded'],
                "Downloaded": user['downloaded'],
                "Ratio": f"{ratio:.2f}"
            })

            data["statsLastSend"] = time.time()
            saveDataFile()

    # Spend free bonus points
    if config.AUTO_SPEND_POINTS:
        r = session.get(
            f"{base_url}/json/bonusBuy.php/?spendtype=upload&amount=Max Affordable ", 
            headers=headers
        ).json()

        # Extract results and send to webhook
        if r["success"]:
            sendWebhook(content="{} GB upload credit purchased.".format(r["amount"]))

    # Skip if no more torrents should be added
    if unsat >= limit:
        print(f"You've reached your unsaturated torrent limit, not continuing.")
        return
    
    # Create a list which we can check ids against to avoid duplicates
    skip_ids = []
    for value in config.SKIP:
        count = user[value]['count']
        # Do the check if not saved or saved count differs from last check
        if value not in data or count != len(data[value]):
            print(f"Storing {count} items from {value} list")
            data[value] = getSnatchListIds(user, value)
            saveDataFile()
        skip_ids.extend(data[value])
    
    skip_ids = list(set(skip_ids))

    # Browse for torrents
    amount = limit - unsat
    print(f"Grabbing {amount} torrents with specified criteria")
    ids = getTorrents(skip_ids, amount)
    
    # Download grabbed torrents
    if ids:
        print(f"Downloading batch of {len(ids)} torrents")
        downloadBatch(ids)

if __name__ == "__main__":
    main()
