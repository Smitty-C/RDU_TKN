import json
import os
import time
import subprocess
import sys
import shutil
import wget
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
OBS_DOWNLOAD_URL = 'https://github.com/obsproject/obs-studio/releases/download/32.1.0/OBS-Studio-32.1.0-Windows-x64.zip'
OBS_SETTINGS_DIR = Path(os.path.expandvars("%APPDATA%"))/'obs-studio'
OBS_DIR = BASE_DIR / 'OBS-Studio'
OBS_SCENE_JSON_PATH = BASE_DIR / 'RDU_TKN_obs_files' / 'rdu_tkn_scene_collection.json'
OBS_ASSETS_DIR = BASE_DIR / 'RDU_TKN_obs_files' / 'assets'
OBS_SCRIPTS_DIR = BASE_DIR / 'RDU_TKN_obs_files' / 'scripts'
TSH_DIR = BASE_DIR / 'TournamentStreamHelper'


# Make sure submodules exist before running the rest of the script
print('') # Extra newline for pretty printing
if not TSH_DIR.is_dir():
    print('Error! Submodules not found! Run the following command to update submodules before running this script:')
    print('git submodule update --init --recursive')
    sys.exit()

# Check if OBS exists or not
if not OBS_DIR.is_dir():
    # Download OBS if not found
    print("Downloading OBS from " + OBS_DOWNLOAD_URL)
    obs_filename = wget.download(OBS_DOWNLOAD_URL, out=str(BASE_DIR))  # Download OBS
    shutil.unpack_archive(obs_filename, str(OBS_DIR))                  # Unzip
    Path(obs_filename).unlink()                                        # Delete old .zip file
    print("\nDownloaded OBS to " + str(OBS_DIR))
else:
    print("Found OBS installation at " + str(OBS_DIR))

# OBS stores settings files at %APPDATA%/obs-studio. This folder doesn't exist until launching OBS for the first time.
# Therefore, force create the settings files by launching OBS, let it setup it's settings directories, and then close OBS.
if not OBS_SETTINGS_DIR.is_dir():
    # Launch OBS to create settings directory
    print('OBS settings directory ' + str(OBS_SETTINGS_DIR) + ' doesn\'t exist. Launching OBS to create it...')
    obs_bin_path = OBS_DIR / 'bin' / '64bit'
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
    print('Loading JSON settings from ' + str(OBS_SCENE_JSON_PATH))
    scene_json = json.load(scene_json_file)

    # Update json filepaths TODO: Search for keys by value to avoid hardcoded array indicies
    print('Updating JSON settings...')
    scene_json['transitions'][0]['settings']['path'] = str(OBS_ASSETS_DIR / 'rdu_stinger.webm').replace('\\', '/')
    scene_json['modules']['scripts-tool'][0]['path'] = str(OBS_SCRIPTS_DIR / 'advanced-timer.lua').replace('\\', '/')
    scene_json['sources'][1]['settings']['local_file'] = str(OBS_ASSETS_DIR / 'tk8_website_animated.webm').replace('\\', '/')
    scene_json['sources'][3]['settings']['local_file'] = str(TSH_DIR / 'layout' / 'bracket' / 'index.html').replace('\\', '/')
    scene_json['sources'][7]['settings']['local_file'] = str(TSH_DIR / 'layout' / 'commentators' / 'tag_twitter.html').replace('\\', '/')
    scene_json['sources'][11]['settings']['file'] = str(OBS_ASSETS_DIR / 'rdu_tkn_logo.png').replace('\\', '/')
    scene_json['sources'][16]['settings']['file'] = str(OBS_ASSETS_DIR / 't8_bg.png').replace('\\', '/')
    scene_json['sources'][17]['settings']['file'] = str(OBS_ASSETS_DIR / 'red_outline_left_gradient.png').replace('\\', '/')
    scene_json['sources'][18]['settings']['file'] = str(OBS_ASSETS_DIR / 'red_outline_right_gradient.png').replace('\\', '/')
    scene_json['sources'][20]['settings']['local_file'] = str(TSH_DIR / 'layout' / 'scoreboard' / 'rdu_t8.html').replace('\\', '/')
    scene_json['sources'][28]['settings']['local_file'] = str(TSH_DIR / 'layout' / 'top_8' / 'index.html').replace('\\', '/')
    scene_json['sources'][31]['settings']['file'] = str(OBS_ASSETS_DIR / 'twitch.png').replace('\\', '/')
    scene_json['sources'][33]['settings']['file'] = str(OBS_ASSETS_DIR / 'twitter.png').replace('\\', '/')
    scene_json['sources'][38]['settings']['file'] = str(OBS_ASSETS_DIR / 'youtube.png').replace('\\', '/')

    # Save updated json settings
    scene_json_file.seek(0)
    scene_json_file.truncate()  # Clear file before writing
    json.dump(scene_json, scene_json_file, ensure_ascii=False, indent=4)
    print('JSON settings updated. Settings saved at ' + str(OBS_SCENE_JSON_PATH))

# Launch OBS
print("Launching OBS to setup scene collection and profile...")
obs_bin_path = OBS_DIR / 'bin' / '64bit'
obs_subprocess = subprocess.Popen(obs_bin_path / 'obs64.exe', cwd=obs_bin_path, creationflags=subprocess.DETACHED_PROCESS)

# Instruct user to select correct scenes. OBS does not provide a way to import scenes from command line.
print("/////////////////////////////////////IMPORTANT!/////////////////////////////////////")
print("TO FINISH SETTING UP OBS YOU MUST MANUALLY SELECT YOUR SCENE COLLECTION AND PROFILE")
print("\nIMPORTING PROFILE : From within OBS go to Profile > Import > C:/Path/To/RDU_TKN/RDU_TKN_obs_files/obs_profile > Select Folder")
print("\nIMPORTING SCENE COLLECTION : From within OBS go to Scene Collection > Import > Click the three dots under Collection Path > " \
"C:/Path/To/RDU_TKN/RDU_TKN_obs_files/rdu_tkn_scene_collection.json > Open > Import > Scene Collection > rdu_tkn_scene_collection")
print("\n/////////////////////////////////////////////////////////////////////////////////")




