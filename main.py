import shutil
import wget
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
OBS_DOWNLOAD_URL = 'https://github.com/obsproject/obs-studio/releases/download/32.1.1/OBS-Studio-32.1.1-Windows-arm64.zip'
OBS_DIR = str(BASE_DIR / 'OBS-Studio')  # DO NOT CHANGE THIS NAME

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

# Update OBS with RDU_TKN files
