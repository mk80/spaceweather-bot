# Project: SpaceWeather Bot

## Overview
This project is a Discord bot that monitors space weather conditions using data from the NOAA Space Weather Prediction Center (spaceweather.gov). It provides alerts for:
1.  **Aurora Visibility in Northern US**: Notifies when auroras are likely to be visible further south than usual (implying better visibility in the northern US).
2.  **Severe Space Storms**: Alerts when space weather conditions reach "very severe" levels (e.g., G4/Kp >= 8).

## Data Sources
-   **Aurora Forecast**: `https://services.swpc.noaa.gov/json/ovation_aurora_latest.json` (or `products/noaa-ovation-aurora-latest.json`)
-   **Planetary K-index**: `https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json`

## Configuration
-   **Discord Token**: Stores in `token.txt` (or environment variable).
-   **Channel**: "general" channel of the server.

## Logic
-   **Aurora Detection**: Analyze the OVATION forecast model. Look for high probabilities of visible aurora in latitudes corresponding to the northern United States (approx 40°N - 50°N).
-   **Severe Storm Detection**: Monitor the K-index. Trigger alert if Kp >= 8.

## Constraints
-   Use `discord.py` for Discord interaction.
-   Use `requests` or `aiohttp` for API requests.
-   Keep the bot running continuously.
