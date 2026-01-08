from telethon import TelegramClient
from collections import defaultdict
import json
import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
group = os.environ["GROUP"]

client = TelegramClient("session", api_id, api_hash)

# Load last processed message id
try:
    with open("last_id.txt") as f:
        last_id = int(f.read().strip())
except:
    last_id = 0

# Load existing stats
try:
    with open("stats.json") as f:
        stats = json.load(f)
except:
    stats = {}

new_last_id = last_id

async def main():
    global new_last_id

    async for msg in client.iter_messages(group, min_id=last_id):
        if not msg.sender:
            continue

        user = msg.sender.username or f"id_{msg.sender_id}"
        stats[user] = stats.get(user, 0) + 1
        new_last_id = max(new_last_id, msg.id)

    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    with open("last_id.txt", "w") as f:
        f.write(str(new_last_id))

with client:
    client.loop.run_until_complete(main())
