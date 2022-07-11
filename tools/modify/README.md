Meta.json is the core of each model within Snudda. To explain how features are added, we start with an example:
    
    Here, is an example dictionary from a dSPN, prior to the addition of features
    
    
    { "p1863c9a5": {
        "m22be6817": {
            "morphology": "WT-0728MSN01-cor-rep-ax-res3-var7.swc"
        }
    For this model, we start with a simple addition of the 'neuromodulation'-feature:

    We utilise the add_feature.add_feature_to_meta, we accepts the dictionary of the model 
    to execute the addition on (directory) and a dictionary containing the additional 
    feature (additional_feature_json).
    The structure of 'additional_feature_json' is the same as meta.json in terms of parameter hash_keys
    and morphology hash_keys. For example, for the above example, the 'additional_feature_json' would
    look like:

    {
    "p1863c9a5": {
        "m22be6817": {
            "neuromodulation": [
                "nm4b9bc75a",
                "nma92963ce"
            ]
        }}

    Thus, the function of add_feature_to_meta is purley to merge two dictionaries.

    The resulting dictionary would be,

    {
    "p1863c9a5": {
        "m22be6817": {
            "morphology": "WT-0728MSN01-cor-rep-ax-res3-var7.swc",
            "neuromodulation": [
                "nm4b9bc75a",
                "nma92963ce"
            ]
        }}