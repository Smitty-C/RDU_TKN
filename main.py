import json
import os
import time
import subprocess
import shutil
import wget
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
OBS_DOWNLOAD_URL = 'https://github.com/obsproject/obs-studio/releases/download/32.1.0/OBS-Studio-32.1.0-Windows-x64.zip'
OBS_DIR = str(BASE_DIR / 'OBS-Studio')
OBS_SETTINGS_DIR = Path(os.path.expandvars("%APPDATA%"))/'obs-studio'
OBS_SCENE_JSON_PATH = Path(BASE_DIR) / 'RDU_TKN_obs_files' / 'rdu_tkn_scene_collection.json'

OBS_ASSETS_DIR = Path(BASE_DIR) / 'RDU_TKN_obs_files' / 'assets'
OBS_ASSETS = [
    'rdu_stinger.webm',
    'red_outline_left_gradient.png',
    'red_outline_right_gradient.png',
    't8_bg.png',
    'tk8_website_animated.webm',
    'twitch.png',
    'twitter.png',
    'youtube.png'
]

# This function recursively searches through a json object to find the lowest level key value pair whose value contains 'searchStr' substring
g_assetDict = {}
def recursiveDictSearch(d, searchStr):
    for k,v in d.items():
        if searchStr in str(v):
            if isinstance(v, dict):
                recursiveDictSearch(v, searchStr)
            else:
                if isinstance(v, list):
                    for dictList in v:
                        if isinstance(dictList, dict):
                            recursiveDictSearch(dictList, searchStr)
                        else:
                            g_assetDict[k] = v
                else:
                    g_assetDict[k] = v

print('')

# Check if OBS exists or not
if not Path(OBS_DIR).is_dir():
    # Download OBS if not found
    print("Downloading OBS from " + OBS_DOWNLOAD_URL)
    obs_filename = wget.download(OBS_DOWNLOAD_URL, out=str(BASE_DIR))  # Download OBS
    shutil.unpack_archive(obs_filename, OBS_DIR)                       # Unzip
    Path(obs_filename).unlink()                                        # Delete old .zip file
    print("\nDownloaded OBS to " + OBS_DIR)
else:
    print("Found OBS installation at " + OBS_DIR)

# OBS stores settings files at %APPDATA%/obs-studio. This folder doesn't exist until launching OBS for the first time.
# Therefore, force create the settings files by launching OBS, let it setup it's settings directories, and then close OBS.

# Check if obs settings directory exists
if not OBS_SETTINGS_DIR.is_dir():
    # Launch OBS to create settings directory
    print('OBS settings directory ' + str(OBS_SETTINGS_DIR) + ' doesn\'t exist. Launching OBS to create it...')
    obs_bin_path = Path(OBS_DIR) / 'bin' / '64bit'
    obs_subprocess = subprocess.Popen(obs_bin_path / 'obs64.exe', cwd=obs_bin_path, creationflags=subprocess.DETACHED_PROCESS)

    # Wait for obs settings directory to be created
    while not (Path(os.path.expandvars("%APPDATA%"))/'obs-studio').is_dir():
        time.sleep(0.05)

    # Kill OBS process
    time.sleep(1) # Give obs an extra second to finish setting everything up
    print('Found OBS settings directory at ' + str(OBS_SETTINGS_DIR))
    print("Killing OBS process...")
    obs_subprocess.terminate()
else:
    print('Found OBS settings directory at ' + str(OBS_SETTINGS_DIR))

# Load OBS scene json
with open(OBS_SCENE_JSON_PATH, 'r+') as scene_json_file:
    scene_json = json.load(scene_json_file)

    # Update each asset in json
    for curr_asset in OBS_ASSETS:
        # Find asset in json
        print(curr_asset)
        g_assetDict.clear()
        recursiveDictSearch(scene_json, curr_asset)
        if g_assetDict:
            for k,v in g_assetDict.items():
                print(k,v)
        else:
            print('Warning! Did not find ' + curr_asset + ' in json')




