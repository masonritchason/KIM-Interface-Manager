
"""Mapping Configurations instruct the Interface to send data to specific places on i-Reporter forms."""

from json import dumps

# KIM Interface Mapping Configuration Class
class MappingConfiguration:
    # default constructor
    def __init__(self, id_num, mappings):
        self.id_num = id_num
        self.mappings = mappings

    # default print
    def __str__(self):
        return f"Config {self.id_num}"

    def toJSON(id_num, mappings):
        """Writes the class to a JSON object that can be stored in configuration files."""
        # create a Dictionary to hold the Object
        to_dict = {"id":int(id_num), 
                   "mappings":mappings}
        # dump to a JSON formatted object
        to_json = dumps(to_dict, indent = 4)
        # return the json object
        return to_json