import pandas as pd
import json
import math

xls = pd.ExcelFile(r'd:\SAF\supplementary material.xlsx')
raw_data = {}

for s in xls.sheet_names:
    df = pd.read_excel(xls, s, header=None)
    
    source_data = {}
    current_target = None
    
    for idx, row in df.iloc[3:].iterrows():
        target = row[0]
        if pd.notna(target) and str(target).strip() != "":
            current_target = str(target).strip()
            source_data[current_target] = {
                "energy": [],
                "phits": [],
                "rel_error": [],
                "icrp": [],
                "delta": []
            }
            
        if current_target:
            try:
                energy = float(row[1]) if pd.notna(row[1]) else None
                phits = float(row[2]) if pd.notna(row[2]) else None
                rel_error = float(row[3]) if pd.notna(row[3]) else None
                icrp = float(row[4]) if pd.notna(row[4]) else None
                delta = float(row[5]) if pd.notna(row[5]) else None
                
                if energy is not None:
                    source_data[current_target]["energy"].append(energy)
                    source_data[current_target]["phits"].append(phits)
                    source_data[current_target]["rel_error"].append(rel_error)
                    source_data[current_target]["icrp"].append(icrp)
                    source_data[current_target]["delta"].append(delta)
            except Exception as e:
                pass
                
    def clean_nans(d):
        for k, v in d.items():
            for i in range(len(v["energy"])):
                if v["phits"][i] is not None and math.isnan(v["phits"][i]): v["phits"][i] = None
                if v["rel_error"][i] is not None and math.isnan(v["rel_error"][i]): v["rel_error"][i] = None
                if v["icrp"][i] is not None and math.isnan(v["icrp"][i]): v["icrp"][i] = None
                if v["delta"][i] is not None and math.isnan(v["delta"][i]): v["delta"][i] = None
    clean_nans(source_data)
    
    raw_data[s] = source_data

# Wrap in Phantom -> Particle hierarchy
hierarchical_data = {
    "Adult Male": {
        "Photons": raw_data
    }
}

with open(r'd:\SAF\data.js', 'w', encoding='utf-8') as f:
    f.write("const INITIAL_DATA = ")
    json.dump(hierarchical_data, f, ensure_ascii=False, indent=2)
    f.write(";")
