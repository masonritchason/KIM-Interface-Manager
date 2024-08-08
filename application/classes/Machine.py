
"""Machines are virtualizations of specific Keyence IM Machines involved in production processes."""

from json import dumps
from classes.MappingConfiguration import MappingConfiguration as MappingConfiguration

# KIM Interface Machine Class
class Machine:
    # default constructor
    def __init__(self, name, measurements, mapping_configurations, model):
        self.name = name
        self.measurements = measurements
        self.mapping_configurations = mapping_configurations 
        self.model = model

    # default print
    def __str__(self):
        return f"Machine {self.name}"
    
    def machineToDict(self):
        """Converts the object to a Dict that can be used in config writing/JSON conversion."""
        # create a dictionary to hold the object
        to_dict = {"name":self.name, 
                   "measurements":self.measurements,
                   "mapping_configurations":[]}
        # for each config in the machine's config list
        for config in self.mapping_configurations:
            # convert the config to a dictionary
            config = MappingConfiguration.configToDict(config)
            # append the config dictionary to the machine dictionary
            to_dict['mapping_configurations'].append(config)
        # return the dictionary
        return to_dict

    def machineToJSON(self):
        """Writes the class to a JSON object that can be stored in configuration files."""
        # create a Dictionary to hold the Object
        to_dict = Machine.machineToDict(self)
        # dump to a JSON formatted object
        to_json = dumps(to_dict, indent = 4)
        # return the json object
        return to_json