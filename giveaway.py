from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaGiveaway
from telethon.tl.functions.channels import JoinChannelRequest
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Replace these with your Telegram API credentials from the .env file
api_id = int(os.getenv('API_ID'))  # Ensure api_id is an integer
api_hash = os.getenv('API_HASH')
giveaway_channels = os.getenv('GIVEAWAY_CHANNELS').split(',')  # Split channels into a list
your_country = os.getenv('YOUR_COUNTRY')

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=giveaway_channels))
async def giveaway_handler(event):
    media = event.message.media
    if isinstance(media, MessageMediaGiveaway):
        stars_count = getattr(media, 'stars', None)
        premium_months = getattr(media, 'months', None)
        channels_to_join = getattr(media, 'channels', [])
        countries_iso2 = getattr(media, 'countries_iso2', [])

        # Display giveaway type
        if stars_count:
            print(f"Stars giveaway: {stars_count} stars detected.")
        elif premium_months:
            print(f"Premium giveaway: {premium_months} months detected.")
        else:
            print("Giveaway detected but type is unknown.")

        # Check country eligibility
        if countries_iso2 and your_country not in countries_iso2:
            print(f"You are not eligible for this giveaway (Your country: {your_country}). Skipping.")
            return  # Stop processing this giveaway

        # Join channels/groups if eligible
        if channels_to_join:
            print("Attempting to join required channels/groups...")
            for channel_id in channels_to_join:
                try:
                    result = await client(JoinChannelRequest(channel_id))
                    if result.updates:
                        print(f"Successfully joined: ID: {channel_id}")
                    else:
                        print(f"Already a member of: ID: {channel_id}")
                except Exception as e:
                    print(f"Failed to join ID: {channel_id}: {e}")
        else:
            print("No channels/groups specified for participation.")
    else:
        print("No giveaway detected.")

# Start the client and listen for messages
with client:
    print("Listening for messages from multiple giveaway channels...")
    client.run_until_disconnected()
