import json


def rename_math_exp(parameters_json, output_dir):

    """
    Rename the exp expression with math.exp for Snudda
    :param parameters_json:
    :param output_dir:
    :return:
    """
    with open(parameters_json, 'r+') as f:
        content = f.read()
        f.seek(0)
        content = content.replace('math.exp',
                                  'exp')  # This way it can be run multiple time without creating math.math.exp
        content = content.replace('exp',
                                  'math.exp')  # In long term, change "from math import *" in Alex code to "import math"
        f.write(content)

    with open(os.path.join(output_dir, "parameters.json"), "w") as f:
        json.dump(content, f)
