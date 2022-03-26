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
                  "wallpaperdump", "minimalwallpaper", "animewallpaper" ]

    # Fetch wallpapers
    logger.info(f'Scraping images from {subreddits}')
    desktopWallpapers = []
    for submission in reddit.subreddit('+'.join(subreddits)).hot(limit=200):
        if not submission.over_18 and submission.link_flair_text not in ['Request', 'Mobile', 'Animated', 'Collection'] and hasattr(submission, 'preview'):
            images = submission.preview.get("images", [])
            for image in images:
                url = image['source']['url']
                width = image['source']['width']
                height = image['source']['height']
                if width > height:
                    desktopWallpapers.append(Wallpaper(
                        submission.id, submission.subreddit_name_prefixed, submission.title, url, width, height))
    
    # Create directory if not exists
    outDir = os.getenv('OUT_DIR')
    Path(outDir).mkdir(parents=True, exist_ok=True)

    # Fill folder
    num_files = int(os.getenv('NUM_FILES'))
    list_of_files = os.listdir(outDir)
    while len(list_of_files) < num_files:
        # Pick random image
        logger.info(f'Picking one of {len(desktopWallpapers)} files')
        wallpaper = random.choice(desktopWallpapers)
        logger.info(f'{wallpaper.url} => {wallpaper.filename()}')

        # Download Image
        urllib.request.urlretrieve(
            wallpaper.url, f'{outDir}\\{wallpaper.filename()}')
        
        # Recheck folder
        list_of_files = os.listdir(outDir)

    # Remove old files if we have too many
    list_of_files = os.listdir(outDir)
    while len(list_of_files) > num_files:
        full_path = [f'{outDir}\\{name}' for name in list_of_files]
        oldest_file = min(full_path, key=os.path.getctime)
        logger.info(f'Cleaning {oldest_file}')
        os.remove(oldest_file)
        list_of_files = os.listdir(outDir)

except:
    logger.error("Unexpected error:", sys.exc_info()[0])
    raise
