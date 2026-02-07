# SpaceWeather Bot

A Discord bot that monitors space weather conditions from the NOAA Space Weather Prediction Center (SWPC) and alerts your server about:
1.  **Aurora Visibility**: High probability of auroras being visible in the Northern US (and lower latitudes).
2.  **Severe Space Storms**: Planetary K-index reaching severe levels (Kp >= 8).

## Features
-   **Real-time Monitoring**: Checks NOAA data every 15 minutes.
-   **Smart Alerts**: Sends messages to the `#general` channel only when significant events occur.
-   **Cooldowns**: Prevents spam by enforcing a 6-hour cooldown between similar alerts.

## Installation

1.  **Prerequisites**:
    -   Python 3.8+
    -   A Discord Server

2.  **Clone/Download** the repository.

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### 1. Discord Token
Create a file named `token.txt` in the root directory and paste your Discord Bot Token inside it.
*(Do not share this token with anyone)*.

### 2. Invite the Bot
You must invite the bot to your server with the correct permissions.
1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2.  Select your app -> **OAuth2** -> **URL Generator**.
3.  Select Scope: `bot`.
4.  Select Permissions: `Send Messages`, `View Channels`, `Read Message History`.
5.  Use the generated URL to invite the bot to your server.

**Note**: The bot looks for a channel named `general`. Ensure this channel exists and the bot has permission to view and post in it.

## Usage

### Run the Bot
```bash
python3 bot.py
```
The bot will log in and start checking for space weather updates immediately.

### Verify / Test
To confirm the bot can post to your server without waiting for a real solar storm, run the manual test script:
```bash
python3 manual_test_alert.py
```
This will send a simulated "Severe Validator Alert" to your `#general` channel.

## Data Sources
-   [NOAA Planetary K-index](https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json)
-   [NOAA OVATION Aurora Forecast](https://services.swpc.noaa.gov/json/ovation_aurora_latest.json)
