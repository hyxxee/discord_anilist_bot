# Final Discord Anime & Manga Bot

This is a Discord bot that fetches and displays information about anime and manga using the Anilist API. The bot provides commands to retrieve detailed information about anime and manga, including release dates, status, episodes/chapters, and more.

## Features

- Fetch and display detailed information about anime and manga.
- Use the Anilist API to gather data.
- Display anime and manga details in embedded messages.
- Include features like status, format, total episodes/chapters, genres, average score, and ranking.
- Dynamically update the embed color based on the anime or manga cover color.
- Commands:
  - `?ping`: Check the bot's latency.
  - `?anime [title]`: Get information about the specified anime.
  - `?manga [title]`: Get information about the specified manga.

## Requirements

- Python 3.8 or higher
- `discord.py` library
- `requests` library
- `pillow` library
- A Discord bot token

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/hyxxee/discord_anilist_bot.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your `config.py` file

4. Run the bot:

    ```bash
    python main.py or python3 main.py
    ```
