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


with open(json_path / "columns_ccog.json") as f:
    columns_names_ccog = json.load(f)
# Output directory
output_dir = Path("data/renamed_files/")
output_dir.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# FIND ALL ccog FILES
# -------------------------------------------------
ccog_files = list(folder_path.glob("*ccog*.csv"))
print(f"🔍 Found {len(ccog_files)} ccog files")

for file in ccog_files:
    print(f"⚙ Processing → {file.name}")

    # ---------------------------------------------
    # LOAD + NAME COLUMNS
    # ---------------------------------------------
    df = pd.read_csv(file, header=None)
    df = df.rename(columns={int(k): v for k, v in columns_names_ccog.items()})
    '''
    {
        "0": "Timestamp_Epoch",
        "1": "Timestamp_Seconds",
        "2": "Cable_X",
        "3": "Cable_Y",
        "4": "Cable_Z",
        "5": "Cable_offset_distance",
        "6": "Offsets_1",
        "7": "Offsets_2",
        "8": "Offsets_3",
        "9": "Offsets_4",
        "10": "Offsets_5",
        "11": "Cable_Lock"
    }
    '''

    # ---------------------------------------------
    # WRITE OUTPUT
    # ---------------------------------------------
    out_path = output_dir / file.name.replace(".csv", "_renamed.csv")
    df.to_csv(out_path, index=False)

    print(f"   ✔ Saved → {out_path}")



