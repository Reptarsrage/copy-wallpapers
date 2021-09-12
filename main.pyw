import praw
from pathlib import Path
import urllib.request
import random
import os
import sys
import logger
from dotenv import load_dotenv


class Wallpaper:
    def __init__(self, id, subreddit, title, url, width, height):
        self.id = id
        self.subreddit = subreddit
        self.title = title
        self.url = url
        self.width = width
        self.height = height
        self.ext = url.split('?')[0].split('.')[-1]

    def filename(self):
        filename = f'{self.title} [{self.subreddit}] [{self.id}]'
        filename = "".join([c for c in filename if c.isalpha()
                           or c.isdigit() or c == ' ']).rstrip()
        return f'{filename}.{self.ext}'


try:
    load_dotenv()  # take environment variables from .env.

    # Create reddit client
    logger.info('Authenticating with reddit')
    reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        user_agent=os.getenv('USER_AGENT'),
    )

    # Define subreddits to check
    subreddits = ["wallpaper", "wallpapers",
                  "wallpaperdump", "minimalwallpaper", ]

    # Fetch wallpapers
    logger.info(f'Scraping images from {subreddits}')
    desktopWallpapers = []
    for submission in reddit.subreddit('+'.join(subreddits)).hot(limit=100):
        if not submission.over_18 and submission.link_flair_text != 'Request' and hasattr(submission, 'preview'):
            images = submission.preview.get("images", [])
            for image in images:
                url = image['source']['url']
                width = image['source']['width']
                height = image['source']['height']
                if width > height:
                    desktopWallpapers.append(Wallpaper(
                        submission.id, submission.subreddit_name_prefixed, submission.title, url, width, height))

    # Pick random image
    wallpaper = random.choice(desktopWallpapers)
    logger.info(f'{wallpaper.url} => {wallpaper.filename()}')

    # Create directory if not exists
    outDir = os.getenv('OUT_DIR')
    Path(outDir).mkdir(parents=True, exist_ok=True)

    # Download Image
    urllib.request.urlretrieve(
        wallpaper.url, f'{outDir}\\{wallpaper.filename()}')

    # Remove old files if we have too many
    list_of_files = os.listdir(outDir)
    full_path = [f'{outDir}\\{name}' for name in list_of_files]
    if len(list_of_files) > 10:
        oldest_file = min(full_path, key=os.path.getctime)
        logger.info(f'Cleaning {oldest_file}')
        os.remove(oldest_file)

except:
    logger.error("Unexpected error:", sys.exc_info()[0])
    raise
