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
        print("Test severe alert sent!")
        
        await asyncio.sleep(1)
        
        # Simulate a Forecast Alert
        await channel.send(
            "🔮 **TEST: SPACE WEATHER FORECAST** 🔮\n"
            "This is a test of the SpaceWeather Bot alert system.\n"
            "A strong geomagnetic storm is predicted!\n"
            "Predicted K-Index: **7.33** (TEST)\n"
            "Time of Peak: 2026-02-10 00:00:00 UTC\n"
            "Prepare for potential aurora activity in the coming days."
        )
        print("Test forecast alert sent!")
        
        await asyncio.sleep(1)

        # Simulate a Radio Blackout Alert
        await channel.send(
            "☢️ **TEST: RADIO BLACKOUT ALERT** ☢️\n"
            "Solar X-ray Flux has reached **R3 (Strong)** levels.\n"
            "Flux: **1.5e-04** (TEST)\n"
            "Time: 2026-02-07 12:00:00 UTC\n"
            "HF Radio communications on the sunlit side of Earth may be degraded or lost."
        )
        print("Test blackout alert sent!")
    else:
        print(f"Could not find channel '{GENERAL_CHANNEL_NAME}' to send test message.")
    
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
