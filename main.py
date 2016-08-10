"""This is the main entry point for the reddit wallpaper
grabber and setter, currently only for linux!"""

# Imports
import praw
import requests
import re
import sys
import os
# import random this is unused until we fix logic
import datetime
import subprocess


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def download_x_pictures(num_to_get):
    reddit = praw.Reddit(user_agent='wallpaper_grabber')
    submissions = reddit.get_subreddit('wallpapers').get_hot(limit=num_to_get)
    filter_name = "^(.*[\\\/])"  # This removes everything but after the last /
    image_names = []  # Container for names' of images

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

    return image_names


def check_file_exits():
    if os.path.exists("wallpapers"):
        date = modification_date("wallpapers")
        age = (datetime.datetime.now() - date).seconds
        if age / 3600 >= 24:
            import shutil
            shutil.rmtree("wallpapers")
        else:
            os.makedirs("wallpapers")


def set_wallpaper(wallpaper_to_use):
    command = "gsettings set org.gnome.desktop.background picture-uri\
    file:" + os.getcwd() + "/" + wallpaper_to_use
    subprocess.Popen(command.split())
