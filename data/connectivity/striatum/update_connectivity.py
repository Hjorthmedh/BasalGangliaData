import json

with open('striatum-connectivity.json', 'r') as h:
    data = json.load(h)

# open updated notebooks
with open('../../../../Snudda/examples/notebooks/optimise_prune/ChIN/network-config-opt.json', 'r') as h:
    chin = json.load(h)
with open('../../../../Snudda/examples/notebooks/optimise_prune/TH/network-config-opt.json', 'r') as h:
    th = json.load(h)
with open('../../../../Snudda/examples/notebooks/optimise_prune/NGF/network-config-opt.json', 'r') as h:
    ngf = json.load(h)

# merge
for cell in [chin, th, ngf]:
    for key, item in cell['connectivity'].items():
        for k in item.keys():
            item[k]['conductance'] = [1.1e-09, 1.5e-09]
        data[key] = item

# save to file
with open('striatum-connectivity.json', 'w') as h:
    json.dump(data, h, indent=4)

