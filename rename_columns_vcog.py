import pandas as pd
import numpy as np
from omegaconf import OmegaConf
from pathlib import Path
import json

# -------------------------------------------------
# LOAD CONFIG
# -------------------------------------------------
config_path = "config.yaml"
config = OmegaConf.load(config_path)
folder_path = Path(config.folder_path)
json_path = Path(config.json_path)
#-------------------------------------------------
# LOAD COLUMN NAMES FROM JSON
#-------------------------------------------------
with open(json_path / "columns_vcog.json") as f:
    columns_names_vcog = json.load(f)

with open(json_path / "columns_ccog.json") as f:
    columns_names_ccog = json.load(f)
# Output directory
output_dir = Path("data/renamed_files/")
output_dir.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# FIND ALL VCOG FILES
# -------------------------------------------------
vcog_files = list(folder_path.glob("*VCoG*.csv"))
print(f"🔍 Found {len(vcog_files)} VCOG files")

for file in vcog_files:
    print(f"⚙ Processing → {file.name}")

    # ---------------------------------------------
    # LOAD + NAME COLUMNS
    # ---------------------------------------------
    df = pd.read_csv(file, header=None)
    df = df.rename(columns={int(k): v for k, v in columns_names_vcog.items()})
    '''
    {
    "0": "Timestamp_Epoch",
    "1": "Timestamp_Seconds",
    "2": "Cart_X",
    "3": "Cart_Y",
    "4": "Cart_Z",
    "5": "Yaw_angle",
    "6": "Cable_X",
    "7": "Cable_Y",
    "8": "Unused",
    "9": "Cable_Lock"
    }
    '''

    # ---------------------------------------------
    # WRITE OUTPUT
    # ---------------------------------------------
    out_path = output_dir / file.name.replace(".csv", "_renamed.csv")
    df.to_csv(out_path, index=False)

    print(f"   ✔ Saved → {out_path}")



