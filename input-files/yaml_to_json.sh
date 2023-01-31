#!/bin/bash 



YAML_FILE_PATH=$(pwd)/Helm_Charts_MZ13.0.0fix.yaml

# The following command uses built-in python libraries to convert YAML file into JSON to be used as a request payload.
python -c 'import json, yaml, os; print(json.dumps(yaml.safe_load(open(os.getenv("YAML_FILE_PATH"))),indent=2)) ' > yaml.json