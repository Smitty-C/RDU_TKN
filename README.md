### README ###

This repository stores assets used for RDU Tekken Streams for both Open Broadcaster Software (OBS) and Tournament Stream Helper (TSH). Additionally this repository also contains scripts used for automatically setting up a new installation of OBS and TSH.

This functions by running a python script which does the following:
- Checks to see if OBS is installed, if not then downloads it.
- Checks to see if OBS' settings directory exists. If not then quickly launches and closes OBS to force create it.
- OBS stores scene settings in .json files. Next the script updates filepaths in that .json file relative to your machine.
- Then prints out some post installation steps that must be done manually. Unfortunately selecting an OBS scene collection must be done via their GUI and cannot be automated.

### Prerequisites ###

- [Python](https://www.python.org/downloads/windows/) - Using Python 3.14.4 at the time of writing. Make sure you add Python to your windows PATH.
- [Git](https://git-scm.com/install/windows) - Most windows machines have git by default now, however recommended to download git bash so you have a unix like shell.

### Setup ###

NOTE: This setup guide is written from the perspective of someone with zero git/software experience. If you know what you're doing feel free to skip over stuff.

1. Clone this repository
    - Right click in the directory you want to clone this repository in and click "Git Bash Here"
    - From your Git Bash terminal run: `git clone https://github.com/Smitty-C/RDU_TKN.git`
2. Install submodules
    - `cd RDU_TKN`
    - `git submodule update --init --recursive`
3. Setup python virtual environment
    - `python -m venv .venv`
    - `source .venv/Scripts/activate`
    - `pip install -r requirements.txt`
4. Run setup.py
    - `python setup.py`
5. Post installation steps
    - Launch OBS (setup.py automatically launches OBS for you)
    - Import profile by going to Profile > Import > C:/Path/To/RDU_TKN/RDU_TKN_obs_files/obs_profile > Select Folder. Then select RDU_TKN in the dropdown menu under Profile
    - Import scene collection by going to Scene Collection > Import > Click the three dots under Collection Path > C:/Path/To/RDU_TKN/RDU_TKN_obs_files/rdu_tkn_scene_collection.json > Open > Import. Then select rdu_tkn_scene_collection in the dropdown menu under Scene Collection
    - Microphones/Webcams then have to be manually assigned after plugging them into the PC running OBS. This can be done by selecting mic 1/mic 2 under Sources, then choosing the desired microphone in the Devices dropdown menu. Same idea for webcams, but you click Properties to access the dropdown menu