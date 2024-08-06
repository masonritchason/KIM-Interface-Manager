
from json import dumps

# KIM Interface Mapping Configuration Class
class MappingConfiguration:
    # default constructor
    def __init__(self, id_num, mappings):
        self.id_num = id_num
        self.mappings = mappings

    def toJSON(id_num, mappings):
        """Writes the class to a JSON object that can be stored in configuration files."""
        # create a Dictionary to hold the Object
        to_dict = {"id":int(id_num), 
                   "mappings":mappings}
        # dump to a JSON formatted object
        to_json = dumps(to_dict, indent = 4)
        # return the json object
        return to_json