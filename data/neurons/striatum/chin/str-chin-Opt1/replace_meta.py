import json
import copy

# Define the new morphologies
morphologies = [f"17JUL302018_170614_no6_MD_cell_2_x63-cor_centered-ax{i}.swc" for i in range(1, 20)]

# Load the original meta.json
with open("meta.json", "r") as f:
    meta = json.load(f)

new_meta = {}

for param_key, param_data in meta.items():
    new_meta[param_key] = {}
    
    # Use the first morphology entry as the template to copy structure/inputs from
    template_morph_key = next(iter(param_data))
    template = param_data[template_morph_key]
    
    for i, morph_file in enumerate(morphologies, start=1):
        morph_key = f"morph{i}"
        new_entry = copy.deepcopy(template)
        new_entry["morphology"] = morph_file
        new_meta[param_key][morph_key] = new_entry

# Save the result
with open("meta_new.json", "w") as f:
    json.dump(new_meta, f, indent=4)

print(f"Done! Created {len(new_meta)} parameter sets, each with {len(morphologies)} morphologies.")
