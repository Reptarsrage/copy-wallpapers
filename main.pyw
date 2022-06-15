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

class Cache:
    def __init__(self):
        self.filename = "wallpapers.cache"
        self.limit = 1000
        self.keys = []
        self.init = False

    def __exists(self):
        return os.path.exists(self.filename)

    def __read(self):
        if self.init:
            return self.keys

        if self.__exists():
            with open(self.filename, 'r') as file:
                self.keys = file.readlines()
                self.keys = [key.rstrip() for key in self.keys]
        
        self.init = True
        return self.keys

    def __write(self):
        if not self.init:
            self.__read()

        with open(self.filename, 'w') as file:
            file.writelines([key + '\n' for key in self.keys])
    
    def has(self, key):
        keys = self.__read()
        return key in keys
    
    def add(self, key):
        if not self.has(key):
            self.keys.append(key) # append key
            self.keys = self.keys[-self.limit:] # take only most recent keys
            self.__write()
    
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
                if width > height and width >= 1920 and height >= 1080:
                    desktopWallpapers.append(Wallpaper(
                        submission.id, submission.subreddit_name_prefixed, submission.title, url, width, height))
    
    # Create directory if not exists
    outDir = os.getenv('OUT_DIR')
    Path(outDir).mkdir(parents=True, exist_ok=True)

    # Init cache
    cache = Cache()

    # Fill folder
    num_files = int(os.getenv('NUM_FILES'))
    new_files = int(os.getenv('NEW_FILES'))
    list_of_files = os.listdir(outDir)
    while len(desktopWallpapers) > 0 and len(list_of_files) < num_files + new_files:
        # Pick random image
        logger.info(f'Picking one of {len(desktopWallpapers)} files')
        wallpaper = desktopWallpapers.pop(random.randrange(len(desktopWallpapers)))
        logger.info(f'{wallpaper.url} => {wallpaper.filename()}')

        # Check if previously downloaded
        if cache.has(wallpaper.id):
            continue

        # Download Image
        urllib.request.urlretrieve(
            wallpaper.url, f'{outDir}\\{wallpaper.filename()}')
        
        # Add to cache
        cache.add(wallpaper.id)

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
