#!/usr/bin/env python
__author__ = "Jamie Sherriff"
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Jamie Sherriff"
__contact__ = "https://github.com/jamie-sherriff"
__status__ = "Prototype"
__date__ = "27-02-2017"
'''
Simple script to download over the last 100 images found at usap antarctica web cams
Built using pyinstaller --onefile download_loop.py --hidden-import queue
'''
import shutil
import time
import requests
import random
import os
import sys
from time import strftime, localtime
dir_path = os.path.dirname(os.path.realpath(__file__))
start_time = strftime("%Y-%m-%d %H-%M-%S", localtime())

# download_folder = os.path.join(os.getcwd(), start_time)
download_folder = os.path.join(os.getcwd(), 'pictures')

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

BASE_URL = None
OPTION = None
if len(sys.argv) > 1:
    if str(sys.argv[1]).lower() == 'pier' :
        print ('downloading pier')
        OPTION = 'pier'
        BASE_URL = 'https://www.usap.gov/videoClipsAndMaps/SouthPoleWebcam/MobileWebCam'
    elif str(sys.argv[1]).lower() == 'arrival':
        print('downloading arrival')
        OPTION = 'arrival'
        BASE_URL = 'https://www.usap.gov/videoClipsAndMaps/SouthPoleWebcam/McM'
    elif str(sys.argv[1]).lower() == 'hill':
        print('downloading hill')
        OPTION = 'hill'
        BASE_URL = 'https://www.usap.gov/videoclipsandmaps/SouthPoleWebcam/boresight'
    elif str(sys.argv[1]).lower() == 'radio':
        print('downloading radio')
        OPTION = 'radio'
        BASE_URL = 'https://www.usap.gov/videoClipsAndMaps/SouthPoleWebcam/darksector'
    elif str(sys.argv[1]).lower() == 'pole':
        print('downloading pole')
        OPTION = 'pole'
        BASE_URL = 'https://www.usap.gov/videoClipsAndMaps/SouthPoleWebcam/spole'
    else:
        print('default to pier as could not find correct argument parse: ' + str(sys.argv))
        OPTION = 'pier'
        BASE_URL = 'https://www.usap.gov/videoClipsAndMaps/SouthPoleWebcam/MobileWebCam'
else:
    print('defaulting to pier as no extra args found: ' + str(sys.argv))
    OPTION = 'pier'
    BASE_URL = 'https://www.usap.gov/videoClipsAndMaps/SouthPoleWebcam/MobileWebCam'


def format_number(number):
    num_length = len(str(number))
    new_number = str(number)
    if num_length == 1:
        new_number = '0000' + new_number
    elif num_length == 2:
        new_number = '000' + new_number
    elif num_length == 3:
        new_number = '00' + new_number
    elif num_length == 4:
        new_number = '0' + new_number
    return new_number


for number in range(1, 101, 1):
    #url = 'https://www.usap.gov/videoClipsAndMaps/SouthPoleWebcam/MobileWebCam' + format_number(number) + '.jpg'
    url = BASE_URL + format_number(number) + '.jpg'
    # url = 'https://www.usap.gov/videoClipsAndMaps/SouthPoleWebcam/McM'+ format_number(number) + '.jpg'
    sleep_time = random.randint(10, 20)
    print('sleeping for: ' + str(sleep_time))
    time.sleep(sleep_time)
    print('downloading ' + url)
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    timestamp = str(int(time.time()))
    # with open(str(number)+'img.png', 'wb') as out_file:
    file_name = OPTION + '-' + timestamp + '-' + format_number(number) + '.jpg'
    print('Saving file as: ' + file_name)
    with open(os.path.join(download_folder, file_name), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
