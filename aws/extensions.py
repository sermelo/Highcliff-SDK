from ast import Str
from tokenize import String
from typing import Dict
import re

# this file contains some helper functions for processing data

# map dictionary values to variables in file 
def fileVarMapper(mappings: Dict, file: Str ) -> Str:

    mappings = dict((re.escape(k), v) for k, v in mappings.items())
    pattern = re.compile('|'.join(mappings.keys()))

    with open(file, 'r') as f:
            data = pattern.sub(lambda m: mappings[re.escape(m.group(0))], f.read())

    return data

    


