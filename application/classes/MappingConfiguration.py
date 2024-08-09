
"""Mapping Configurations instruct the Interface to send data to specific places on i-Reporter forms."""

from json import dumps

# KIM Interface Mapping Configuration Class
class MappingConfiguration:
    # default constructor
    def __init__(self, id_num, mappings, machine):
        self.id_num = id_num
        self.mappings = mappings
        self.machine = machine

    # default print
    def __str__(self):
        return f"Config {self.id_num}"

    def configToDict(self):
        """Converts the object to a Dict that can be used in config writing/JSON conversion."""
        # create a dictionary to hold the object
        to_dict = {"id":str(self.id_num), 
                   "mappings":self.mappings}
        # return the dictionary
        return to_dict

    def configToJSON(self):
        """Writes the class to a JSON object that can be stored in configuration files."""
        # get dictionary format
        to_dict = MappingConfiguration.configToDict(self)
        # dump to a JSON formatted object
        to_json = dumps(to_dict, indent = 4)
        # return the json object
        return to_json