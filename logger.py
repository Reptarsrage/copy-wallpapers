import logging
import logging.handlers as handlers

logger = logging.getLogger('theme-switcher')
logger.setLevel(logging.INFO)

## Here we define our formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.RotatingFileHandler('./logs/app.log', maxBytes=100000, backupCount=10)
logHandler.setLevel(logging.INFO)

## Here we set our logHandler's formatter
logHandler.setFormatter(formatter)

logger.addHandler(logHandler)
logger.addHandler(logging.StreamHandler())

# Add logger to PRAW
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def info(str):
    logger.info(str)

def warn(str):
    logger.warn(str)

def error(str):
    logger.error(str)