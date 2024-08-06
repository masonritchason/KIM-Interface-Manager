
"""Machines are virtualizations of specific Keyence IM Machines involved in production processes."""

from json import dumps

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

    def toJSON(name, measurements, mapping_configurations):
        """Writes the class to a JSON object that can be stored in configuration files."""
        # create a Dictionary to hold the Object
        to_dict = {"name":str(name), 
                   "measurements":measurements,
                   "mapping_configurations":mapping_configurations}
        # dump to a JSON formatted object
        to_json = dumps(to_dict, indent = 4)
        # return the json object
        return to_json