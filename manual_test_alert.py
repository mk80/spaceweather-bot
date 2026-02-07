import discord
import asyncio

# Read token
try:
    with open('token.txt', 'r') as f:
        TOKEN = f.read().strip()
except FileNotFoundError:
    print("Error: token.txt not found.")
    exit(1)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

GENERAL_CHANNEL_NAME = 'general'

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    print(f"Connected to {len(client.guilds)} guilds.")
    
    channel = None
    for guild in client.guilds:
        for ch in guild.text_channels:
            if ch.name == GENERAL_CHANNEL_NAME:
                channel = ch
                break
        if channel:
            break
            
    if channel:
        print(f"Sending test message to #{channel.name} in guild '{channel.guild.name}'...")
        
        # Simulate a Severe Weather Alert
        await channel.send(
            "⚠️ **TEST: SEVERE SPACE WEATHER ALERT** ⚠️\n"
            "This is a test of the SpaceWeather Bot alert system.\n"
            "Planetary K-index has reached **8.0** (TEST).\n"
            "Systems may be affected. Auroras likely visible at lower latitudes."
        )
        print("Test message sent!")
    else:
        print(f"Could not find channel '{GENERAL_CHANNEL_NAME}' to send test message.")
    
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
