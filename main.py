import os
import shutil
from pathlib import Path

# TODO: Turns out all the layout stuff is from a repo here https://github.com/TournamentStreamHelper/TournamentStreamHelper-layouts.
# TODO: Need to submodule that repo, and the TSH repo to make all this easier, have everything contained in the RDU_TKN repo.
# TODO: Should also look into submoduling the OBS repo as well.
# TODO: Don't forget about the TSH default layouts repo

# TODO: You can clone the TSH repo directly and it has the .exe in it.
# TODO: OBS has to be built from source. Not sure if we want to mess with that or just wget the latest release. Might also just wget the latest TSH release as well.
# TODO: obs is build via visual studio solution file, not going to mess with that, just use wget

# TODO: wget OBS and TSH, submodule TSH layouts and fork the repo with our changes

# Filepaths for OBS and TSH. These are the destination directory where the script will copy files into.
# TODO: Make these command line parameters
TSH_FILEPATH = Path(os.path.join(r'D:\Stuff\rdu_tkn\TESTING_TSH_OBS\TournamentStreamHelper-5.967'))
OBS_FILEPATH = Path(os.path.join(r'D:\Stuff\rdu_tkn\TESTING_TSH_OBS\OBS-Studio-32.0.4-Windows-x64'))
print("OBS Destination Directory = " + str(OBS_FILEPATH))
print("TSH Destination Directory = " + str(TSH_FILEPATH))

# Get file's relative filepaths based on main.py filepath
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # main.py filepath
TSH_FILES_DIR = Path(os.path.join(SCRIPT_DIR, "tsh_files"))
OBS_FILES_DIR = Path(os.path.join(SCRIPT_DIR, "obs_files"))
print("Script directory = " + str(SCRIPT_DIR))

# Keeps track of errors
IS_ERROR = False

# Copy TSH files
print("Copying TSH files...")
if TSH_FILEPATH.is_dir():
    try:
        # Copy layout files
        print("Copying layout files...")
        for file in TSH_FILES_DIR.glob('*'):
            if file.is_file():
                destination_path = Path(os.path.join(TSH_FILEPATH, "layout", file.name))
                print("Copying " + str(file) + " to " + str(destination_path))
                shutil.copy2(file, destination_path)

        # Copy scoreboard files
        print("Copying scoreboard files...")
        TSH_SCOREBOARD_FILES_DIR = Path(os.path.join(TSH_FILES_DIR, "scoreboard"))
        for file in TSH_SCOREBOARD_FILES_DIR.glob('*'):
            if file.is_file():
                destination_path = Path(os.path.join(TSH_FILEPATH, "layout", "scoreboard", file.name))
                print("Copying " + str(file) + " to " + str(destination_path))
                shutil.copy2(file, destination_path)
    except Exception as e:
        IS_ERROR = True
        print(f"An error occured: {e}")
else:
    IS_ERROR = True
    print("Error directory does not exist : " + str(TSH_FILEPATH))
print("Finished copying TSH files")

# Copy OBS Files
print("Copying OBS files...")
if OBS_FILEPATH.is_dir():
    print("TODO: Copy OBS Files")
else:
    IS_ERROR = True
    print("Error directory does not exist : " + str(OBS_FILEPATH))
print("Finished copying OBS files")

# Cleanup
if not IS_ERROR:
    print("Finished copying all files.")
    print("REMINDER: This script just copies assets over. In order for OBS to be setup correctly you must manually import OBS profiles and scenes.")
    print("In OBS profiles can be imported by going to: Profile > Import...")
    print("In OBS scenes can be imported by going to: Scene Collection > Import...")
