"""This is the main entry point for the reddit wallpaper
grabber and setter, currently only for linux!"""

# Imports
import praw
import requests
import re
import sys
import os
import random
import datetime


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


reddit = praw.Reddit(user_agent='wallpaper_grabber')
submissions = reddit.get_subreddit('wallpapers').get_hot(limit=25)
filter_name = "^(.*[\\\/])"  # This removes everything but after the last /
image_names = []  # Container for names' of images


if os.path.exists("wallpapers"):
    date = modification_date("wallpapers")
    age = (datetime.datetime.now() - date).seconds
    if age / 3600 >= 24:
        import shutil
        shutil.rmtree("wallpapers")
else:
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
else:
    background = random.choice(image_names)
    command = "gsettings set org.gnome.desktop.background picture-uri\
    file:" + os.getcwd() + "/" + background

    import subprocess
    process = subprocess.Popen(command.split())
    sys.exit()
