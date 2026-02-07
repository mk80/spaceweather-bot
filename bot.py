import discord
from discord.ext import tasks, commands
import os
from utils import get_aurora_data, get_k_index_data, check_severe_storm, check_northern_us_aurora
import datetime

# Read token
try:
    with open('token.txt', 'r') as f:
        TOKEN = f.read().strip()
except FileNotFoundError:
    print("Error: token.txt not found.")
    exit(1)

# Discord Intents
intents = discord.Intents.default()
# intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Channel ID to post to (will be found dynamically or set)
# We'll look for a channel named 'general'
GENERAL_CHANNEL_NAME = 'general'

# State to avoid spamming
last_severe_alert_time = None
last_aurora_alert_time = None
ALERT_COOLDOWN = datetime.timedelta(hours=6) # Don't alert for the same thing within 6 hours

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    check_space_weather.start()

@tasks.loop(minutes=15)
async def check_space_weather():
    global last_severe_alert_time, last_aurora_alert_time
    
    print(f"Checking space weather at {datetime.datetime.now()}...")
    
    # Find the general channel
    channel = None
    
    print(f"Connected to {len(bot.guilds)} guilds.")
    
    for guild in bot.guilds:
        # Try to find 'general'
        for ch in guild.text_channels:
            if ch.name == GENERAL_CHANNEL_NAME:
                channel = ch
                break
        
        # If not found, fall back to the first text channel we can send messages in
        if not channel and guild.text_channels:
             channel = guild.text_channels[0]
             print(f" 'general' not found in {guild.name}, defaulting to: {channel.name}")

        if channel:
            break
    
    if not channel:
        print(f"Could not find channel '{GENERAL_CHANNEL_NAME}' in any guild.")
        return

    # 1. Check Severe Storm
    k_data = get_k_index_data()
    severe_info = check_severe_storm(k_data)
    
    if severe_info:
        now = datetime.datetime.now()
        if last_severe_alert_time is None or (now - last_severe_alert_time) > ALERT_COOLDOWN:
            message = (
                f"⚠️ **SEVERE SPACE WEATHER ALERT** ⚠️\n"
                f"Planetary K-index has reached **{severe_info['kp']}** ({severe_info['level']}).\n"
                f"Time: {severe_info['time']}\n"
                f"Systems may be affected. Auroras likely visible at lower latitudes."
            )
            await channel.send(message)
            last_severe_alert_time = now
            print("Sent Severe Weather Alert.")

    # 2. Check Northern US Aurora
    aurora_data = get_aurora_data()
    aurora_vis = check_northern_us_aurora(aurora_data)
    
    if aurora_vis:
        now = datetime.datetime.now()
        if last_aurora_alert_time is None or (now - last_aurora_alert_time) > ALERT_COOLDOWN:
            message = (
                f"🌌 **AURORA FORECAST ALERT** 🌌\n"
                f"High probability of aurora visibility in Northern US!\n"
                f"Forecast Max Probability: **{aurora_vis['max_prob']}%** in the region.\n"
                f"Keep an eye on the sky tonight!"
            )
            await channel.send(message)
            last_aurora_alert_time = now
            print("Sent Aurora Visibility Alert.")

@check_space_weather.before_loop
async def before_check():
    await bot.wait_until_ready()

if __name__ == '__main__':
    bot.run(TOKEN)
