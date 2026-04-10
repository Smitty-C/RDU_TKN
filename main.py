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

# Update scene .json file with current filepaths
with open(OBS_SCENE_JSON_PATH, 'r+') as scene_json_file:
    scene_json = json.load(scene_json_file)
