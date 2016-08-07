"""This is the main entry point for the reddit wallpaper
grabber and setter, currently only for linux!"""

import praw
import urllib.request
import re
import sys


reddit = praw.Reddit(user_agent='wallpaper_grabber')
submissions = reddit.get_subreddit('wallpapers').get_hot(limit=25)
filter_name = "^(.*[\\\/])"  # This removes everything but after the last /
image_names = []  # Container for names' of images

# Loops through all submissions and decides if they're valid image formats
# Proceeds to download them if so!
for img in submissions:
    if "JPG" in img.url.upper() or "PNG" in img.url.upper():
        try:
            filename = re.sub(filter_name, '', img.url)
            urllib.request.urlretrieve(img.url, filename)
            image_names.append(filename)
        except urllib.error.HTTPError as e:
            sys.stderr.write("HTTP Problem with: " + img.url + ' ')

# If there is no images downloaded then exit!
if(len(image_names) < 1):
    sys.ext()
