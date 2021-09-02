# copy-wallpapers

Scheduled task to copy cool wallpapers locally so windows can use them.

## Wallpapers scraped from:

- [r/wallpaper](https://www.reddit.com/r/wallpaper/)
- [r/wallpapers](https://www.reddit.com/r/wallpapers/)
- [r/wallpaperdump](https://www.reddit.com/r/wallpaperdump/)
- [r/minimalwallpaper](https://www.reddit.com/r/minimalwallpaper/)

## Installation

1. Clone this repo into `C:\Scripts\`

```ps
$ git clone https://github.com/Reptarsrage/copy-wallpapers.git C:\Scripts\copy-wallpapers
```

2. Install the dependencies by running:

```ps
$ cd C:\Scripts\copy-wallpapers
$ python -m venv venv
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
```

3. Create `C:\Scripts\copy-wallpapers\.env` with the following contents:

```
CLIENT_ID=<REDDIT CLIENT ID>
CLIENT_SECRET=<REDDIT CLIENT SECRET>
USER_AGENT=copy-wallpapers/1.0.0 by reptarsrage
OUT_DIR=D:\Pictures\Wallpapers
```

> NOTE: To generate Reddit API Creds [see here](https://github.com/reddit-archive/reddit/wiki/OAuth2#getting-started).

> NOTE: Feel free to modify `OUT_DIR` to whatever you wish, this will be the location of the downloaded wallpapers.

4. Open Task Scheduler and import `C:\Scripts\copy-wallpapers\Copy Wallpapers.xml`.

5. On the "General" tab, click "Change User or Group..." button, type in your username.
   Ensure it's correct by clicking "Check Names" before clicking "OK".

6. On the "Triggers" tab, highlight the trigger and click "Edit" then click "Change User..." and type in your username.
   Ensure it's correct by clicking "Check Names" before clicking "OK".

7. Right click your desktop and click "Personalize", then set the background
   to a Slideshow and use the `OUT_DIR` configured in you `.env` file.
