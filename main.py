"""This is the main entry point for the reddit wallpaper
grabber and setter, currently only for linux!"""

# Imports
import praw
import requests
import re
import sys
import os
import random  # this is unused until we fix logic
import datetime
import subprocess


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def select_from_x_pictures(num_to_get):
    reddit = praw.Reddit(user_agent='wallpaper_grabber')
    subs = reddit.get_subreddit('wallpapers').get_hot(limit=num_to_get)
    filter_name = "^(.*[\\\/])"  # This removes everything but after the last /
    image = None

    submissions = []
    for img in subs:
        if ".png" in img.url.lower() or ".jpg" in img.url.lower():
            submissions.append(img.url)

    attempts = 0
    while attempts < num_to_get:
        try:
            check_file_exits()
            image = random.choice(submissions)
            filename = "wallpapers/" + re.sub(filter_name, '', image)
            file = requests.get(image)
            with open(filename, 'wb') as img:
                img.write(file.content)
                image = filename
        except:
            sys.stderr.write("Problem with downloading image")
            attempts += 1
            continue
        return image


def check_file_exits():
    if os.path.exists("wallpapers"):
        import shutil
        shutil.rmtree("wallpapers")
    else:
        os.makedirs("wallpapers")


def set_wallpaper(wallpaper_to_use):
    command = "gsettings set org.gnome.desktop.background picture-uri\
    file:" + os.getcwd() + "/" + wallpaper_to_use
    subprocess.Popen(command.split())

set_wallpaper(select_from_x_pictures(25))
