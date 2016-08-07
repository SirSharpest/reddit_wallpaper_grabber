"""This is the main entry point for the reddit wallpaper
grabber and setter, currently only for linux!"""

import praw
import requests
import re
import sys
import os

reddit = praw.Reddit(user_agent='wallpaper_grabber')
submissions = reddit.get_subreddit('wallpapers').get_hot(limit=25)
filter_name = "^(.*[\\\/])"  # This removes everything but after the last /
image_names = []  # Container for names' of images

if not os.path.exists("wallpapers"):
    os.makedirs("wallpapers")

# Loops through all submissions and decides if they're valid image formats
# Proceeds to download them if so!
for img in submissions:
    if "JPG" in img.url.upper() or "PNG" in img.url.upper():
        try:
            filename = "wallpapers/" + re.sub(filter_name, '', img.url)
            file = requests.get(img.url)

            with open(filename, 'wb') as image:
                image.write(file.content)

            image_names.append(filename)
        except requests.exceptions as e:
            sys.stderr.write("HTTPs Problem with: " + img.url + ' ')

# If there is no images downloaded then exit!
if(len(image_names) < 1):
    sys.ext()
