
"""Models are virtualizations of specific production processes."""

from json import dumps
from classes.Machine import Machine as Machine

# KIM Interface Model Class
class Model:
    # default constructor
    def __init__(self, name, base_information, machines):
        self.name = name
        self.base_information = base_information
        self.machines = machines

    # default print
    def __str__(self):
        return f"Model {self.name}"

    def modelToDict(self):
        """Converts the object to a Dict that can be used in config writing/JSON conversion."""
        # create a Dictionary to hold the Object
        to_dict = {"name":self.name, 
                   "base_information":self.base_information,
                   "machines":[]}
        # add the machines in the machine list as dicts
        for machine in self.machines:
            # convert the machine to a dict
            machine = Machine.machineToDict(machine)
            # append the machine to the existing list
            to_dict['machines'].append(machine)
        # return the dictionary
        return to_dict

    def modelToJSON(self):
        """Writes the class to a JSON object that can be stored in configuration files."""
        # get dictionary format
        to_dict = Model.modelToDict(self)
        # dump to a JSON formatted object
        to_json = dumps(to_dict, indent = 4)
        # return the json object
        return to_json