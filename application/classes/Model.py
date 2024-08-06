
from json import dumps

# KIM Interface Model Class
class Model:
    # default constructor
    def __init__(self, name, base_information, machines):
        self.name = name
        self.base_information = base_information
        self.machines = machines

    def toJSON(name, base_information, machines):
        """Writes the class to a JSON object that can be stored in configuration files."""
        # create a Dictionary to hold the Object
        to_dict = {"name":str(name), 
                   "base_information":base_information,
                   "machines":machines}
        # dump to a JSON formatted object
        to_json = dumps(to_dict, indent = 4)
        # return the json object
        return to_json