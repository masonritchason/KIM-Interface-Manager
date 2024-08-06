

### KIM_interface_manager.py
# developed for Yamada North America, INC. Quality Assurance by Mason Ritchason
"""KIM_interface_manager.py

Assistive component of the KIM Interface that grants a user-friendly
mapping configuration experience without JSON literacy.
"""


### Libraries Segment
#__________________________________________________________________________________________________
import dearpygui.dearpygui as dpg
import os as os
from json import loads, dumps
from re import compile
from shutil import copytree
from datetime import datetime
from webbrowser import open as web
from classes import Model, Machine, MappingConfiguration


### Global Definition Segmemt
#__________________________________________________________________________________________________
# environment directory
sys_env_dir = os.path.abspath(os.path.join(os.getcwd()))

# detect user signature
user = os.getenv('username')

# get the manager configuration; open the KIM Interface Manager configuration file
File = open(os.path.join(sys_env_dir, "KIM_interface_manager_config.json"), 'r')
# read it
Manager_Config_File = File.read()
# close it
File.close()
# convert from JSON to Dict
Manager_Config_File = loads(Manager_Config_File)
# save the version number
version = Manager_Config_File['version']
# save the version date
version_date = Manager_Config_File['version_date']
# release unnecessary used memory
del(Manager_Config_File)

# create dpg context and viewport
# set up dpg
dpg.create_context()
dpg.create_viewport(title = "KIM Interface Manager - KIM Interface v" + str(version)
    + " - " + str(user), width = 1280, height = 720, x_pos = 0, y_pos = 0)

# initialize StartupWindow
StartupWindow = dpg.window(tag = "startupWindow", pos = [0, 0], width = 1280, height = 720, 
    no_move = True, no_close = True, no_collapse = True, no_title_bar = True)


### Helper Function Segment
#__________________________________________________________________________________________________
# timestamp function adds a timestamp to the top of the config file passed
def timestamp(cfg, filename, action):
    """timestamp(cfg, filename, action)

    cfg: str|dict; the path of the file needing a timestamp update OR
        a file dict object with a timestamp key.
    filename: str; a plaintext name to display on the changelog file entry.
    action: str; a plaintext description of the action performed.
    
    Creates a timestamp on the top of the configuration files. This timestamp
    allows the system to create a collection of backups, created at each launch.
    It also allows users to see when a change was made.
    """
    # try as a file path is passed
    try:
        # open the config file needing a timestamp
        File = open(cfg, 'r')
        # save the file's lines
        text = File.read()
        # close the file
        File.close()
        # format the lines as JSON
        text = loads(text)
        # update the timestamp
        text.update({"timestamp":str(str(datetime.now()) + " | " + str(user))})
        # dump the text to JSON
        text = dumps(text, indent = 4)
        # open the file to write
        File = open(cfg, 'w')
        # write the lines back into the file
        File.writelines(text)
        # close the file
        File.close()
    # not a file
    except Exception:
        # update the timestamp key:value
        cfg.update({"timestamp":str(str(datetime.now()) + " | " + str(user))})
        # return the new config object
    # update the timestamp of the main config file
    File = open(os.path.join(sys_env_dir, "config", "KIM_interface_configuration.json"), 'r')
    text = File.read()
    File.close()
    # format the file as dict
    text = loads(text)
    # update the timestamp
    text.update({"timestamp":str(str(datetime.now()) + " | " + str(user))})
    # format the file as JSON
    text = dumps(text, indent = 4)
    # update the config file
    File = open(os.path.join(sys_env_dir, "config", "KIM_interface_configuration.json"), 'w')
    File.write(text)
    File.close()
    # add entry to the changelog
    File = open(os.path.join(sys_env_dir, "logs", "changelog.txt"), 'a')
    # write the entry to the file
    File.write(str(str(datetime.now()) + " | " + str(user) + " | " 
        + str(filename) + " | " + str(action) + "\n"))
    # close file
    File.close()
    # return the new config item (may not be used if a filepath was passed)
    return cfg


### Config File Management
# openConfigFile reads and returns the KIM Interface configuration
def openConfigFile():
    """openConfigFile()

    Retrieves the Dict Object of the current KIM Interface configuration file.

    -> Dict:Interface_Config_File
    """
    # open the KIM Interface config file
    File = open(os.path.join(sys_env_dir, "config", "KIM_interface_configuration.json"), 'r')
    # read the file
    Interface_Config_File = File.read()
    # convert from JSON to Py Dict
    Interface_Config_File = loads(Interface_Config_File)
    # close
    File.close()
    # return the KIM Interface config object
    return Interface_Config_File

# overwrites the KIM Interface config file with a new config object
def overwriteConfigFile(new_config_object, action):
    """overwriteConfigFile(new_config_object, action)
    
    new_config_object: Dict:Config; the edited Config File object that needs to be
        written over the existing KIM Interface configuration file.
    action: str; a plaintext description of the action performed.

    Overwrites the existing KIM Interface configuration JSON file with an edited version.
    """
    # update the new config object's timestamp
    new_config_object = timestamp(new_config_object, "KIM_interface_configuration.json", action)
    # convert the new config to json
    Interface_Config_File = dumps(new_config_object, indent = 4)
    # open the KIM Interface config file
    File = open(os.path.join(sys_env_dir, "config", "KIM_interface_configuration.json"), 'w')
    # overwrite the KIM Interface config file
    File.write(Interface_Config_File)
    # close the file
    File.close()

# get Configs from the KIM Interface config file
def getConfigs(machine):
    """getConfigs(machine)
    
    Returns the list of Mapping Configurations currently in the passed Machine.

    machine: Machine Object; the Machine to return its Configs.

    -> [Config]
    """
    # create a list to hold the Config objects
    configs = []
    # add Configs from each Machine's Config list in the machines list 
    for i in range(len(machine.mapping_configurations)):
        # save the current Config
        curr = machine.mapping_configurations[i]
        # create a Config object
        TempConfig = MappingConfiguration.MappingConfiguration(curr['id'], curr['mappings'])
        # append that object to the list
        configs.append(TempConfig)
    # return configs list
    return configs

# get Machines from the KIM Interface config file
def getMachines(model):
    """getMachines(model)
    
    Returns the list of Machines currently in the passed Model.

    model: Model Object; the Model object to return its Machines.

    -> [Machine]
    """
    # create a list to hold the Machine objects
    machines = []
    # add Machines from the passed Model's Machine list 
    for i in range(len(model.machines)):
        # save the current Machine
        curr = model.machines[i]
        # create a Machine object
        TempMachine = Machine.Machine(curr['name'], curr['measurements'], curr['mapping_configurations'])
        # fix machine measurement character issues
        for j in range(len(TempMachine.measurements)):
            # save current measurement
            curr = TempMachine.measurements[j]
            # replace characters 
            curr = curr.replace('Ã˜', 'Ø')
            curr = curr.replace('Â±', '±')
            # save the changed measurement
            TempMachine.measurements[j] = curr
        # add the Machine's Configs to its Configs attribute
        TempMachine.mapping_configurations = getConfigs(TempMachine)
        # append that object to the list
        machines.append(TempMachine)
    # return machines list
    return machines

# get Models from the KIM Interface config file
def getModels():
    """getModels()
    
    Returns the list of Models currently in the KIM Interface config file.

    -> [Model]
    """
    # get the KIM Interface config
    Interface_Config_File = openConfigFile()
    # set models
    models = Interface_Config_File['models']
    # convert to a list of Model objects
    for i in range(len(models)):
        # save current Model
        curr = models[i]
        # create a new Model object
        TempModel = Model.Model(curr['name'], curr['base_information'], curr['machines'])
        # add the Model's Machines to its Machines attribute
        TempModel.machines = getMachines(TempModel)
        # overwrite the Model in the models list
        models[i] = TempModel
    # return models list
    return models


### Backup Management
# checkBackupCount maintains a limit of 25 backups in the system
def checkBackupCount():
    """checkBackupCount():
    
    Maintains that there are only 25 previous config backups (excluding the latest).
    Removes the oldest config backup in the case that the count exceeds 25.
    """
    # save the backups directory
    past_backups_dir = os.path.join(sys_env_dir, "bin", "backups", "past")
    # check the number of folders in the past backups folder
    while len(os.listdir(past_backups_dir)) >= 25:
        # scan the size of the folder
        backups = os.listdir(past_backups_dir)
        # does the directory need trimmed?
        if len(backups) >= 25:
            # add the dir root to each file name
            for i in range(len(backups)):
                # add the dir root
                backups[i] = os.path.join(past_backups_dir, backups[i])
            # there are 25+ folders in the past backups folder; remove oldest
            backups = sorted(backups, key = os.path.getctime)
            # clear the files in the directory
            for root, dirs, files in os.walk(top = backups[0], topdown = False):
                # remove all files
                for file in files:
                    os.remove(os.path.join(root, file))
                # remove all dirs
                for folder in dirs:
                    os.rmdir(os.path.join(root, folder))
            # remove the oldest file (first in the list)
            os.rmdir(backups[0])
            backups.pop(0)
        # once here, there is room for another backup in past backups

# pastBackup moves the latest backup to the past folder
def pastBackup():
    """pastBackup()

    Takes the latest backup of the config files and moves it into its own folder
    in the past backups folder. Clears the latest backup from the latest folder.
    """
    # save the backups directories
    latest_dir = os.path.join(sys_env_dir, "bin", "backups", "latest")
    # save the timestamp (used to name the past backup folder)
    File = open(os.path.join(latest_dir, "KIM_interface_configuration.json"), 'r')
    # save the file text
    text = File.read()
    # close the file
    File.close()
    # convert to JSON
    text = loads(text)
    # get the timestamp
    timestamp = text['timestamp']
    # remove milliseconds from timestamp
    timestamp = (timestamp.split('.'))[0]
    # remove invalid directory characters
    timestamp = timestamp.replace(':', '.')
    # save the past backup folder dir
    past_dir = os.path.join(sys_env_dir, "bin", "backups", "past", timestamp)
    # check the past backups folder
    checkBackupCount()
    # if the timestamped config has not already been backed-up
    if not os.path.isdir(past_dir):
        # copy the config tree from the latest to past backup
        copytree(latest_dir, past_dir)
    # clear all files from the latest directory (needs to happen either way)
    for root, dirs, files in os.walk(top = latest_dir, topdown = False):
        # for each file in the tree
        for file in files:
            # remove that file
            os.remove(os.path.join(root, file))
        # for each folder in the tree
        for dir in dirs:
            # remove that folder
            os.rmdir(os.path.join(root, dir))
    # remove the latest folder (recreated by createConfigBackup)
    os.rmdir(latest_dir)

# createConfigBackup maintains a configuration backup
def createConfigBackup():
    """createConfigBackup():
    
    Creates a copy of the current KIM_Interface_Configuration.json file and
    the mapping configurations folder in the bin folder.
    """
    # save the backups directory
    backups_dir = os.path.join(sys_env_dir, "bin", "backups")
    # set the source for copying
    source = os.path.join(sys_env_dir, "config")
    dest = os.path.join(backups_dir, "latest")
    # move the previous latest configuration backup to past packups
    pastBackup()
    # copy the config tree from the config to backup/latest
    copytree(source, dest)


### DPG Window Management
# clears the passed window alias for reuse
def clearWindow(window):
    """clearWindow(window)
    
    window: DPG Window ID; the window to be closed and cleared

    Clears the window that is passed.
    """
    # check if the window exists
    if dpg.does_alias_exist(window):
        # delete the existing window
        dpg.delete_item(window)

# clears all open windows that are not excluded and startupWindow, which it hides
def clearWindowRegistry(exclusions = []):
    """clearWindowRegistry(exlusions = [])

    exclusions: [Empty] by default; list of DPG Window aliases

    Closes all windows in the DPG context that are not the startupWindow;
    Hides the startupWindow;
    Does nothing with windows in exclusions.
    """
    # set a list of program windows
    program_windows = ["selectConfigWindow","addConfigWindow","viewConfigWindow",
        "editConfigWindow","removeConfigWindow","selectMachineWindow","addMachineWindow",
        "viewMachineWindow","editMachineWindow","removeMachineWindow","selectModelWindow",
        "addModelWindow","viewModelWindow","editModelWindow","removeModelWindow",
        "editMachineSubwindow","editModelSubwindow","urlViewWindow","resultsViewWindow",
        "logsViewWindow","informationWindow","helpWindow","contactPopup"]
    # for each item in the program windows list
    for Window in program_windows:
        # window is not excluded
        if not (Window in exclusions):
            # check if the window exists
            if dpg.does_alias_exist(Window):
                # delete the window connected to this alias
                dpg.delete_item(Window)
    # is the startup window excluded?
    if not ("startupWindow" in exclusions):
        # hide the startup window
        dpg.hide_item("startupWindow")
        dpg.hide_item("changelogWindow")

# shows a warning popup with a custom message
def showWarningPopup(warning_message):
    """showWarningPopup(warning_message)
    
    warning_message: str; the message to be displayed to the user.

    Shows an 'error' type warning popup that tells the user something went wrong.
    """
    # clear the warning popup
    clearWindow("warningPopup")
    # create the popup
    WarningPopup = dpg.window(tag = "warningPopup", popup = True, no_open_over_existing_popup = False,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        modal = True)
    # add items to the popup
    with WarningPopup:
        # add a title label
        dpg.add_text("Warning:", color = [255, 150, 75])
        dpg.add_text(warning_message)
        dpg.add_text("Please resolve these issues and try again!", color = [255, 150, 75])
        # add an Okay button
        dpg.add_button(label = "Okay!", width = 150, height = 25, 
            callback = deleteItem, user_data = ["warningPopup"])


#### POSSIBLY OBSOLETE AFTER OOP OVERHAUL
# # open a specific machine mapping file
# def openMachineConfiguration(machine_name):
#     """openMachineConfiguration
    
#     machine_name: str; name of the Machine object.
    
#     Opens the passed Machine's configuration .json file.

#     -> Dict:Machine_file
#     """
#     # create path to mapping config files
#     path = os.path.join(sys_env_dir, "config", "mapping configurations")
#     # add route to model folder
#     path = os.path.join(path, str(machine_name[:3]))
#     # add route to machine .json file
#     path = os.path.join(path, str(machine_name) + ".json")
#     # open the file
#     File = open(os.path.abspath(path), 'r')
#     # read the file
#     Machine_file = File.read()
#     # close
#     File.close()
#     # convert from JSON to Py Dict
#     Machine_file = loads(Machine_file)
#     # return the machine file
#     return Machine_file

# # gets a Model in the KIM Interface config by a passed dpg id
# def getModelObject(ModelItem):
#     """getModelObject(ModelItem)
    
#     ModelItem: Dict:Model; [int, str]:DPG Item; str:ModelName; 
#         the key to search Models by.

#     Returns a Model Object from the KIM Interface config files.

#     -> [Dict:Model]
#     """
#     # first see if the passed item is a dict (Model Object)
#     if type(ModelItem) == dict:
#         # return the object
#         return ModelItem
#     # not a Model object, test as DPG
#     else:
#         try:
#             # get the passed item's value
#             temp = dpg.get_value(ModelItem)
#             # if the item was a valid DPG item, it will return some value
#             if not (temp is None):
#                 # set the model name
#                 Model = dpg.get_value(ModelItem)
#             # otherwise assume the input was actually a Model name (string)
#             else:
#                 # assume the input was actually a Model name (str)
#                 Model = ModelItem
#         # there was an issue getting DPG value
#         except Exception as ex:
#             # warn in console
#             print("Error: " + str(ex) + "; Defaulting to Model Object as: " + str(Model))
#         # get the full Models list from KIM Interface config
#     models = getModels()
#     # find the Model in the list
#     for curr_model in models:
#         # if the names match
#         if curr_model['model_name'] == Model:
#             # set the return Model as the matching Model
#             Model = curr_model
#             break
#     # return the selected Model
#     return Model

# # gets a machine in the KIM Interface config by a passed dpg id
# def getMachineObject(MachineItem):
#     """getMachineObject(MachineItem)
    
#     MachineItem: Dict:Machine; [int, str]:DPG Item; str:MachineName; 
#         the key to search Machines by.

#     Returns a Machine Object from the KIM Interface config files.

#     -> [Dict:Machine]
#     """
#     # first see if the passed item is a dict (Machine Object)
#     if type(MachineItem) == dict:
#         # return the object
#         return MachineItem
#     # not a Machine object, test as DPG
#     else:
#         try:
#             # get the passed item's value
#             temp = dpg.get_value(MachineItem)
#             # if the item was a valid DPG item, it will return some value
#             if not (temp is None):
#                 # set the Machine name
#                 Machine = dpg.get_value(MachineItem)
#             # otherwise assume the input was actually a Machine name (string)
#             else:
#                 # assume the input was actually a Machine name (str)
#                 Machine = MachineItem
#         # there was an issue getting DPG value
#         except Exception as ex:
#             # assume the input was actually a Machine name (str)
#             Machine = MachineItem
#             # warn in console
#             print("Error: " + str(ex) + "; Defaulting to Machine Object as: " + str(Machine))
#         # get the full Machines list from KIM Interface config
#     machines = getMachines()
#     # find the Machine in the list
#     for curr_machine in machines:
#         # if the names match
#         if curr_machine['name'] == Machine:
#             # set the return Machine as the matching Machine
#             Machine = curr_machine
#             break
#     # return the selected Machine
#     return Machine

# # gets a mapping configuration in the config file by machine and ID
# def getConfigObject(Machine, ConfigItem):
#     """getConfigObject(Machine, ConfigItem)
    
#     Machine: Dict:Machine; the Machine object owning the Config.
#     ConfigItem: Dict:Config; [int, str]:DPG Item; str:ConfigName; 
#         the key to search Configs by.

#     Returns a Config Object from the passed machine's configuration file.

#     -> [Dict:Config]
#     """
#     # if the input is a Config object
#     if type(ConfigItem) == dict:
#         # set the id as the Config object's id
#         return ConfigItem
#     # id_input is not an object
#     else:
#         # try treating the input as a DPG item
#         try:
#             # get the item value
#             temp = dpg.get_value(ConfigItem)
#             # if the item was a valid DPG item, it will return some value
#             if not (temp is None):
#                 # set the Config name
#                 Config = dpg.get_value(ConfigItem)
#             # otherwise assume the input was actually a Config ID (string)
#             else:
#                 # assume the input was actually a Config ID (str)
#                 Config = ConfigItem
#         # failed to get the item value
#         except Exception:
#             # passed ID wasn't a DPG item
#             pass
#             # the id is a string, set the ID to the value 
#             Config = str(ConfigItem)
#     # get the machine file
#     machine_file = openMachineConfiguration(Machine['name'])
#     # for each mapping in the machine's config
#     for curr_map in machine_file['mappings']:
#         # check the IDs against each other
#         if str(curr_map['id']) == Config:
#             # pull that Config object
#             Config = curr_map
#             break
#     # return Config
#     return Config

# validates the input of an ADDED config
def validateAddConfigInput(Model, Machine, new_id, info_checks, measurement_checks, 
    info_maps, measurement_maps):
    """
    validateAddConfigInput(Model, Machine, new_id, info_checks, measurement_checks, 
            info_maps, measurement_maps)

    Model: Dict:Model; Model the Config belongs to.
    Machine: Dict:Machine; Machine the Config belongs to.
    new_id: str; input id of the Config.
    info_checks: [DPG Checkboxes]; list of the checkboxes used to select included Model info.
    measurement_checks: [DPG Checkboxes]; list of the checkboxes used to 
        select included Machine measurements.
    info_maps: [DPG Inputs]; list of the inputs used to assign each Model info a sheet/cluster map.
    measurement_maps: [DPG Inputs]; list of the inputs used to assign each Machine measurement a 
        sheet/cluster map.

    Takes a full set of information that defines a Configuration 
    and returns the validation of that info.
    
    -> [Boolean:result, Dict:Config|Error]
    """
    # check that an ID was entered
    if (not new_id) or (new_id is None):
        # no ID entered
        return [False, 
            {"error":"Mapping Configuration IDs cannot be blank."}]
    # some kind of ID was entered
    else:
        # create a regex to compare to (0-9 and '-')
        pattern = compile('^[0-9\\-]+$')
        # if the entered mapping ID does not match
        if not pattern.match(new_id):
            # invalid ID entered
            return [False, 
                {"error":"Mapping Configuration IDs can only contain digits (0-9) and dashes '-'."
                + "\nYou have included an invalid character in this ID."}]
        # valid ID was entered
        else:
            # get the Machine's Config list
            machine_configs = openMachineConfiguration(Machine['name'])
            machine_configs = machine_configs['mappings']
            # check that it is unique
            for config in machine_configs:
                # if the Config IDs match
                if config['id'] == new_id:
                    # overlapping IDs, not unique
                    return [False, 
                        {"error":"Mapping Configuration IDs must be unique.\n"
                        + "The ID " + new_id + " for " + Machine['name'] 
                        + " has already been assigned.\n"
                        + "Choose a different Mapping Configuration ID for this new Configuration."
                        }]
    # create a map list to hold the verified mapping items
    map_list = []
    # track the index of the model base info list
    index = 0
    # verify that each selected information field has a full sheet/cluster map
    for check in info_checks:
        # get values (s p e e d)
        sheet = dpg.get_value(info_maps[index][0])
        cluster = dpg.get_value(info_maps[index][1])
        # if the checkbox was selected
        if dpg.get_value(check):
            # check that there were sheet and cluster #s
            if not (sheet and cluster):
                # bad configuration settings
                return [False, 
                    {"error":"Selected Model Base Information fields must all have\n"
                    + "Sheet and Cluster #'s. You have ommited a # for at least one."}]
            # this map is good to add
            else:
                # add it to the list
                map_list.append(
                    {"item":Model['model_base_information'][index], 
                    "sheet":int(sheet), "cluster":int(cluster), "type":"string", "value":""})
        # increment the model_info_loop
        index += 1
    # track the index of the machine measurement list
    index = 0
    # verify that each selected measurement has a full sheet/cluster map
    for meas in measurement_checks:
        # get values (s p e e d)
        sheet = dpg.get_value(measurement_maps[index][0])
        cluster = dpg.get_value(measurement_maps[index][1])
        # if the checkbox was selected
        if dpg.get_value(meas):
            # check that there were sheet and cluster #s
            if not (sheet and cluster):
                # bad configuration settings
                return [False, 
                    {"error":"Selected Machine Measurements fields must all have\n"
                    + "Sheet and Cluster #'s. You have ommited a # for at least one."}]
            # this map is good to add
            else:
                # add it to the list
                map_list.append(
                    {"item":Machine['measurements'][index], 
                    "sheet":int(sheet), "cluster":int(cluster), "type":"string", "value":""})
        # increment the model_info_loop
        index += 1
    # if here, the Config information can make a Config Object
    Config = {"id":new_id, "configuration":[]}
    # add each of the maps to the configuration list
    for curr_map in map_list:
        # add the item
        Config["configuration"].append(curr_map)
    # return the Config
    return [True, Config]

# validates the input of an EDITED config
def validateEditConfigInput(Model, Machine, Config, new_id, prior_id, checks, inputs):
    """
    validateEditConfigInput(Model, Machine, Config, new_id, prior_id, checks, inputs)

    Model: Dict:Model; Model the Config belongs to
    Machine: Dict:Machine; Machine the Config belongs to
    Config: Dict:Config; the Config being edited
    id: str; edited input id of the Config
    prior_id: str; original id of the Config
    checks: [DPG Checkboxes]; list of the checkboxes used to select included maps
    inputs: [DPG Inputs]; list of the inputs used to assign each map a sheet/cluster map

    Takes a full edited Configuration and returns the validation of that info.
    
    -> [Boolean:result, Dict:Config|Error]
    """
    # get the new_id value from the DPG Input item
    new_id = dpg.get_value(new_id)
    # check that an ID was entered
    if (not new_id) or (new_id is None):
        # no ID entered
        return [False, 
            {"error":"Mapping Configuration IDs cannot be blank."}]
    # some kind of ID was entered
    else:
        # create a regex to compare to (0-9 and '-')
        pattern = compile('[\\-0-9]+')
        # if the entered mapping ID does not match
        if not pattern.match(new_id):
            # invalid ID entered
            return [False, 
                {"error":"Mapping Configuration IDs can only contain digits (0-9) and dashes '-'."
                + "\nYou have included an invalid character in this ID."}]
        # valid ID was entered
        else:
            # get the Machine's Config list
            machine_configs = openMachineConfiguration(Machine['name'])
            machine_configs = machine_configs['mappings']
            # check that it is unique
            for config in machine_configs:
                # if the Config IDs match
                if config['id'] == new_id:
                    # is the match with the prior ID
                    if config['id'] == prior_id:
                        # skip this Config, the ID can match its previous ID
                        continue
                    else:
                        # overlapping IDs, not unique
                        return [False, 
                            {"error":"Mapping Configuration IDs must be unique.\n"
                            + "The ID " + new_id + " for " + Machine['name'] 
                            + " has already been assigned.\n"
                            + "Choose a different Mapping Configuration" 
                            + " ID for this new Configuration."}]
    # create a map list to hold the verified mapping items
    map_list = []
    # track the index of the Config's map list
    index = 0
    # for each check item in the checkbox list
    for check in checks:
        # get values (s p e e d)
        sheet = dpg.get_value(inputs[index][0])
        cluster = dpg.get_value(inputs[index][1])
        # if the checkbox was selected
        if dpg.get_value(check):
            # check that there were sheet and cluster #s
            if not (sheet and cluster):
                # bad configuration settings
                return [False, 
                    {"error":"Selected Configuration maps must all have\n"
                    + "Sheet and Cluster #'s. You have ommited a # for at least one."}]
            # this map is good to add
            else:
                # add it to the list
                map_list.append(
                    {"item":Config['configuration'][index]['item'], "sheet":sheet, 
                    "sheet":int(sheet), "cluster":int(cluster), "type":"string", "value":""})
        # increment the model_info_loop
        index += 1
    # if here, the Config information can make a Config Object
    Config = {"id":new_id, "configuration":[]}
    # add each of the maps to the configuration list
    for curr_map in map_list:
        # add the item
        Config["configuration"].append(curr_map)
    # return the Config
    return [True, Config]

# validates the input of an ADDED Machine
def validateAddMachineInput(Model, machine_name, measurements):
    """
    validateAddMachineInput(Model, machine_name, measurements)

    Model: Dict:Model; Model the Config belongs to.
    machine_name: str; the new Machine's name.
    measurements: [DPG Inputs]; list of the DPG items used to assign each Machine measurement 
        a specification. 

    Takes a full set of information defining a Machine and returns the validation of that info.
    
    -> [Boolean:result, Dict:Machine|Error]
    """
    # check that a name was entered
    if (not machine_name) or (machine_name is None):
        # no name entered
        return [False, 
            {"error":"Machine names cannot be blank."}]
    # some kind of name was entered
    else:
        # create a regex to compare to (0-9, a-z, A-Z, space, and '-')
        pattern = compile('^[a-zA-Z0-9\\- ]+$')
        # if the entered name does not match
        if not pattern.match(machine_name):
            # invalid name entered
            return [False, 
                {"error":"Machine names must be alphanumeric (A-Z, 0-9). They may contain\n"
                + "spaces ' ' and dashes '-' but no other special characters.\n"
                + "You have included an invalid character in this name."}]
        # valid name was entered
        else:
            # get the Model's Machine list
            model_machines = Model['model_machines']
            # check that the name is unique
            for curr_machine in model_machines:
                # if the machine names match
                if curr_machine == machine_name:
                    # overlapping names, not unique
                    return [False, 
                        {"error":"Machine names must be unique.\n"
                        + "The Machine '" + machine_name + "' for " + Model['model_name']
                        + "\nhas already been assigned."
                        + "\nChoose a different name for this Machine."}]
    # create a list to hold valid measurements
    meas_list = []
    # validate the measurement inputs
    for meas in measurements:
        # get the measurement input box value
        meas = dpg.get_value(meas)
        # check that there was a value entered
        if meas:
            # check the length of the measurement
            if len(meas) > 50:
                # this is excessive in length, the input could be malicious
                return [False, 
                    {"error":"Measurement specs must be 50 characters or less.\n"
                    + "One or more spec you have entered is too long."}]
            # the measurement spec is valid
            meas_list.append(meas)
        # the input box was empty, omit this input
        continue
    # if here, the Machine information can make a Machine Object
    Machine = {"name":machine_name, "measurements":[]}
    # add each of the measurements to the measurement list
    for meas in meas_list:
        # add the item
        Machine['measurements'].append(meas)
    # return the Machine
    return [True, Machine]        

# validates the input of an EDITED Machine
def validateEditMachineInput(Model, Machine, new_name, prior_name, checks, inputs):
    """
    validateEditMachineInput(Model, Machine, machine_name, prior_name, checks, inputs)

    Model: Dict:Model; Model the Machine belongs to.
    Machine: Dict:Machine; Machine being edited
    new_name: DPG Input Item; the Inputbox holding the Machine's name after editing.
    prior_name: str; name of the Machine before editing.
    checks: [DPG Checkboxes]; list of the DPG items used to select measurements.
    inputs: [DPG Inputs]; list of the DPG items used to assign each Machine measurement 
        an edited specification.

    Takes an edited Machine and returns the validation of that info. 
    
    -> [Boolean:result, Dict:Machine|Error]
    """
    # get the new_name value from the DPG Input item
    new_name = dpg.get_value(new_name)
    # check that a new name was entered
    if (not new_name) or (new_name is None):
        # no new name entered
        return [False, 
            {"error":"Machine names cannot be blank."}]
    # some kind of new name was entered
    else:
        # create a regex to compare to (0-9, a-z, A-Z, space, and '-')
        pattern = compile('^[a-zA-Z0-9\\- ]+$')
        # if the entered name does not match
        if not pattern.match(new_name):
            # invalid new name entered
            return [False, 
                {"error":"Machine names must be alphanumeric (A-Z, 0-9). They may contain\n"
                + "spaces ' ' and dashes '-' but no other special characters.\n"
                + "You have included an invalid character in this name."}]
        # valid name was entered
        else:
            # get the Model's Machine list
            model_machines = Model['model_machines']
            # check that the name is unique
            for curr_machine in model_machines:
                # if the machine names match
                if curr_machine == new_name:
                    # if the match is with the prior machine name
                    if curr_machine == prior_name:
                        # the match is okay, no edit was made to the machine name
                        continue
                    # the new name is another machine's name
                    else:
                        # overlapping names, not unique
                        return [False, 
                            {"error":"Machine names must be unique.\n"
                            + "The Machine '" + new_name + "' for " + Model['model_name']
                            + "\nhas already been assigned."
                            + "\nChoose a different name for this Machine."}]
    # create a list to hold valid measurements
    meas_list = []
    # hold a measurement index
    index = 0
    # for each checkbox on measurements
    for check in checks:
        # if the checkbox was selected
        if dpg.get_value(check):
            # get the measurement input box value
            meas = dpg.get_value(inputs[index])
            # check that there was a value entered
            if meas and not ((meas is None) and (meas == "")):
                # check the length of the measurement
                if len(meas) > 50:
                    # this is excessive in length, the input could be malicious
                    return [False, 
                        {"error":"Measurement specs must be 50 characters or less.\n"
                        + "One or more spec you have entered is too long."}]
            # the selected measurement spec input box was empty
            else:
                # this is invalid
                return [False, 
                    {"error":"Selected measurement specs must have a value.\n"
                    + "One or more spec you have selected does not have a value."}]
            # the measurement spec is valid
            meas_list.append(meas)
        # increment the index
        index += 1
    # if here, the Machine information can make a Machine Object
    Machine = {"name":new_name, "measurements":[]}
    # add each of the measurements to the measurement list
    for meas in meas_list:
        # add the item
        Machine['measurements'].append(meas)
    # return the Machine
    return [True, Machine]   

# validates the input of an ADDED model
def validateAddModelInput(model_name, base_information):
    """
    validateAddModelInput(model_name, base_information)

    model_name: str; name of the new model
    base_information: [DPG Inputs]; list of the DPG items used to assign each Model base
        information field a header. 

    Takes a full set of information defining a Model and returns the validation of that info.
    
    -> [Boolean:result, Dict:Model|Error]
    """
    # check that a name was entered
    if (not model_name) or (model_name is None):
        # no name entered
        return [False, 
            {"error":"Model names cannot be blank."}]
    # some kind of name was entered
    else:
        # check the name's length (MUST be exactly 3)
        if not (len(model_name) == 3):
            # model name is too short or long
            return [False, 
                {"error":"Model names must be 3 characters in length."}]
        # create a regex to compare to (0-9, A-Z)
        pattern = compile('^[A-Z0-9]+$')
        # if the entered name does not match
        if not pattern.match(model_name):
            # invalid name entered
            return [False, 
                {"error":"Model names can only contain capital letters and digits.\n"
                + "You have included an invalid character in this name."}]
        # valid name was entered
        else:
            # get the Model list
            models = getModels()
            # check that the name is unique
            for curr_model in models:
                # if the model names match
                if curr_model['model_name'] == model_name:
                    # overlapping names, not unique
                    return [False, 
                        {"error":"Model names must be unique.\n"
                        + "The Model '" + model_name + "' has already been defined.\n"
                        + "Choose a different name for this Model."}]
    # create a list to hold valid base information headers
    info_list = []
    # validate the base information inputs
    for info in base_information:
        # get the base information input box value
        info = dpg.get_value(info)
        # check that there was a value entered
        if info:
            # check the length of the base information
            if len(info) > 50:
                # this is excessive in length, the input could be malicious
                return [False, 
                    {"error":"Base information headers must be 50 characters or less.\n"
                    + "One or more header you have entered is too long."}]
            # the base information is valid
            info_list.append(info)
        # the input box was empty, omit this input
        continue
    # if here, the Model information can make a Model Object
    Model = {"model_name":model_name, "model_base_information":[], "model_machines":[]}
    # add each base information to the base information list
    for info in info_list:
        # add the item
        Model['model_base_information'].append(info)
    # return the Model
    return [True, Model]  

# validates the input of an EDITED model
def validateEditModelInput(Model, new_name, prior_name, checks, inputs):
    """
    validateEditModelInput(Model, new_name, prior_name, checks, inputs)

    Model: Dict:Model; Model being edited.
    new_name: DPG Input Item; the Inputbox holding the Model's name after editing.
    prior_name: str; name of the Model before editing.
    checks: [DPG Checkboxes]; list of the DPG items used to select base information.
    inputs: [DPG Inputs]; list of the DPG items used to assign each Model base 
        information an edited header. 
    
    Takes an edited Model and returns the validation of that info.
    
    -> [Boolean:result, Dict:Model|Error]
    """
    # check that a name was entered
    if (not new_name) or (new_name is None):
        # no name entered
        return [False, 
            {"error":"Model names cannot be blank."}]
    # some kind of name was entered
    else:
        # check the name's length (MUST be exactly 3)
        if not (len(new_name) == 3):
            # model name is too short or long
            return [False, 
                {"error":"Model names must be 3 characters in length."}]
        # create a regex to compare to (0-9, A-Z)
        pattern = compile('^[A-Z0-9]+$')
        # if the entered name does not match
        if not pattern.match(new_name):
            # invalid name entered
            return [False, 
                {"error":"Model names can only contain capital letters and digits.\n"
                + "You have included an invalid character in this name."}]
        # valid name was entered
        else:
            # get the Model list
            models = getModels()
            # check that the name is unique
            for curr_model in models:
                # if the model names match
                if curr_model['model_name'] == new_name:
                    # if the match is with the prior model name
                    if curr_model['model_name'] == prior_name:
                        # this is okay, skip the match
                        continue
                    else:
                        # overlapping names, not unique
                        return [False, 
                            {"error":"Model names must be unique.\n"
                            + "The Model '" + new_name + "' has already been defined.\n"
                            + "Choose a different name for this Model."}]
    # create a list to hold valid base information headers
    info_list = []
    # hold a base information index
    index = 0
    # for each checkbox on base information
    for check in checks:
        # if the checkbox was selected
        if dpg.get_value(check):
            # get the base information input box value
            info = dpg.get_value(inputs[index])
            # check that there was a value entered
            if info and not ((info is None) and (info == "")):
                # check the length of the base information header
                if len(info) > 50:
                    # this is excessive in length, the input could be malicious
                    return [False, 
                        {"error":"Base Information headers must be 50 characters or less.\n"
                        + "One or more header you have entered is too long."}]
            # the selected base information header input box was empty
            else:
                # this is invalid
                return [False, 
                    {"error":"Selected Base Information headers must have a value.\n"
                    + "One or more header you have selected does not have a value."}]
            # the base information header is valid
            info_list.append(info)
        # increment the index
        index += 1
    # if here, the Model information can make a Model Object
    Model = {"model_name":new_name, "model_base_information":[], 
        "model_machines":Model['model_machines']}
    # add each of the base information headers to the list
    for info in info_list:
        # add the item
        Model['model_base_information'].append(info)
    # return the Model
    return [True, Model]


# currentAverageRuntime allows calculation of the current average runtime of the script
def currentAverageRuntime():
    """currentAverageRuntime()
    
    Calculates the average runtime of the system based on the current information in runtime_log.txt.
    """
    # open the runtime_log.txt file
    log = os.path.join(sys_env_dir, "logs", "runtime_log.txt")
    File = open(log, 'r')
    # get lines from the file
    lines = File.readlines()
    # close log
    File.close()
    # initialize a count and a total
    count = 0
    total = 0
    # for loop over the lines in runtime log
    for line in lines:
        # if line isnt blank
        if line != '\n':
            # get the tracked time of the run
            runtime = line.split(' ')
            # convert to a float value
            runtime = float(runtime[3])
            # add to total
            total += runtime
            # increment count
            count += 1
    # use total / count to calculate average
    average_runtime = total / count
    # output average
    return ('{:f}'.format(average_runtime) + " seconds per script call")


### Callback Segment
#__________________________________________________________________________________________________
## GENERAL CALLBACKS
# callback that ends the program
def closeProgram(sender, app_data, user_data):
    """closeProgram()
    
    Callback that closes the program on invoke.
    """
    # create a new backup
    createConfigBackup()
    # exit the program
    dpg.destroy_context()
    raise SystemExit(1)

# deletes the passed item
def deleteItem(sender, app_data, user_data):
    """deleteItem(user_data = [destroyed_item])
    
    destroyed_item: DPG Item ID; the DPG Item to be destroyed.

    Destroys the passed DPG Item.
    """
    # destroy the item
    dpg.delete_item(user_data[0])

# returns to the startupWindow from anywhere
def returnToStartup(sender, app_data, user_data):
    """returnToStartup()
    
    Returns the UI to the startup (main) window.
    """
    # clear the windows
    clearWindowRegistry()
    # show the startup window
    dpg.show_item("startupWindow")
    dpg.show_item("changelogWindow")
    # make the startup window the primary window
    dpg.set_primary_window("startupWindow", True)


## CONFIG UI CALLBACKS
#__________________________________________________________________________________________________
# makes an edit to a config in the mapping configurations file
def commitConfigEdits(sender, app_data, user_data):
    """commitConfigEdits(user_data = [continueCode, Model, Machine, 
        Config, new_id, prior_id, checks, inputs])
    
    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning this Config
    Machine: Dict:Machine; Machine Object owning this Config
    Config: Dict:Config; Config Object being edited
    new_id: DPG item; Input box holding the edited ID of the Config
    prior_id: str; ID of the Config before edits
    checks: [DPG Checkboxes]; list of edited selected Config items
    inputs: [DPG Input boxes]; list of edited selected Config item maps

    Commits a user edit to a mapping configuration in the system environment.
    """
    # get continue code
    continueCode = user_data[0]
    # get the Model that owns this Config
    Model = user_data[1]
    # get the Machine that owns this configuration
    Machine = user_data[2]
    # get the edited Config
    Config = user_data[3]
    # get the edited ID
    new_id = user_data[4]
    # get the prior id
    prior_id = user_data[5]
    # get the edited selected config fields
    checks = user_data[6]
    # get the edited selected config field maps
    inputs = user_data[7]
    # get the actual values of the entries
    for check in checks:
        check = dpg.get_value(check)
    for inp in inputs:
        inp = dpg.get_value(inp)
    # validate the new Config's information
    validation = validateEditConfigInput(Model, Machine, Config, 
        new_id, prior_id, checks, inputs)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new Config object
        showWarningPopup(validation[1]['error'])
    # valid Config input
    else:
        # input was valid, continue
        EditedConfig = validation[1]
        # get the machine file
        machine_file = openMachineConfiguration(Machine['name'])
        # get the index of the edited Config
        config_index = machine_file['mappings'].index(Config)
        # update the value of that index
        machine_file['mappings'][config_index] = EditedConfig
        # timestamp the file
        machine_file = timestamp(machine_file, str(Machine['name']) + ".json", 
            "Edit Configuration: " + str(Machine['name']) + "; ID # " + str(EditedConfig['id']))
        # dump config to JSON
        machine_file = dumps(machine_file, indent = 4)
        # overwrite the config file
        File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
            Machine['name'][:3], Machine['name'] + ".json"), 'w')
        # overwrite the config
        File.write(machine_file)
        # close the file
        File.close()
        # update the Config Object in runtime memory
        Config = getConfigObject(Machine, Config['id'])
        # clear the Popup alias
        clearWindow("confirmPopup")
        # create the confirmation popup
        Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = True,
            width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
            pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
            modal = True)
        # add items to the popup
        with Popup:
            # add a success message
            dpg.add_text("Success:", color = [150, 150, 255])
            dpg.add_text("Your edits to " + Machine['name'] + "'s configuration\n"
                + "ID # " + str(Config['id']) + " have been saved.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewConfig, user_data = ["viewConfig", Model, Machine, Config])

# add a new configuration to the mappings files
def commitConfigAdd(sender, app_data, user_data):
    """commitConfigAdd(user_data = [continueCode, Model, Machine, config_id, 
        model_info_checks, machine_measurement_checks, model_info_mappings, machine_meas_mappings])
    
    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning this Config's Machine
    Machine: Dict:Machine; Machine Object owning this Config
    config_id: str; new Config's ID number
    model_info_checks: [DPG Checkboxes]; selected Model base info for Config
    machine_measurement_checks: [DPG Checkboxes]; selected Machine measurements for Config
    model_info_mappings: [DPG Input boxes]; maps for selected Model base info 
    machine_meas_mappings: [DPG Input boxes]; maps for selected Machine measurements

    Commits an addition of a new mapping configuration to the system environment.
    """
    # get continue code
    continueCode = user_data[0]
    # get the Model that owns the Config
    Model = user_data[1]
    # get the Machine that owns the Config
    Machine = user_data[2]
    # get the Config ID
    config_id = dpg.get_value(user_data[3])
    # get the selection information lists
    model_info_checks = user_data[4]
    machine_measurement_checks = user_data[5]
    info_mappings = user_data[6]
    meas_mappings = user_data[7]
    # validate the new Config's information
    validation = validateAddConfigInput(Model, Machine, config_id, 
        model_info_checks, machine_measurement_checks, info_mappings, meas_mappings)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new Config object
        showWarningPopup(validation[1]['error'])
    # valid Config input
    else:
        # input was valid, continue
        NewConfig = validation[1]
        # get the machine file
        machine_file = openMachineConfiguration(Machine['name'])
        # add the new Config to the Machine object
        machine_file['mappings'].append(NewConfig)
        # fix corrupt character writing
        for curr_mapping in machine_file['mappings']:
            for curr_item in curr_mapping['configuration']:
                curr_item['item'] = curr_item['item'].replace('Ã˜', 'Ø')
                curr_item['item'] = curr_item['item'].replace('Â±', '±')
        # write the machine's information to its file after appending the new mapping
        # timestamp the file
        machine_file = timestamp(machine_file, str(Machine['name']) + ".json", 
            "Add Configuration: " + str(Machine['name']) + "; ID # " + str(NewConfig['id']))
        # reformat the machine_file text into JSON
        machine_file = dumps(machine_file, indent = 4)
        # open the machine's file
        File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
            str(Model['model_name']), str(Machine['name']) + ".json"), 'w')
        # write to the file
        File.write(machine_file)
        # close the machine file
        File.close()
        # update the Config Object in runtime memory
        Config = getConfigObject(Machine, NewConfig['id'])
        # clear the Popup alias
        clearWindow("confirmPopup")
        # create the confirmation popup
        Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = True,
            width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
            pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
            modal = True)
        # add items to the popup
        with Popup:
            # add a success message
            dpg.add_text("Success:", color = [150, 150, 255])
            dpg.add_text("Your new mapping configuration ID # " + str(NewConfig['id']) 
                + "\nfor " + Machine['name'] + " has been added.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewConfig, user_data = ["viewConfig", Model, Machine, Config])

# duplicates a config in the mapping configurations file
def commitConfigDuplicate(sender, app_data, user_data):
    """commitConfigDuplicate(user_data = [continueCode, Model, Machine, Config, ConfigID])
    
    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; the Model owning the duplicated Config.
    Machine: Dict:Machine; the Machine owning the duplicated Config.
    Config: Dict:Config; Config Object to be duplicated.
    ConfigID: DPG Inputbox; Item holding the duplicate Config's ID

    Commits the duplication of a mapping configuration in the system environment
    """
    # get continue code
    continueCode = user_data[0]
    # get the Model
    Model = user_data[1]
    # get the Machine
    Machine = user_data[2]
    # get the duplicated config
    Config = user_data[3]
    # get the ID
    ConfigID = dpg.get_value(user_data[4])
    # get the machine file
    machine_file = openMachineConfiguration(Machine['name'])
    # validate the Config's ID
    # create a regex to compare to (0-9 and '-')
    pattern = compile('^[0-9\\-]+$')
    # if the entered mapping ID does not match
    if not pattern.match(ConfigID):
        # invalid ID entered
        showWarningPopup("Mapping Configuration IDs can only contain digits (0-9) and dashes '-'."
            + "\nYou have included an invalid character in this ID.")
        # destroy the popup
        clearWindow("duplicateConfigPopup")
        return
    # valid ID was entered
    else:
        # get the Machine's Config list
        machine_configs = machine_file['mappings']
        # check that it is unique
        for config in machine_configs:
            # if the Config IDs match
            if config['id'] == ConfigID:
                # overlapping IDs, not unique
                showWarningPopup("Mapping Configuration IDs must be unique.\n"
                    + "The ID " + ConfigID + " has already been assigned.\n"
                    + "Choose a different Mapping Configuration ID for this new Configuration.")
                # destroy the popup
                clearWindow("duplicateConfigPopup")
                return
    # ID is acceptable, duplicate the Config
    temp = Config
    DuplicateConfig = temp
    # set the duplicate Config's ID
    DuplicateConfig.update(id = ConfigID)
    # add the new Config to the Machine object
    machine_file['mappings'].append(DuplicateConfig)
    # fix corrupt character writing
    for curr_mapping in machine_file['mappings']:
        for curr_item in curr_mapping['configuration']:
            curr_item['item'] = curr_item['item'].replace('Ã˜', 'Ø')
            curr_item['item'] = curr_item['item'].replace('Â±', '±')
    # write the machine's information to its file after appending the new mapping
    # timestamp the file
    machine_file = timestamp(machine_file, str(Machine['name']) + ".json", 
        "Duplicate Configuration: " + str(Machine['name']) + "; ID # " + str(DuplicateConfig['id']))
    # reformat the machine_file text into JSON
    machine_file = dumps(machine_file, indent = 4)
    # open the machine's file
    File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
        Model['model_name'], Machine['name'] + ".json"), 'w')
    # write to the file
    File.write(machine_file)
    # close the machine file
    File.close()
    # clear the Popup alias
    clearWindow("confirmPopup")
    # create the confirmation popup
    Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = False,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        modal = True)
    # add items to the popup
    with Popup:
        # add a success message
        dpg.add_text("Success:", color = [150, 150, 255])
        dpg.add_text("Your duplicate mapping configuration ID # " + DuplicateConfig['id'] 
            + "\nfor " + Machine['name'] + " has been created.")
        # add an Okay button
        dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
            callback = viewConfig, user_data = ["viewConfig", Model, Machine, Config])

# removes a config from the mapping configurations file
def commitConfigRemove(sender, app_data, user_data):
    """commitConfigRemove(user_data = [continueCode, Model, Machine, Config])
    
    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning this Config's Machine
    Machine: Dict:Machine; Machine Object owning this Config
    Config: Dict:Config; Config Object to be removed

    Commits the removal of a mapping configuration from the system environment.
    """
    # get continue code
    continueCode = user_data[0]
    # get the Model Object owning this Config
    Model = user_data[1]
    # get the Machine Object to be removed
    Machine = user_data[2]
    # get the removed config
    Config = user_data[3]
    # get the machine file
    machine_file = openMachineConfiguration(Machine['name'])
    # initialize a list index
    index = 0
    # find the config in the list
    for curr_mapping in machine_file['mappings']:
        # if the names match
        if curr_mapping['id'] == Config['id']:
            # remove that config from the list
            machine_file['mappings'].remove(Config)
            # break the loop
            break
        # increment the index
        index += 1
    # timestamp the file
    machine_file = timestamp(machine_file, str(Machine['name']) + ".json", 
        "Remove Configuration: " + str(Machine['name']) + "; ID # " + str(Config['id']))
    # convert the new config to json
    machine_file = dumps(machine_file, indent = 4)
    # open the machine config file
    File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
        Model['model_name'], Machine['name'] + ".json"), 'w')
    # overwrite the config file
    File.write(machine_file)
    # close the file
    File.close()
    # clear the remove popup
    clearWindow("removeConfig")
    # clear the Popup alias
    clearWindow("confirmPopup")
    # create the confirmation popup
    Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = False,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        modal = True)
    # add items to the popup
    with Popup:
        # add a success message
        dpg.add_text("Success:", color = [150, 150, 255])
        dpg.add_text("Your mapping configuration ID # " + Config['id'] 
            + "\nfor " + Machine['name'] + " has been removed.")
        # add an Okay button
        dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
            callback = selectModel, user_data = ["viewConfig"])

# add config flow
def addConfig(sender, app_data, user_data):
    """
    addConfig(user_data = [continueCode, Model, Machine])
    
    SelectMachineWindow -> AddConfigWindow

    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    Model: Dict:Model; the Model owning the Machine that is being added to.
    Machine: Dict:Machine; the Machine owning the new Config.
    
    Invokes the UI flow from the SelectMachineWindow to the AddConfigWindow.
    Invoked by the menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the Model Object owning this Config
    Model = getModelObject(user_data[1])
    # get the Machine Object to be removed
    Machine = getMachineObject(user_data[2])
    # clear windows
    clearWindowRegistry()
    # create the AddConfigWindow
    AddConfigWindow = dpg.window(tag = "addConfigWindow", pos = [0, 0], width = 1280, height = 720,
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the window
    with AddConfigWindow:
        # make the new window the primary window
        dpg.set_primary_window("addConfigWindow", True)
        # back button
        dpg.add_button(label = "<- Main Menu / Add a new Config...", pos = [10, 25],
            callback = selectModel, user_data = ["addConfig"])
        # add config text label
        dpg.add_text("Add a new Mapping Configuration for the KIM Interface to use.\n"
            + "-  Select the information fields you want to use on the form;\n"
            + "   assign each information field a sheet and cluster number.\n"
            + "-  Configuration IDs must be unique and contain only numbers and dashes.", pos = [75, 75])
        # machine name label
        dpg.add_text("Machine Name: " + Machine['name'], pos = [75, 200])
        # mapping ID label
        dpg.add_text("Enter Configuration ID #:", pos = [75, 225])
        # mapping ID entry box
        NewConfigID = dpg.add_input_text(width = 100, pos = [250, 225])
        # warn for ID uniqueness
        dpg.add_text("! - Mapping IDs must be unique.", color = [150, 150, 255], pos = [350, 225])
        # information fields label
        dpg.add_text("Information Fields:", pos = [75, 250])
        # measurement fields label
        dpg.add_text("Measurement Fields:", pos = [700, 75])
        # sheet/cluster # labels
        dpg.add_text("Sheet #", pos = [300, 250])
        dpg.add_text("Cluster #", pos = [400, 250])
        dpg.add_text("Sheet #", pos = [1000, 75])
        dpg.add_text("Cluster #", pos = [1100, 75])
        # warn for use instructions
        dpg.add_text("! - Select to include;", color = [150, 150, 255], pos = [1175, 100])
        dpg.add_text("! - Enter Sheet/Cluster #.", color = [150, 150, 255], pos = [1175, 125])
        # set an incrementing position offset
        pos_offset = 1
        # initialize a list of created checkboxes & sheet/cluster mappings
        # lists for model base info
        info_checkboxes = []
        info_mappings = []
        # lists for machine measurements
        measurement_checkboxes = []
        measurement_mappings = []
        # for each field of base information
        for curr_info in Model['model_base_information']:
            # calculate positional offset
            offset = 250 + (25 * pos_offset)
            # add a text label w/its name
            dpg.add_text(curr_info, pos = [75, offset])
            # add a toggle checkbox
            info_checkboxes.append(dpg.add_checkbox(default_value = False, pos = [200, offset]))
            # add a sheet # and cluster # input
            input_pair = [dpg.add_input_text(width = 75, pos = [300, offset]),
                dpg.add_input_text(width = 75, pos = [400, offset])]
            # add that mapping pair to the mapping list
            info_mappings.append(input_pair)
            # increment the position offset
            pos_offset += 1
        # reset the incrementing position offset
        pos_offset = 1
        # for each field of machine measurements
        for meas in Machine['measurements']:
            # calculate positional offset
            offset = 75 + (25 * pos_offset)
            # add a text label w/its name
            dpg.add_text(meas, pos = [700, offset])
            # add a toggle checkbox
            measurement_checkboxes.append(dpg.add_checkbox(default_value = False, pos = [900, offset]))
            # add a sheet # and cluster # input
            input_pair = [dpg.add_input_text(width = 75, pos = [1000, offset]), 
                dpg.add_input_text(width = 75, pos = [1100, offset])]
            # add that mapping pair to the mapping list
            measurement_mappings.append(input_pair)
            # increment the position offset
            pos_offset += 1
        # add 'finalize' config button
        dpg.add_button(label = "Add Mapping Configuration", callback = commitConfigAdd, 
            user_data = ["viewConfig", Model, Machine, NewConfigID, info_checkboxes, measurement_checkboxes, 
            info_mappings, measurement_mappings], pos = [50, 620],
            width = 300)

# remove config flow
def removeConfig(sender, app_data, user_data):
    """removeConfig(user_data = [continueCode, Model, Machine, Config])

    ViewConfigWindow -> RemoveConfigWindow

    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    Model: Dict:Model; the Model owning the Machine that is being removed from.
    Machine: Dict:Machine; the Machine owning the removed Config.
    Config: Dict:Config; the Config being removed.
    
    Invokes the UI flow from the ViewConfigWindow to the RemoveConfigWindow.
    Invoked by the selection of "Remove Config" in ViewConfigWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model
    Model = user_data[1]
    # get machine 
    Machine = user_data[2]
    # get the config from the selected ID
    Config = getConfigObject(Machine, user_data[3])
    # clear popup alias
    clearWindow("removeConfig")
    # create a popup window
    RemoveConfigPopup = dpg.window(tag = "removeConfig", popup = True, no_open_over_existing_popup = True,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        modal = True)
    # add items to the popup
    with RemoveConfigPopup:
        # add a warning
        dpg.add_text("Warning:", color = [255, 0, 50])
        dpg.add_text("Removing a Config from the Interface is 100" + '%' + "\n" 
            + "irreversible! Only perform this action if you\n"
            + "are completely sure that it is out-of-use.")
        # add a Cancel button
        dpg.add_button(label = "Cancel", pos = [10, 100], width = 180, height = 25,
            callback = deleteItem, user_data = ["removeConfig"])
        # add a Delete button
        dpg.add_button(label = "Delete", pos = [200, 100], width = 180, height = 25,
            callback = commitConfigRemove, user_data = ["removeConfig", Model, Machine, Config])

# edit config flow
def editConfig(sender, app_data, user_data):
    """editConfig(user_data = [continueCode, Model, Machine, Config])

    ViewConfigWindow -> EditConfigWindow

    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    Model: Dict:Model; the Model owning the Machine that is being edited.
    Machine: Dict:Machine; the Machine owning the edited Config.
    Config: Dict:Config; the Config being edited.
    
    Invokes the UI flow from the ViewConfigWindow to the EditConfigWindow.
    Invoked by the selection of "Edit Config" in ViewConfigWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model
    Model = user_data[1]
    # get machine 
    Machine = user_data[2]
    # get the config from the selected ID
    Config = getConfigObject(Machine, user_data[3])
    # set the prior_id value before edits made
    prior_id = Config['id']
    # clear windows
    clearWindowRegistry()
    # enable the EditConfigWindow
    EditConfigWindow = dpg.window(tag = "editConfigWindow", pos = [0, 0], width = 1280, height = 720,
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the EditConfigWindow
    with EditConfigWindow:
        # make the new window the primary window
        dpg.set_primary_window("editConfigWindow", True)
        # back button
        dpg.add_button(label = "<- ... / View Configuration / Edit Configuration...",
            callback = selectModel, user_data = ["editConfig"], pos = [10, 25])
        # add a config name label
        dpg.add_text("Configuration ID #:\n\nfor " + Machine['name'], pos = [75, 100])
        # add an input box to allow editing of ID
        IDInput = dpg.add_input_text(pos = [210, 100], width = 100, default_value = Config['id'],
            hint = "New ID...")
        # add a mapping list
        dpg.add_text("Included Fields:", pos = [75, 200])
        dpg.add_text("sheet #", pos = [250, 200])
        dpg.add_text("cluster #", pos = [350, 200])
        # set a positional offset
        pos_offset = 1
        # create a list to hold the input boxes
        inputs = []
        # create a list to hold the checkboxes
        checks = []
        # for each cluster mapping in the configuration
        for curr_map in Config['configuration']:
            # add a text item for that field
            dpg.add_text(curr_map['item'] + ":", pos = [75, 200 + (pos_offset * 25)])
            # add a checkbox for this field
            checks.append(dpg.add_checkbox(pos = [200, 200 + (pos_offset * 25)], default_value = True))
            # add a sheet # input box
            SheetsInput = dpg.add_input_text(default_value = curr_map['sheet'], 
                pos = [250, 200 + (pos_offset * 25)], width = 75, hint = "Clear Map")
            # add a cluster # input box
            ClustersInput = dpg.add_input_text(default_value = curr_map['cluster'], 
                pos = [350, 200 + (pos_offset * 25)], width = 75, hint = "Clear Map")
            # add the mapping and its header to the mapping input list
            inputs.append([SheetsInput, ClustersInput])
            # increment positional offset
            pos_offset += 1
        # add informational text
        dpg.add_text("! - De-selecting an existing Mapping Field will\n" 
                    + "    remove it from the Configuration's mappings.\n"
                    + "    This should be avoided, if possible.", 
                    pos = [450, 225], color = [150, 150, 255])
        # add a Finish Editing button
        dpg.add_button(label = "Finish Editing Configuration...", width = 270, pos = [50, 600],
            callback = commitConfigEdits, user_data = 
            ["editConfig", Model, Machine, Config, IDInput, prior_id, checks, inputs])

# duplicate config flow
def duplicateConfig(sender, app_data, user_data):
    """duplicateConfig(user_data = [continueCode, Model, Machine, Config])
    
    ViewConfigWindow -> DuplicateConfigWindow

    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    Model: Dict:Model; the Model owning the Config that is being duplicated.
    Machine: Dict:Machine; the Machine owning the duplicated Config.
    Config: Dict:Config; the Config being duplicated.

    Invokes the UI flow from the viewConfigWindow to the duplicateConfigWindow.
    Invoked by clicking the Duplicate this Config button on the viewConfigWindow
    """
    # get continue code
    continueCode = user_data[0]
    # get the Model
    Model = user_data[1]
    # get the machine
    Machine = user_data[2]
    # get the config to duplicate
    DuplicatedConfig = user_data[3]
    # clear the duplicateConfigPopup window
    clearWindow("duplicateConfigPopup")
    # create a popup to get the duplicate config's ID
    Popup = dpg.window(tag = "duplicateConfigPopup", popup = True, no_open_over_existing_popup = False,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        modal = True)
    # add items to the popup
    with Popup:
        # add a label
        dpg.add_text("Duplicating Mapping Configuration ID #" + str(DuplicatedConfig['id'])
            + "\nPlease enter the duplicate Configuration's ID:")
        # add an input box
        IDInput = dpg.add_input_text(hint = "ID #...", width = 300, 
            default_value = DuplicatedConfig['id'])
        # add an add field button
        dpg.add_button(label = "Duplicate Configuration", pos = [5, 100], 
            callback = commitConfigDuplicate, user_data = 
            ["duplicateConfig", Model, Machine, DuplicatedConfig, IDInput])
        # add a cancel button
        dpg.add_button(label = "Cancel", pos = [200, 100], 
            callback = deleteItem, user_data = ["duplicateConfigPopup"])

# view config flow
def viewConfig(sender, app_data, user_data):
    """viewConfig(user_data = [continueCode, Model, Machine, Config])

    SelectConfigWindow -> ViewConfigWindow

    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    Model: Dict:Model; the Model owning the Machine that is being viewed.
    Machine: Dict:Machine; the Machine owning the viewed Config.
    Config: Dict:Config; the Config being viewed.
    
    Invokes the UI flow from the SelectConfigWindow to the ViewConfigWindow.
    Invoked by the selection of a config or the menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model
    Model = user_data[1]
    # get machine 
    Machine = user_data[2]
    # get the config from the selected ID
    Config = getConfigObject(Machine, user_data[3])
    # clear windows
    clearWindowRegistry()
    # enable the ViewConfigWindow
    ViewConfigWindow = dpg.window(tag = "viewConfigWindow", pos = [0, 0], width = 1280, height = 720,
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the ViewConfigWindow
    with ViewConfigWindow:
        # make the new window the primary window
        dpg.set_primary_window("viewConfigWindow", True)
        # back button
        dpg.add_button(label = "<- ... / Select a Configuration / View Configuration...",
            callback = selectModel, user_data = ["viewConfig"], pos = [10, 25])
        # add a config ID label
        dpg.add_text("Configuration ID #: " + Config['id'] + "\nfor " + Machine['name'], 
            pos = [75, 100])
        # add a mapping list
        dpg.add_text("Cluster Mappings:", pos = [75, 200])
        # set a positional offset
        pos_offset = 1
        # for each mapping in the list
        for curr_mapping in Config['configuration']:
            # add a text item for that field
            dpg.add_text("-   " + str(curr_mapping['item']) + "; sheet #" + str(curr_mapping['sheet']) 
                + "; cluster #" + str(curr_mapping['cluster']), pos = [80, 200 + (pos_offset * 25)])
            # increment positional offset
            pos_offset += 1
        # add Config Actions side panel
        dpg.add_text("Configuration Actions:", pos = [800, 200])
        # add action buttons
        dpg.add_button(label = "Edit this Configuration       ->", pos = [800, 225],
            callback = editConfig, user_data = ["editConfig", Model, Machine, Config])
        dpg.add_button(label = "Remove this Configuration     !!", pos = [800, 250],
            callback = removeConfig, user_data = ["removeConfig", Model, Machine, Config])
        dpg.add_button(label = "Duplicate this Configuration  ->", pos = [800, 275],
            callback = duplicateConfig, user_data = ["duplicateConfig", Model, Machine, Config])

# select config flow
def selectConfig(sender, app_data, user_data):
    """selectConfig(user_data = [continueCode, Model, Machine])

    StartupWindow -> SelectConfigWindow
    
    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    Model: Dict:Model; the Model owning the Machine that is being selected from.
    Machine: Dict:Machine; the Machine being selected from.

    Invokes the UI flow from the StartupWindow to the SelectConfigWindow.
    Invoked by the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get Model
    Model = user_data[1]
    # get Machine
    Machine = getMachineObject(user_data[2])
    # clear windows
    clearWindowRegistry(["selectModelWindow", "selectMachineWindow"])
    # create a SelectMapping window
    SelectConfigWindow = dpg.window(tag = "selectConfigWindow", pos = [900, 18], width = 500, height = 702, 
        no_move = True, no_close = True, no_collapse = True, no_title_bar = True, no_resize = True)
    # add items to the new window
    with SelectConfigWindow:
        # mapping listbox (hidden at first)
        list_items = []
        # get the machine file
        machine_file = openMachineConfiguration(Machine['name'])
        # find the machine's mappings
        for curr_mapping in machine_file['mappings']:
            # add the mapping to the list
            list_items.append(curr_mapping['id'])
        # if list is empty
        if not list_items:
            # just add "None"; skip the list
            dpg.add_text("No Machine Configurations", pos = [25, 57])
        # there are configurations to list
        else:
            # mapping selection
            dpg.add_text("Select a Mapping Configuration:", pos = [25, 32])
            # sort the mapping configuration list
            list_items = sorted(list_items, reverse = False)
            # mapping configuration listbox
            ConfigListbox = dpg.add_listbox(items = list_items, width = 300, pos = [25, 57], 
                num_items = 20, default_value = list_items[0])
            # add a select button
            SelectConfigButton = dpg.add_button(label = "Select this Mapping Configuration", 
                width = 300, pos = [25, 600])
            # if the continue code is to edit config
            if continueCode == "editConfig":
                # set the callback to edit config
                dpg.set_item_callback(SelectConfigButton, editConfig)
            # if the continue code is to remove config
            elif continueCode == "removeConfig":
                # set the callback to remove config
                dpg.set_item_callback(SelectConfigButton, removeConfig)
            # otherwise set to view config
            else:
                # set the callback to view config
                dpg.set_item_callback(SelectConfigButton, viewConfig)
            # set the button's user data
            dpg.set_item_user_data(SelectConfigButton, [continueCode, Model, Machine, ConfigListbox])
            

## MACHINE UI CALLBACKS
#__________________________________________________________________________________________________
# makes an edit to a machine in the KIM Interface configuration file
def commitMachineEdits(sender, app_data, user_data):
    """commitMachineEdits(user_data = [continueCode, Model, Machine, 
        new_name, prior_name, checks, inputs])
    
    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning the edited Machine.
    Machine: Dict:Machine; Machine Object being edited.
    new_name: DPG item; Input box holding the edited name of the Machine.
    prior_name: str; Name of the Machine before edits.
    checks: [DPG Check Boxes]; list of edited selected Machine measurements.
    inputs: [DPG Input Boxes]; list of edited selected Machine measurements maps.

    Takes a machine with edits and overwrites that machine in the config."""
    # get continue code
    continueCode = user_data[0]
    # get Model
    Model = user_data[1]
    # get Machine
    Machine = getMachineObject(user_data[2])
    # get the new machine name
    new_name = user_data[3]
    # get the name prior to editing
    prior_name = user_data[4]
    # get the edited machine information
    checks = user_data[5]
    inputs = user_data[6]
    # validate the passed machine information
    validation = validateEditMachineInput(Model, Machine, new_name, prior_name, checks, inputs)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the edited Machine object
        showWarningPopup(validation[1]['error'])
    # edits were valid
    else:
        # update the machine
        EditedMachine = validation[1]
        # reflect edits to measurement fields in Mapping Configurations
        File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
            Model['model_name'], Machine['name'] + ".json"), 'r')
        # read the file contents
        machine_file = File.read()
        # close the machine file
        File.close()
        # format the Machine file as JSON
        machine_file = loads(machine_file)
        # create a list to hold the removed measurements
        removed_meas = []
        # calculate removed measurements
        for meas in Machine['measurements']:
            # if this measurement isnt in the EditedMachine's list
            if meas not in EditedMachine['measurements']:
                # add the measurement to the removed list
                removed_meas.append(meas)
        # for each Config in the Machine file
        for Config in machine_file['mappings']:
            # create a list to store removed mapping items
            removed_items = []
            # for each mapped Item in the Configuration
            for i in range(len(Config['configuration'])):
                # if the current item in the mapped item list was removed
                if Config['configuration'][i]['item'] in removed_meas:
                    # add this index value to the removed list
                    removed_items.append(i)
            # reverse the list of removed indexes (remove from right to left (large to small index))
            removed_items.reverse()
            # for each index needing removed
            for index in removed_items:
                # remove that item by index
                Config['configuration'].pop(index)
        # update the machine's name
        machine_file['machine'] = EditedMachine['name']
        # timestamp the file
        machine_file = timestamp(machine_file, str(EditedMachine['name']) + ".json", 
            "Edit Machine: " + str(EditedMachine['name']))
        # format the new Machine file text as JSON
        machine_file = dumps(machine_file, indent = 4)
        # overwrite the Machine file
        File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
            Model['model_name'], Machine['name'] + ".json"), 'w')
        # write the new JSON to the file
        File.write(machine_file)
        # close the machine file
        File.close()
        # get the KIM Interface config file 
        Interface_Config_File = openConfigFile()
        # get the index of the machine in the machine list
        machines = getMachines()
        # get the index from the list
        machine_index = machines.index(Machine)
        # update that machine's measurement list
        Interface_Config_File['machines'][machine_index] = EditedMachine
        # get a list of Models
        models = getModels()
        # find the Model's index in the Model list
        model_index = models.index(Model)
        # find the Machine index in the Model's Machine list
        machine_index = Model['model_machines'].index(Machine['name'])
        # update the Machine's name in the Model's Machines list
        Model['model_machines'][machine_index] = EditedMachine['name']
        # update the Model in the config file
        Interface_Config_File['models'][model_index] = Model
        # overwrite the KIM Interface config file
        overwriteConfigFile(Interface_Config_File, "Edit Machine: " + str(EditedMachine['name']))
        # set the machine file directory with the old Machine name
        old_machine_file = os.path.join(
            sys_env_dir, "config", "mapping configurations", 
            Model['model_name'], Machine['name'] + ".json")
        # set the machine file directory with the new Machine name
        new_machine_file = os.path.join(
            sys_env_dir, "config", "mapping configurations", 
            Model['model_name'], EditedMachine['name'] + ".json")
        # update the Model's folder in config folder
        os.rename(old_machine_file, new_machine_file)
        # update the model and machine objects in runtime 
        Model = getModelObject(Model['model_name'])
        Machine = getMachineObject(EditedMachine['name'])
        # clear the Popup alias
        clearWindow("confirmPopup")
        # create the confirmation popup
        Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = True,
            width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
            pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
            modal = True)
        # add items to the popup
        with Popup:
            # add a success message
            dpg.add_text("Success:", color = [150, 150, 255])
            dpg.add_text("Your edits to " + Machine['name'] + "\nhave been saved.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewMachine, user_data = ["viewMachine", Model, Machine])

# adds a new machine to the KIM Interface configuration file
def commitMachineAdd(sender, app_data, user_data):
    """commitMachineAdd(user_data = continueCode, Model, machine_name, measurements_list)
    
    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning the added Machine.
    machine_name: DPG item; Input box holding the name of the new Machine.
    measurements_list: [DPG Input Boxes]; list of entered Machine measurements.

    Adds a new machine to a model in the KIM Interface config."""
    # get continue code
    continueCode = user_data[0]
    # get Model
    Model = user_data[1]
    # get new machine name
    machine_name = dpg.get_value(user_data[2])
    # get the measurements for this machine
    measurements_list = user_data[3]
    # validate the new Machine input
    validation = validateAddMachineInput(Model, machine_name, measurements_list)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new Config object
        showWarningPopup(validation[1]['error'])
    # valid Config input
    else:
        # format the new machine information
        NewMachine = validation[1]
        # open KIM Interface config
        Interface_Config_File = openConfigFile()
        # add the new machine to the machines list
        Interface_Config_File['machines'].append(NewMachine)
        # get the index of the machine's model in KIM Interface config
        model_index = Interface_Config_File['models'].index(Model)
        # add the new machine to its model
        Interface_Config_File['models'][model_index]['model_machines'].append(NewMachine['name'])
        # overwrite the KIM Interface config file
        overwriteConfigFile(Interface_Config_File, "Add Machine: " + str(NewMachine['name']))
        # create a default Config for the new machine (ID# 1)
        # convert machine information to JSON
        machine_config = {"timestamp":str(str(datetime.now()) + " | " + str(user)), "machine":NewMachine["name"], 
            "mappings":[{"id":"1", "configuration":[]}]}
        # add each model base info to the default mapping
        for info in Model['model_base_information']:
            # add the info as a mapping item
            machine_config["mappings"][0]['configuration'].append(
                {"item":info, "sheet":1, "cluster":1, "type":"string", "value":""})
        # add each machine measurement to the default mapping
        for meas in NewMachine['measurements']:
            # add the measurement as a mapping item
            machine_config["mappings"][0]['configuration'].append(
                {"item":meas, "sheet":1, "cluster":1, "type":"string", "value":""})
        # convert the machine_config Dict to JSON
        machine_config = dumps(machine_config, indent = 4)
        # add file to store machine configurations in mapping configurations folder
        File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
            Model['model_name'], NewMachine['name'] + ".json"), 'x')
        # write the machine info into the file
        File.write(machine_config)
        # close the file
        File.close()
        # update the model and machine objects in runtime 
        Model = getModelObject(Model['model_name'])
        Machine = getMachineObject(NewMachine['name'])
        # clear the Popup alias
        clearWindow("confirmPopup")
        # create the confirmation popup
        Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = True,
            width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
            pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
            modal = True)
        # add items to the popup
        with Popup:
            # add a success message
            dpg.add_text("Success:", color = [150, 150, 255])
            dpg.add_text("Your new machine " + Machine['name'] 
                + "\nfor " + Model['model_name'] + " has been added.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewMachine, user_data = ["viewMachine", Model, Machine])

# removes a machine from the KIM Interface configuration file
def commitMachineRemove(sender, app_data, user_data):
    """commitMachineRemove(user_data = continueCode, Model, Machine)
    
    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning the removed Machine.
    Machine: Dict:Machine; Machine being removed.

    Removes a machine from a model in the KIM Interface config."""
    # get continue code
    continueCode = user_data[0]
    # get Model
    Model = user_data[1]
    # get Machine
    Machine = user_data[2]
    # get the KIM Interface config file
    Interface_Config_File = openConfigFile()
    # remove the machine from the KIM Interface config['machines'] list
    Interface_Config_File['machines'].remove(Machine)
    # update the model in the KIM Interface config file
    # get the index of the model in the model list
    model_index = Interface_Config_File['models'].index(Model)
    # update that model's machine list
    Interface_Config_File['models'][model_index]['model_machines'].remove(Machine['name'])
    # overwrite the KIM Interface config file
    overwriteConfigFile(Interface_Config_File, "Remove Machine: " + str(Machine['name']))
    # remove machine file in model folder in mapping configurations
    os.remove(os.path.join(sys_env_dir, "config", "mapping configurations", 
        Model['model_name'], Machine['name'] + ".json"))
    # update the model object in runtime 
    Model = getModelObject(Model['model_name'])
    # clear the remove popup
    clearWindow("removeMachine")
    # clear the Popup alias
    clearWindow("confirmPopup")
    # create the confirmation popup
    Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = False,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        modal = True)
    # add items to the popup
    with Popup:
        # add a success message
        dpg.add_text("Success:", color = [150, 150, 255])
        dpg.add_text("Your machine " + Machine['name'] 
            + "\nhas been removed.")
        # add an Okay button
        dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
            callback = selectModel, user_data = ["viewMachine"])

# updates the edit machine measurements subwindow
def editMachineSubwindow(sender, app_data, user_data):
    """editMachineSubwindow(user_data = [continueCode, Model, Machine, checks, inputs])

    Subwindow segment of the EditMachineWindow

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning the added Machine.
    Machine: Dict:Machine; Machine being edited.
    checks: [DPG Check Boxes]; list of edited selected Machine measurements.
    inputs: [DPG Input Boxes]; list of edited selected Machine measurements maps.
    
    Allows for dynamic addition of Model Base Information
    """
    # get continue code
    continueCode = user_data[0]
    # get the Model owning the edited Machine
    Model = user_data[1]
    # get the selected Machine
    Machine = user_data[2]
    # get the current checks list
    checks = user_data[3]
    # get the current inputs list
    inputs = user_data[4]
    # clear windows
    clearWindowRegistry("editMachineWindow")
    # create a new subwindow to show the machine's measurements
    EditMachineSubwindow = dpg.window(tag = "editMachineSubwindow", pos = [0, 125], 
        width = dpg.get_viewport_width(), height = 600, no_move = True, no_close = True, 
        no_collapse = True, no_title_bar = True, no_background = True, show = True)
    # add items to the window
    with EditMachineSubwindow:
        # add a measurement list
        dpg.add_text("Machine Measurements:", pos = [75, 0])
        # set a positional offset
        pos_offset = 1
        # add an add measurement field button
        dpg.add_button(tag = "addMeasurementButton", label = "+ New Measurement Field", 
            pos = [175, 50], width = 225, callback = addMachineMeasurementField)
        # for each field in the measurement list
        for meas in Machine['measurements']:
            # add a text item for that field
            dpg.add_text("Edit Spec:", pos = [75, 0 + (pos_offset * 25)])
            # add a checkbox for this spec
            MeasurementCheck = dpg.add_checkbox(pos = [150, 0 + (pos_offset * 25)], default_value = True)
            # add an input for editing the spec
            MeasurementInput = dpg.add_input_text(default_value = meas, 
                pos = [200, 0 + (pos_offset * 25)], width = 200, hint = "Empty = Clear Measurement...")
            # add the check to the list
            checks.append(MeasurementCheck)
            # add the input to the list
            inputs.append(MeasurementInput)
            # increment positional offset
            pos_offset += 1
            # update the add measurement button position
            dpg.set_item_pos("addMeasurementButton", [175, 25 + (pos_offset * 25)])
        # set the add measurement button user_data
        dpg.set_item_user_data("addMeasurementButton", [Model, Machine, checks, inputs])
        # add informational text
        dpg.add_text("! - De-selecting an existing Measurement Field will\n" 
                    + "    remove it from the Machine's list and ALL the Machine's\n"
                    + "    configurations. This should be avoided, if possible.", 
                    pos = [400, 25], color = [150, 150, 255])
        # add a Finish Editing button
        dpg.add_button(label = "Finish Editing Machine...", width = 270, pos = [75, 500],
            callback = commitMachineEdits, user_data = 
            ["editMachine", Model, Machine, "machineNameInput", Machine['name'], checks, inputs])

def updateMachineMidEdit(sender, app_data, user_data):
    """updateMachineMidEdit(user_data = [Model, Machine, new_spec])
    
    Model: Dict:Model; the Model owning the Machine being edited.
    Machine: Dict:Machine; the Machine being edited.
    new_spec: DPG Inputbox; input box containing the title of the new specification.

    Adds a new specification to a machine's list mid-edit and refreshes the edit window.
    """
    # get the model owning the machine
    Model = user_data[0]
    # get the Machine
    Machine = user_data[1]
    # get the new measurement specification
    new_spec = dpg.get_value(user_data[2])
    # get the KIM Interface config file
    Interface_Config_File = openConfigFile()
    # find the Machine in KIM Interface config
    machine_index = Interface_Config_File['machines'].index(Machine)
    # add a new measurement field to the Machine
    Machine['measurements'].append(new_spec)
    # update the Machine in the KIM Interface config file
    Interface_Config_File['machines'][machine_index] = Machine
    # overwrite the KIM Interface config file
    overwriteConfigFile(Interface_Config_File, "Edit Machine: " + str(Machine['name']))
    # update the editMachineSubwindow
    editMachineSubwindow(sender = "", app_data = "", 
        user_data = ["editMachine", Model, Machine, [], []])
    # delete the popup
    deleteItem(sender = "", app_data = "", user_data = ["fieldValuePopup"])

# adds a new measurement to the edited machine
def addMachineMeasurementField(sender, app_data, user_data):
    """addMachineMeasurementField(user_data = [Model, Machine, checks, inputs])
    
    Model: Dict:Model; the Model owning the Machine being edited.
    Machine: Dict:Machine; the Machine being edited.
    checks: [DPG Check Boxes]; list of edited selected Machine measurements.
    inputs: [DPG Input Boxes]; list of edited selected Machine measurements maps.

    Prompts the user to enter a new Measurement Specification.
    """
    # get Model
    Model = user_data[0]
    # get Machine
    Machine = user_data[1]
    # get checks list
    checks = user_data[2]
    # get inputs list
    inputs = user_data[3]
    # create a field value input popup
    Popup = dpg.window(tag = "fieldValuePopup", popup = True, no_open_over_existing_popup = False,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        modal = True)
    # add items to the popup
    with Popup:
        # add a label
        dpg.add_text("Please enter the new measurement specification:")
        # add an input box
        NewFieldInput = dpg.add_input_text(hint = "Specification...", width = 300)
        # add an add field button
        dpg.add_button(label = "Add New Measurement", pos = [5, 100], 
            callback = updateMachineMidEdit, user_data = [Model, Machine, NewFieldInput])
        # add a cancel button
        dpg.add_button(label = "Cancel", pos = [165, 100], 
            callback = deleteItem, user_data = ["fieldValuePopup"])

# add machine flow
def addMachine(sender, app_data, user_data):
    """addMachine(user_data = continueCode, Model)
    
    SelectModelWindow -> AddMachineWindow

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning the added Machine.
    
    Invokes the UI flow from the SelectModelWindow to the AddMachineWindow.
    Invoked by the menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model
    Model = getModelObject(user_data[1])
    # clear windows
    clearWindowRegistry()
    # create the AddMachineWindow
    AddMachineWindow = dpg.window(tag = "addMachineWindow", pos = [0, 0], width = 1280, height = 720,
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the window
    with AddMachineWindow:
        # make the new window the primary window
        dpg.set_primary_window("addMachineWindow", True)
        # back button
        dpg.add_button(label = "<- ... / Select a Model / Add a new Machine...", pos = [10, 25],
            callback = selectModel, user_data = ["addMachine"])
        # add model text label
        dpg.add_text("Add a new Machine for the KIM Interface to use.\n"
            + "-  Each Machine has a set of measurements;\n"
            + "   these measurements are used to create mappings.\n"
            + "-  Machine names must be unique.", pos = [75, 100])
        # enter machine name label
        dpg.add_text("Enter the new machine name:", pos = [75, 200])
        # machine name entry box
        MachineNameEntry = dpg.add_input_text(width = 200, pos = [75, 225], hint = "Machine name...")
        # add measurements setting panel
        # add measurements panel label
        dpg.add_text("Enter machine measurements (measurement column headers):", pos = [400, 200])
        # add 15 measurement field entries
        # set positional offset
        pos_offset = 1
        # create a list to hold the measurement entries
        measurement_entries = []
        for i in range(15):
            # add a field name input box
            MeasurementsEntry = dpg.add_input_text(width = 300, pos = [400, 200 + (pos_offset * 25)], 
                hint = "Measurement Specs...")
            # add the input box to the list
            measurement_entries.append(MeasurementsEntry)
            # increment positional offset
            pos_offset += 1
        # add existing model machines label
        dpg.add_text("Existing Model Machines (names):", pos = [1000, 200])
        # add existing machines list text
        # set positional offset
        pos_offset = 1
        # display the Model's existing machines
        for machine in Model['model_machines']:
            # add this name to the window
            dpg.add_text(machine, pos = [1000, 200 + (pos_offset * 25)])
            # increment the positional offset
            pos_offset += 1
        # add the Add New Machine button
        dpg.add_button(label = "Add new Machine...", width = 270, pos = [50, 600],
            callback = commitMachineAdd, user_data = ["addMachine", Model, MachineNameEntry, measurement_entries])

# remove machine flow
def removeMachine(sender, app_data, user_data):
    """viewMachine(user_data = continueCode, Model, Machine)
    
    ViewMachineWindow -> RemoveMachineWindow
    
    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning the removed Machine.
    Machine: Dict:Machine; Machine Object being removed.
    
    Invokes the UI flow from the ViewMachineWindow to the RemoveMachineWindow.
    Invoked by the selection of "Remove Machine" in ViewMachineWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get Model
    Model = user_data[1]
    # get Machine
    Machine = getMachineObject(user_data[2])
    # create a popup window
    RemoveMachinePopup = dpg.window(tag = "removeMachine", popup = True, no_open_over_existing_popup = True,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        show = True, modal = True)
    # add items to the popup
    with RemoveMachinePopup:
        # add a warning
        dpg.add_text("Warning:", color = [255, 0, 50])
        dpg.add_text("Removing a Machine from the Interface is 100" + '%' + "\n" 
            + "irreversible! Only perform this action if you\n"
            + "are completely sure that it is out-of-use.")
        # add a Cancel button
        dpg.add_button(label = "Cancel", pos = [10, 100], width = 180, height = 25,
            callback = deleteItem, user_data = ["removeMachine"])
        # add a Delete button
        dpg.add_button(label = "Delete", pos = [200, 100], width = 180, height = 25,
            callback = commitMachineRemove, user_data = ["removeMachine", Model, Machine])

# edit machine flow
def editMachine(sender, app_data, user_data):
    """editMachine(user_data = continueCode, Model, Machine)

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning the edited Machine.
    Machine: Dict:Machine; Machine Object being edited.

    ViewMachineWindow -> EditMachineWindow

    Invokes the UI flow from the ViewMachineWindow to the EditMachineWindow.
    Invoked by the selection of "Edit Machine" in ViewMachineWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get Model
    Model = user_data[1]
    # get Machine
    Machine = getMachineObject(user_data[2])
    # clear windows
    clearWindowRegistry()
    # enable the EditMachineWindow
    EditMachineWindow = dpg.window(tag = "editMachineWindow", pos = [0, 0], width = 1280, height = 720,
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the EditMachineWindow
    with EditMachineWindow:
        # make the new window the primary window
        dpg.set_primary_window("editMachineWindow", True)
        # back button
        dpg.add_button(label = "<- ... / View Machine / Edit Machine...",
            callback = selectModel, user_data = ["editMachine"], pos = [10, 25])
        # add a machine name label
        dpg.add_text("Machine Name:", pos = [75, 100])
        # add an input for the machine name
        dpg.add_input_text(tag = "machineNameInput", pos = [175, 100], 
            width = 200, default_value = Machine['name'])
        # open the editMachineSubwindow
        editMachineSubwindow(sender = "", app_data = "", 
            user_data = ["editMachine", Model, Machine, [], []])

# view machine flow
def viewMachine(sender, app_data, user_data):
    """viewMachine(user_data = continueCode, Model, Machine)

    SelectMachineWindow -> ViewMachineWindow
    
    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object owning the viewed Machine.
    Machine: Dict:Machine; Machine Object being viewed.
    
    Invokes the UI flow from the SelectMachineWindow to the ViewMachineWindow.
    Invoked by the selection of a machine or the menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get Model
    Model = user_data[1]
    # get Machine
    Machine = getMachineObject(user_data[2])
    # clear windows
    clearWindowRegistry()
    # eneable the ViewMachineWindow
    ViewMachineWindow = dpg.window(tag = "viewMachineWindow", pos = [0, 0], width = 1280, height = 720,
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the ViewMachineWindow
    with ViewMachineWindow:
        # make the new window the primary window
        dpg.set_primary_window("viewMachineWindow", True)
        # back button
        dpg.add_button(label = "<- ... / Select a Machine / View Machine...",
            callback = selectModel, user_data = ["viewMachine"], pos = [10, 25])
        # add a machine name label
        dpg.add_text("Machine name: " + Machine['name'], pos = [75, 100])
        # add a measurement list
        dpg.add_text("Machine Measurements:", pos = [75, 200])
        # set a positional offset
        pos_offset = 1
        # for each measurement field in the list
        for meas in Machine['measurements']:
            # add a text item for that field
            dpg.add_text("-   " + str(meas), pos = [80, 200 + (pos_offset * 25)])
            # increment positional offset
            pos_offset += 1
        # add Machine Actions side panel
        dpg.add_text("Machine Actions:", pos = [800, 200])
        # add action buttons
        dpg.add_button(label = "Edit this Machine                   ->", pos = [800, 225],
            callback = editMachine, user_data = ["editMachine", Model, Machine])
        dpg.add_button(label = "Remove this Machine                 !!", pos = [800, 250],
            callback = removeMachine, user_data = ["removeMachine", Model, Machine])
        dpg.add_button(label = "Add a Configuration to this Machine ->", pos = [800, 275],
            callback = addConfig, user_data = ["addConfig", Model, Machine])

# select machine flow
def selectMachine(sender, app_data, user_data):
    """selectMachine(user_data = continueCode, Model)

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model Object being selected from.

    StartupWindow -> SelectMachineWindow
    
    Invokes the UI flow from the StartupWindow to the SelectMachineWindow.
    Invoked by the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get Model
    Model = getModelObject(user_data[1])
    # clear windows
    clearWindowRegistry(["selectModelWindow"])
    # create a SelectMachine window
    SelectMachineWindow = dpg.window(tag = "selectMachineWindow", pos = [400, 18], width = 500, height = 702, 
        no_move = True, no_close = True, no_collapse = True, no_title_bar = True, no_resize = True)
    # add items to the new window
    with SelectMachineWindow:
        # machine listbox (hidden at first)
        list_items = []
        # extract model machine names
        for machine in Model['model_machines']:
            # add it to the list
            list_items.append(machine)
        # if list is empty
        if not list_items:
            # just add "None"; skip the list
            dpg.add_text("No Model Machines", pos = [25, 57])
        # there are machines to list
        else:
            # add the machine selection label
            dpg.add_text("Select a Machine:", pos = [5, 32])
            # sort the mapping configuration list
            list_items = sorted(list_items, reverse = False)
            # create the machine selection listbox
            MachineListbox = dpg.add_listbox(items = list_items, width = 450, 
                pos = [25, 57], num_items = 20, default_value = list_items[0])
            # if the continue code indicates SelectConfigWindow
            if continueCode in ["viewConfig","editConfig","removeConfig"]:
                # set the machine list callback
                dpg.set_item_callback(MachineListbox, selectConfig)
                # set the list's user data
                dpg.set_item_user_data(MachineListbox, [continueCode, Model, MachineListbox])
            # else the continue code was not set to continue to SelectConfigWindow
            else:
                # add a select button
                SelectMachineButton = dpg.add_button(label = "Select this Machine", width = 270, pos = [50, 600])
                # if the continue code is "addConfig"
                if continueCode == "addConfig":
                    # set the callback to add config
                    dpg.set_item_callback(SelectMachineButton, addConfig)
                # if the continue code is edit machine
                elif continueCode == "editMachine":
                    # set the callback to edit machine
                    dpg.set_item_callback(SelectMachineButton, editMachine)
                # if the continue code is edit machine
                elif continueCode == "removeMachine":
                    # set the callback to remove machine
                    dpg.set_item_callback(SelectMachineButton, removeMachine)
                # otherwise set to move to view machine
                else:
                    # set the callback to view machine
                    dpg.set_item_callback(SelectMachineButton, viewMachine)
                # set the button's user data
                dpg.set_item_user_data(SelectMachineButton, [continueCode, Model, MachineListbox])          


## MODEL UI CALLBACKS
#__________________________________________________________________________________________________
# makes an edit to a model in the KIM Interface config file
def commitModelEdits(sender, app_data, user_data):
    """
    commitModelEdits(user_data = continueCode, Model, new_name, prior_name, 
        base_info_checks, base_info_inputs)

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model being edited.
    new_name: DPG Input Box; DPG Item holding the edited Model name.
    prior_name: str; the Model name before edits.
    base_info_checks: [DPG Checkboxes]; Checkboxes indicating the selected base
        information to include after edits.
    base_info_inputs: [DPG Input boxes]; Input boxes holding the edited base information
        headers.

    Takes a model with edits and overwrites that model in the KIM Interface config."""
    # get continue code
    continueCode = user_data[0]
    # get Model
    Model = getModelObject(user_data[1])
    # get the edited model name
    new_name = dpg.get_value(user_data[2])
    # get the model name prior to edits
    prior_name = user_data[3]
    # get the selected model information fields
    checks = user_data[4]
    # get the base information header inputs
    inputs = user_data[5]
    # validate the edited Model input
    validation = validateEditModelInput(Model, new_name, prior_name, checks, inputs)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new Model object
        showWarningPopup(validation[1]['error'])
    # valid Model input
    else:
        # input was valid, continue
        EditedModel = validation[1]
        # set a temp path to the old model name folder
        temp_path = os.path.join(sys_env_dir, "config", "mapping configurations", Model['model_name'])
        # reflect edits to base info fields in Mapping Configurations
        for root, dirs, files in os.walk(top = temp_path, topdown = False):
            # for every Machine configuration file
            for file in files:
                # open the Machine file
                File = open(os.path.join(root, file), 'r')
                # read the file contents
                machine_file = File.read()
                # close the machine file
                File.close()
                # format the Machine file as JSON
                machine_file = loads(machine_file)
                # create a list to hold the removed base information
                removed_base = []
                # calculate removed base info
                for base in Model['model_base_information']:
                    # if this base info isnt in the EditedModel's list
                    if base not in EditedModel['model_base_information']:
                        # add the base infor to the removed list
                        removed_base.append(base)
                # for each Config in the Machine file
                for Config in machine_file['mappings']:
                    # create a list to store removed mapping items
                    removed_items = []
                    # for each mapped Item in the Configuration
                    for i in range(len(Config['configuration'])):
                        # if the current item in the mapped item list was removed
                        if Config['configuration'][i]['item'] in removed_base:
                            # add this index value to the removed list
                            removed_items.append(i)
                    # reverse the list of removed indexes (remove from right to left (large to small index))
                    removed_items.reverse()
                    # for each index needing removed
                    for index in removed_items:
                        # remove that item by index
                        Config['configuration'].pop(index)
                # timestamp the file
                machine_file = timestamp(machine_file, str(machine_file['name']) + ".json", 
                    "Edit Machine: " + str(machine_file['name']))
                # format the new Machine file text as JSON
                machine_file = dumps(machine_file, indent = 4)
                # overwrite the Machine file
                File = open(os.path.join(root, file), 'w')
                # write the new JSON to the file
                File.write(machine_file)
                # close the machine file
                File.close()
        # open the KIM Interface config file
        Interface_Config_File = openConfigFile()
        # hold the edited model's index
        model_index = Interface_Config_File['models'].index(Model)
        # update machines to reflect the new model name
        # first, update the machine names in the KIM Interface config file
        index = 0
        for machine in Interface_Config_File['machines']:
            # do the machine names match
            if machine['name'] in Model['model_machines']:
                # update the name
                Interface_Config_File['machines'][index]['name'] = EditedModel['model_name'] + machine['name'][3:]
            index += 1
        # then update the machines in the model itself
        index = 0
        for machine in EditedModel['model_machines']:
            # create the new machine name
            new_machine_name = EditedModel['model_name'] + machine[3:]
            # update the machine name in the model itself
            EditedModel['model_machines'][index] = new_machine_name
            index == 1
        # update the edited model in KIM Interface config
        Interface_Config_File['models'][model_index] = EditedModel
        # overwrite the KIM Interface config file
        overwriteConfigFile(Interface_Config_File, "Edit Model: " + str(EditedModel['model_name']))
        # set the directory with the old Model name
        old_model_folder = os.path.join(
            sys_env_dir, "config", "mapping configurations", Model['model_name'])
        # set the directory with the new Model name
        new_model_folder = os.path.join(
            sys_env_dir, "config", "mapping configurations", EditedModel['model_name'])
        # update the Model's folder in config folder
        os.rename(old_model_folder, new_model_folder)
        # finally update all of the machine config files in the Model's folder
        for root, dirs, files in os.walk(top = new_model_folder, topdown = False):
            # rename the files
            for file in files:
                # rename file
                os.rename(os.path.join(root, file),
                    os.path.join(sys_env_dir, "config", "mapping configurations", 
                    EditedModel['model_name'], EditedModel['model_name'] + file[3:]))
        # update the Model object in runtime memory
        Model = getModelObject(EditedModel['model_name'])
        # clear the Popup alias
        clearWindow("confirmPopup")
        # create the confirmation popup
        Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = True,
            width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
            pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
            modal = True)
        # add items to the popup
        with Popup:
            # add a success message
            dpg.add_text("Success:", color = [150, 150, 255])
            dpg.add_text("Your edits to " + Model['model_name'] + "\nhave been saved.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewModel, user_data = ["viewModel", Model])

# adds a new model to the KIM Interface config
def commitModelAdd(sender, app_data, user_data):
    """
    commitModelAdd(user_data = continueCode, model_name, model_base_info)

    continueCode: str; continue code correspdonding to the action being performed.
    model_name: DPG Input Box; DPG Item holding the new Model name.
    model_base_info: [DPG Input boxes]; Input boxes holding the new model 
        base information headers.

    Adds a new model in the KIM Interface config."""
    # get continue code
    continueCode = user_data[0]
    # get model name
    model_name = dpg.get_value(user_data[1])
    # get the base information list
    model_base_info = user_data[2]
    # validate the new Model input
    validation = validateAddModelInput(model_name, model_base_info)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new Model object
        showWarningPopup(validation[1]['error'])
    # valid Model input
    else:
        # input was valid, continue
        NewModel = validation[1]
        # add the new model to the KIM Interface config file (open KIM Interface config)
        Interface_Config_File = openConfigFile()
        # add the new model to the models list
        Interface_Config_File['models'].append(NewModel)
        # overwrite the KIM Interface config file
        overwriteConfigFile(Interface_Config_File, "Add Model: " + str(NewModel['model_name']))
        # add folder in mapping configurations to hold this model's machine config files
        os.mkdir(os.path.join(sys_env_dir, "config", "mapping configurations", NewModel['model_name']))
        # update model object in runtime memory
        Model = getModelObject(NewModel['model_name'])
        # clear the Popup alias
        clearWindow("confirmPopup")
        # create the confirmation popup
        Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = True,
            width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
            pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
            modal = True)
        # add items to the popup
        with Popup:
            # add a success message
            dpg.add_text("Success:", color = [150, 150, 255])
            dpg.add_text("Your new model " + Model['model_name'] 
                + "\nhas been added.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewModel, user_data = ["viewModel", Model])

# removes a model from the KIM Interface configuration file
def commitModelRemove(sender, app_data, user_data):
    """
    commitModelRemove(user_data = continueCode, Model)

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model being removed.

    Removes a model in the KIM Interface config."""
    # get continue code
    continueCode = user_data[0]
    # get the removed model
    Model = user_data[1]
    # get the KIM Interface config file
    Interface_Config_File = openConfigFile()
    # remove that model from the list
    Interface_Config_File['models'].remove(Model)
    # remove the model's machines from the KIM Interface config
    for machine in Interface_Config_File['machines']:
        # for each model machine
        for model_machine in Model['model_machines']:
            # if the machine is in the model's list
            if machine['name'] == model_machine:
                # remove that machine from the KIM Interface config list
                Interface_Config_File['machines'].remove(machine)
    # overwrite the KIM Interface config file
    overwriteConfigFile(Interface_Config_File, "Remove Model: " + str(Model['model_name']))
    # get all the machine files in the model folder
    for root, dirs, files in os.walk(
        top = os.path.join(sys_env_dir, "config", "mapping configurations", Model['model_name']),
        topdown = False):
        # remove each file
        for file in files:
            # remove file
            os.remove(os.path.join(root, file))
    # remove model folder in mapping configurations
    os.rmdir(os.path.join(sys_env_dir, "config", "mapping configurations", Model['model_name']))
    # clear the remove popup
    clearWindow("removeModel")
    # clear the Popup alias
    clearWindow("confirmPopup")
    # create the confirmation popup
    Popup = dpg.window(tag = "confirmPopup", popup = True, no_open_over_existing_popup = False,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        modal = True)
    # add items to the popup
    with Popup:
        # add a success message
        dpg.add_text("Success:", color = [150, 150, 255])
        dpg.add_text("Your model " + Model['model_name'] 
            + "\nhas been removed.")
        # add an Okay button
        dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
            callback = selectModel, user_data = ["viewModel"])

# update the edit model information subwindow
def editModelSubwindow(sender, app_data, user_data):
    """updateEditModelSubwindow(user_data = [continueCode, Model, checks, inputs])

    Subwindow segment of the EditModelWindow

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model being edited.
    checks: [DPG Check Boxes]; list of edited selected Model information headers.
    inputs: [DPG Input Boxes]; list of edited selected Model information header maps.

    Allows for dynamic addition of Model Base Information
    """
    # get continue code
    continueCode = user_data[0]
    # get the selected model
    Model = user_data[1]
    # get the current checks list
    checks = user_data[2]
    # get the current inputs list
    inputs = user_data[3]
    # clear windows
    clearWindowRegistry("editModelWindow")
    # create a new subwindow to show the model's base information
    EditModelSubwindow = dpg.window(tag = "editModelSubwindow", pos = [0, 125], 
        width = dpg.get_viewport_width(), height = 600, no_move = True, no_close = True, 
        no_collapse = True, no_title_bar = True, no_background = True, show = True)
    # add items to the window
    with EditModelSubwindow:
        # add a base information list
        dpg.add_text("Model Base Information:", pos = [75, 0])
        # create a list to hold the check boxes
        base_info_checks = []
        # create a list to hold the input boxes
        base_info_inputs = []
        # set a positional offset
        pos_offset = 1
        # add an add base information field button
        dpg.add_button(tag = "addBaseInfoButton", label = "+ New Base Information Field", 
            pos = [175, 50], width = 225, callback = addModelInfoField)
        # for each field in the base info list
        for info in Model['model_base_information']:
            # add a text item for that field
            dpg.add_text("Edit Header:", pos = [75, 25 + (pos_offset * 25)])
            # add a checkbox to include that field
            BaseInfoCheck = dpg.add_checkbox(default_value = True, 
                pos = [175, 25 + (pos_offset * 25)])
            # add an input to edit the header value
            BaseInfoInput = dpg.add_input_text(default_value = info, 
                pos = [200, 25 + (pos_offset * 25)], width = 200, hint = "Empty = Clear Base Info...")
            # add the checkbox to the list
            base_info_checks.append(BaseInfoCheck)
            # add the inputbox to the list
            base_info_inputs.append(BaseInfoInput)
            # increment positional offset
            pos_offset += 1
            # update the add information button position
            dpg.set_item_pos("addBaseInfoButton", [175, 25 + (pos_offset * 25)])
        # set the add model info button user_data
        dpg.set_item_user_data("addBaseInfoButton", [Model, checks, inputs])
        # add informational text
        dpg.add_text("! - De-selecting an existing Base Information Field will\n" 
                    + "    remove it from the Model's list and ALL the Model's\n"
                    + "    Machine lists. This should be avoided, if possible.", 
                    pos = [400, 50], color = [150, 150, 255])
        # add a Finish Editing button
        dpg.add_button(label = "Finish Editing Model...", width = 270, pos = [75, 500],
            callback = commitModelEdits, user_data = ["editModel", Model, "modelNameInput",
                Model['model_name'], base_info_checks, base_info_inputs])

def updateModelMidEdit(sender, app_data, user_data):
    """updateModelMidEdit(user_data = [Model, new_base_info])
    
    Model: Dict:Model; the Model being edited.
    new_base_info: DPG Inputbox; input box containing the title of the new base information.

    Adds a new base information field to a model's list mid-edit and refreshes the edit window.
    """
    # get the model
    Model = user_data[0]
    # get the new base information header
    new_base_info = dpg.get_value(user_data[1])
    # get the KIM Interface config file
    Interface_Config_File = openConfigFile()
    # find the model in KIM Interface config
    model_index = Interface_Config_File['models'].index(Model)
    # add a new information field to the model
    Model['model_base_information'].append(new_base_info)
    # update the model in the KIM Interface config file
    Interface_Config_File['models'][model_index] = Model
    # overwrite the KIM Interface config file
    overwriteConfigFile(Interface_Config_File, "Edit Model: " + str(Model['model_name']))
    # update the editModelSubwindow
    editModelSubwindow(sender = "", app_data = "", 
        user_data = ["editModel", Model, [], []])
    # delete the popup
    deleteItem(sender = "", app_data = "", user_data = ["fieldValuePopup"])

# adds a new model base info field
def addModelInfoField(sender, app_data, user_data):
    """addBaseInfoField(user_data = [Model checks, inputs])
    
    Model: Dict:Model; Model being edited.
    checks: [DPG Check Boxes]; list of edited selected Model information headers.
    inputs: [DPG Input Boxes]; list of edited selected Model information header maps.

    Adds a new blank base information field to the Model while editing
    """
    # get the model
    Model = user_data[0]
    # create a field value input popup
    Popup = dpg.window(tag = "fieldValuePopup", popup = True, no_open_over_existing_popup = False,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        modal = True)
    # add items to the popup
    with Popup:
        # add a label
        dpg.add_text("Please enter the new base information header:")
        # add an input box
        NewFieldInput = dpg.add_input_text(hint = "Base Information...", width = 300)
        # add an add field button
        dpg.add_button(label = "Add New Base Information", pos = [5, 100], 
            callback = updateModelMidEdit, user_data = [Model, NewFieldInput])
        # add a cancel button
        dpg.add_button(label = "Cancel", pos = [200, 100], 
            callback = deleteItem, user_data = ["fieldValuePopup"])

# add model flow
def addModel(sender, app_data, user_data):
    """addModel(user_data = continueCode)

    continueCode: str; continue code correspdonding to the action being performed.

    StartupWindow -> AddModelWindow

    Invokes the UI flow from the StartupWindow to the AddModelWindow.
    Invoked by the menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # clear windows
    clearWindowRegistry()
    # create the AddModelWindow
    AddModelWindow = dpg.window(tag = "addModelWindow", pos = [0, 0], width = 1280, height = 720,
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the window
    with AddModelWindow:
        # make the new window the primary window
        dpg.set_primary_window("addModelWindow", True)
        # back button
        dpg.add_button(label = "<- Main Menu / Add a new Model...", pos = [10, 25],
            callback = returnToStartup)
        # add model text label
        dpg.add_text("Add a new Model for the KIM Interface to use.\n"
            + "-  Each model has a set of base information;\n"
            + "   this base information is added to each machine.\n"
            + "-  Model names must be unique.", pos = [75, 100])
        # enter model name label
        dpg.add_text("Enter the new model name:", pos = [75, 200])
        # model name entry box
        ModelNameEntry = dpg.add_input_text(width = 200, pos = [75, 225], hint = "Model name...")
        # add base information setting panel
        # add base info panel label
        dpg.add_text("Enter model base information (non-measurement column headers):", pos = [400, 200])
        # add 15 base info field entries
        # set positional offset
        pos_offset = 1
        # create a list to hold the base information entries
        base_information_entries = []
        for i in range(15):
            # add a field name input box
            BaseInfoEntry = dpg.add_input_text(width = 300, pos = [400, 200 + (pos_offset * 25)], 
                hint = "Program name, Judgement, etc...")
            # add the input box to the list
            base_information_entries.append(BaseInfoEntry)
            # increment positional offset
            pos_offset += 1
        # add existing models label
        dpg.add_text("Existing Models (names):", pos = [1000, 200])
        # add existing models list text
        # set positional offset
        pos_offset = 1
        # pull models from KIM Interface config
        models = getModels()
        # for each model in KIM Interface config
        for curr_model in models:
            # add this name to the window
            dpg.add_text(str(curr_model['model_name']), pos = [1000, 200 + (pos_offset * 25)])
            # increment the positional offset
            pos_offset += 1
        # add the Add New Model button
        dpg.add_button(label = "Add new Model...", width = 270, pos = [50, 600],
            callback = commitModelAdd, user_data = ["addModel", ModelNameEntry, base_information_entries])

# remove model flow
def removeModel(sender, app_data, user_data):
    """removeModel(user_data = continueCode, Model)

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model being removed.

    ViewModelWindow -> RemoveModelWindow
    
    Invokes the UI flow from the ViewModelWindow to the RemoveModelWindow.
    Invoked by the selection of "Remove Model" in ViewModelWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get information from call
    Model = getModelObject(user_data[1])
    # create a popup window
    RemoveModelPopup = dpg.window(tag = "removeModel", popup = True, no_open_over_existing_popup = True,
        width = 400, height = 250, no_move = True, no_close = True, no_collapse = True, no_resize = True,
        pos = [(dpg.get_viewport_client_width() / 2) - 200, (dpg.get_viewport_client_height() / 2) - 125],
        show = True, modal = True)
    # add items to the popup
    with RemoveModelPopup:
        # add a warning
        dpg.add_text("Warning:", color = [255, 0, 50])
        dpg.add_text("Removing a Model from the Interface is 100" + '%' + "\n" 
            + "irreversible! Only perform this action if you\n"
            + "are completely sure that it is out-of-use.")
        # add a Cancel button
        dpg.add_button(label = "Cancel", pos = [10, 100], width = 180, height = 25,
            callback = deleteItem, user_data = ["removeModel"])
        # add a Delete button
        dpg.add_button(label = "Delete", pos = [200, 100], width = 180, height = 25,
            callback = commitModelRemove, user_data = ["removeModel", Model])

# edit model flow
def editModel(sender, app_data, user_data):
    """editModel(user_data = continueCode, Model)

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model being edited.
    
    ViewModelWindow -> EditModelWindow

    Invokes the UI flow from the ViewModelWindow to the EditModelWindow.
    Invoked by the selection of "Edit Model" in ViewModelWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the selected model
    Model = getModelObject(user_data[1])
    # clear windows
    clearWindowRegistry()
    # eneable the EditModelWindow
    EditModelWindow = dpg.window(tag = "editModelWindow", pos = [0, 0], width = 1280, height = 720,
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the EditModelWindow
    with EditModelWindow:
        # make the new window the primary window
        dpg.set_primary_window("editModelWindow", True)
        # back button
        dpg.add_button(label = "<- ... / View Model / Edit Model...",
            callback = selectModel, user_data = ["editModel"], pos = [10, 25])
        # add a model name label
        dpg.add_text("Model Name:", pos = [75, 100])
        # add an input to edit the model name
        dpg.add_input_text(tag = "modelNameInput", pos = [160, 100], width = 200, 
            default_value = Model['model_name'])
    # open the subwindow
    editModelSubwindow(sender, app_data, user_data = [continueCode, Model, [], []])

# view model flow
def viewModel(sender, app_data, user_data):
    """viewModel(user_data = continueCode, Model)

    continueCode: str; continue code correspdonding to the action being performed.
    Model: Dict:Model; Model being viewed.

    SelectModelWindow -> ViewModelWindow
    
    Invokes the UI flow from the SelectModelWindow to the ViewModelWindow.
    Invoked by the selection of a model or the menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get info from user data
    Model = getModelObject(user_data[1])
    # clear windows
    clearWindowRegistry()
    # eneable the ViewModelWindow
    ViewModelWindow = dpg.window(tag = "viewModelWindow", pos = [0, 0], width = 1280, height = 720,
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the ViewModelWindow
    with ViewModelWindow:
        # make the new window the primary window
        dpg.set_primary_window("viewModelWindow", True)
        # back button
        dpg.add_button(label = "<- ... / Select a Model / View Model...",
            callback = selectModel, user_data = ["viewModel"], pos = [10, 25])
        # add a model name label
        dpg.add_text("Model name: " + Model['model_name'], pos = [75, 100])
        # add a base information list
        dpg.add_text("Model Base Information:", pos = [75, 200])
        # set a positional offset
        pos_offset = 1
        # for each field in the base info list
        for info in Model['model_base_information']:
            # add a text item for that field
            dpg.add_text("-   " + str(info), pos = [80, 200 + (pos_offset * 25)])
            # increment positional offset
            pos_offset += 1
        # add a machine list
        dpg.add_text("Model Machines:", pos = [400, 200])
        # set a positional offset
        pos_offset = 1
        # for each machine in the machine list
        for machine in Model['model_machines']:
            # add a text item for that machine
            dpg.add_text("-   " + machine, pos = [400, 200 + (pos_offset * 25)])
            # increment positional offset
            pos_offset += 1
        # add Model Actions side panel
        dpg.add_text("Model Actions:", pos = [800, 200])
        # add action buttons
        dpg.add_button(label = "Edit this Model             ->", pos = [800, 225],
            callback = editModel, user_data = ["editModel", Model])
        dpg.add_button(label = "Remove this Model           !!", pos = [800, 250],
            callback = removeModel, user_data = ["removeModel", Model])
        dpg.add_button(label = "Add a Machine to this Model ->", pos = [800, 275],
            callback = addMachine, user_data = ["addMachine", Model])

# select model flow 
def selectModel(sender, app_data, user_data):
    """selectModel(user_data = continueCode)

    continueCode: str; continue code correspdonding to the action being performed.
    
    StartupWindow -> SelectModelWindow

    Invokes the UI flow from the StartupWindow to the SelectModelWindow.
    Invoked by the main menu bar.
    """
    # get the continue code from user_data
    continueCode = user_data[0]
    # clear the subsequent model aliases
    clearWindowRegistry()
    # enable the SelectModelWindow
    SelectModelWindow = dpg.window(tag = "selectModelWindow", pos = [0, 0], width = 1280, height = 720, 
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the SelectModelWindow
    with SelectModelWindow:
        # make the new window the primary window
        dpg.set_primary_window("selectModelWindow", True)
        # back button
        dpg.add_button(label = "<- Main Menu / Select a Model...",
            callback = returnToStartup, pos = [10, 25])
        # model selection listbox
        # add select model label (always visible)
        dpg.add_text("Select a Model:", pos = [75, 50])
        # pull models from KIM Interface config
        models = getModels()
        # create a name list
        list_items = []
        # for each model in KIM Interface config
        for model in models:
            # add the name to the list
            list_items.append(model['model_name'])
        # if list is empty
        if not list_items:
            # just add "None"; skip the list
            dpg.add_text("No Models Configured", pos = [25, 75])
        # there are models to list
        else:
            # sort the mapping configuration list
            list_items = sorted(list_items, reverse = False)
            # create the model selection listbox
            ModelListbox = dpg.add_listbox(items = list_items, width = 350, pos = [25, 75], 
                num_items = 20, default_value = list_items[0])
            # if continue code calls for moving to SelectMachineWindow
            if continueCode in ["addConfig","viewConfig","editConfig","removeConfig",
                "viewMachine","editMachine","removeMachine"]:
                # make sure there is no select model button
                deleteItem(sender = "", app_data = "", user_data = ["selectModelButton"])
                # set the model list callback
                dpg.set_item_callback(ModelListbox, selectMachine)
                # set the ModelListbox user data
                dpg.set_item_user_data(ModelListbox, [continueCode, ModelListbox])
            # otherwise don't use the SelectMachineWindow
            else:
                # add a select model button
                SelectModelButton = dpg.add_button(tag = "selectModelButton", label = "Select this Model", 
                    width = 270, pos = [50, 600])
                # if continue code is to edit
                if continueCode == "editModel":
                    # set the callback for the button to edit
                    dpg.set_item_callback(SelectModelButton, editModel)
                # if continue code is to remove
                elif continueCode == "removeModel":
                    # set the callback for the button to remove
                    dpg.set_item_callback(SelectModelButton, removeModel)
                # if continue code is add a machine
                elif continueCode == "addMachine":
                    # set the callback for the button to add machine
                    dpg.set_item_callback(SelectModelButton, addMachine)
                # otherwise just view the model
                else:
                    # add a select model button
                    dpg.set_item_callback(SelectModelButton, viewModel)
                # set the button's user data
                dpg.set_item_user_data(SelectModelButton, [continueCode, ModelListbox])


## INFORMATION UI CALLBACKS
#__________________________________________________________________________________________________
# callback to generate a URL
def generateURL(sender, app_data, user_data):
    """generateURL(user_data = [URLBox])
    
    URLBox: DPG Item; DPG Inputbox holding the current URL.

    Generates a URL that would produce the requested results in an i-Reporter form.
    """
    # get the ID of the URLBox
    URLBox = user_data[0]
    # save machine_name
    machine_name = dpg.get_value("machineNameText")
    # save mapping_config
    mapping_config = dpg.get_value("mappingConfigText")
    # build the URL call string
    url = "http://10.1.30.90:3000/api/v1/getvalue/KIM_Interface?"
    # check that a Machine is selected
    if not machine_name == "Default":
        # add the machine_name to the url, replacing spaces with underscore for URL format
        url += "machine_name=" + str(machine_name.replace(' ', '_'))
        # check that a Mapping Configuration is selected
        if not mapping_config == "Default":
            # add the current mapping_config to the url
            url += "&mapping_config=" + mapping_config
        # else reset the url and warn the user to select a Config
        else:
            # show a warning Popup
            showWarningPopup("Please select a Mapping Configuration to generate a URL.")
            # clear the url value
            url = ""
    # else reset the url and warn the user to select a Machine
    else:
        # show a warning Popup
        showWarningPopup("Please select a Machine to generate a URL.")
        # clear the url value
        url = ""
    # update the url box
    dpg.set_value(URLBox, url)

# updates the selected Mapping Configuration
def updateSelectedMapping(sender, app_data, user_data):
    """updateSelectedMapping(user_data = [ConfigurationListbox, MappingConfigText])
    
    ConfigurationListbox: DPG Listbox; Listbox holding the selected Config.
    MachineNameText: DPG Text; Item holding the current selected mapping_config.

    Updates the selected mapping config with the current selection in the Configurations listbox.
    """
    # get the current value of the Machine Listbox
    machine_name = dpg.get_value(user_data[0])
    # set the Machine text value
    dpg.set_value(user_data[1], machine_name)

# updates the Mapping Configuration selection Listbox items
def updateMappingConfigurationList(sender, app_data, user_data):
    """updateMappingConfigurationList(user_data = [ConfigurationListbox, config_list])
    
    ConfigurationListbox: DPG Listbox; Listbox holding the selected Config.
    config_list: [configuration id]; list of configuration ids from the selected Machine.

    Updates the list of Mapping Configurations to show in the Information window.
    """
    # get the ConfigurationListbox object
    ConfigListbox = user_data[0]
    # get the config list
    config_list = user_data[1]
    # sort the config list
    config_list = sorted(config_list, reverse = False)
    # update the list
    dpg.configure_item(ConfigListbox, items = config_list)

# updates the selected machine text
def updateSelectedMachine(sender, app_data, user_data):
    """updateSelectedMachine(user_data = [MachineListbox, ConfigurationListbox, MachineNameText])
    
    MachineListbox: DPG Listbox; Listbox holding the selected Machine.
    ConfigurationListbox: DPG Listbox; Listbox holding the selected Config.
    MachineNameText: DPG Text; Item holding the current selected machine_name.

    Updates the selected machine name with the current selection in the Machines listbox.
    """
    # get the current value of the Machine Listbox
    machine_name = dpg.get_value(user_data[0])
    # set the Machine text value
    dpg.set_value(user_data[2], machine_name)
    # get the machine file for this Machine
    machine_file = openMachineConfiguration(machine_name)
    # get the mapping configurations
    config_list = machine_file['mappings']
    # update the list to just hold IDs
    for i in range(len(config_list)):
        # set the current index of the list to just the ID
        config_list[i] = config_list[i]['id']
    # show the mapping configuration selection list
    updateMappingConfigurationList(sender = "", app_data = "", user_data = [user_data[1], config_list])

# callback to show the Results View window
def showResultsView(sender, app_data, user_data):
    """showResultsView(user_data = [])

    Creates a widget view that shows the most recent results.
    """
    # is the informationWindow shown?
    if dpg.does_alias_exist("informationWindow"):
        # clear the showResultsView window
        clearWindow("resultsViewWindow")
        # create the widget view
        ResultsViewWindow = dpg.window(tag = "resultsViewWindow", label = "Current Results", width = 550, 
            height = 240, no_move = False, no_close = False, no_collapse = True, no_resize = True, 
            no_title_bar = False, pos = [dpg.get_viewport_width() - 575, 30])
        # add items to the Result View Window
        with ResultsViewWindow:
            # get the results.txt file text
            File = open(os.path.join(sys_env_dir, "results.txt"), 'r')
            # read the file
            results = File.read()
            # close the file
            File.close()
            # replace invalid character readings
            results = results.replace('Ã˜', 'Ø')
            results = results.replace('Â±', '±')
            # add a list of outputs
            dpg.add_text(results)
    # the info window isnt open yet, open it with the Results window flag set
    else:
        informationWindow(sender = "", app_data = "", user_data = [False, True, False])

# callback to show the Logs View window
def showLogsView(sender, app_data, user_data):
    """showLogsView(user_data = [])

    Creates a widget view that shows the logs from the system.
    """
    # is the informationWindow shown?
    if dpg.does_alias_exist("informationWindow"):
        # clear the showLogsView window
        clearWindow("logsViewWindow")
        # create the widget view
        LogsViewWindow = dpg.window(tag = "logsViewWindow", label = "Current Log Entries", width = 300, 
            height = 415, no_move = False, no_close = False, no_collapse = True, no_resize = True, 
            no_title_bar = False, pos = [dpg.get_viewport_client_width() - 310, 280])
        # add items to the Log View Window
        with LogsViewWindow:
            # get the runtime_log.txt file text
            File = open(os.path.join(sys_env_dir, "logs", "runtime_log.txt"), 'r')
            # read the file
            logs = File.read()
            # close the file
            File.close()
            # add a list of outputs
            dpg.add_text(logs)
    # the info window isnt open yet, open it with the Results window flag set
    else:
        informationWindow(sender = "", app_data = "", user_data = [False, False, True])

# callback to show the URL View window
def showURLView(sender, app_data, user_data):
    """showURLView(user_data = [])

    Creates a widget view that shows the Machine and Mapping Configurations being requested;
    Allows the generation of URLs.
    """
    # is the informationWindow shown?
    if dpg.does_alias_exist("informationWindow"):
        # clear the showURLView window
        clearWindow("urlViewWindow")
        # create the widget view
        URLViewWindow = dpg.window(tag = "urlViewWindow", label = "Generated URL", width = 500, 
            height = 250, no_move = False, no_close = False, no_collapse = True, no_resize = True, 
            no_title_bar = False, pos = [10, dpg.get_viewport_client_height() - 260])
        # add items to the URL View Window
        with URLViewWindow:
            # add a label
            dpg.add_text("i-Reporter URL Call (copy to i-Reporter action cluster):", 
                color = [150, 150, 255])
            # create an input box to put the URL call in
            URLBox = dpg.add_input_text(width = 480, hint = "Click 'Generate URL' to see a URL...")
            # add information text
            dpg.add_text("To use this URL, do the following:\n"
                        + "   1. In i-Reporter, add an action cluster to the form;\n"
                        + "   2. Set the cluster to the 'Gateway Linkage' function;\n"
                        + "   3. Copy the above URL into the Gateway Linkage URL.\n")
            # add a generate url button
            dpg.add_button(label = "Generate URL", width = 100, height = 25,
                pos = [200, 175], callback = generateURL, user_data = [URLBox])
    # the info window isnt open yet, open it with the Results window flag set
    else:
        informationWindow(sender = "", app_data = "", user_data = [True, False, False])

# information window
def informationWindow(sender, app_data, user_data):
    """informationWindow(user_data = [showURL, showResults, showLogs])
    
    Navigation Menu -> Information Window
    
    showURL: Boolean; toggles the URL view on opening of the information window.
    showResults: Boolean; toggles the Results view on opening of the information window.
    showLogs: Boolean; toggles the Logs view on opening of the information window.

    Opens the Information window.
    """
    # clear the subsequent aliases
    clearWindowRegistry()
    # enable the InformationWindow
    InformationWindow = dpg.window(tag = "informationWindow", pos = [0, 0], width = 1280, height = 720, 
        no_move = True, no_close = True, no_collapse = True, no_title_bar = False, show = True)
    # add items to the InformationWindow
    with InformationWindow:
        # make the new window the primary window
        dpg.set_primary_window("informationWindow", True)
        # back button
        dpg.add_button(label = "<- Main Menu / Information",
            callback = returnToStartup, pos = [10, 25])
        # add a description label
        dpg.add_text("Please see the KIM Interface User Manual to learn more about this window.",
            pos = [75, 50])
        # add current machine_name label
        dpg.add_text("Current Selected Machine: ", pos = [75, 150])
        # add current machine_name text object
        MachineNameText = dpg.add_text("Default", tag = "machineNameText",
             color = [0, 255, 0], pos = [75, 175])
        # add current mapping_config label
        dpg.add_text("Current Selected Mapping Configuration: ", pos = [75, 225])
        # add current mapping_config text object
        MappingConfigText = dpg.add_text("Default", tag = "mappingConfigText",
             color = [0, 255, 0], pos = [75, 250])
        # add runtime label
        dpg.add_text("Current Average Runtime:", pos = [75, 300])
        # add the text object that holds the current runtime avg
        dpg.add_text(currentAverageRuntime(), color = [0, 255, 0], pos = [75, 325])
        # create a Machine List
        machines = getMachines()
        # create a pruned copy just holding the Machine names
        machine_names = []
        # for every Machine in the configuration file
        for machine in machines:
            # add Machine name to machine_names list
            machine_names.append(machine['name'])
        # add Machine selection label
        dpg.add_text("Select a Machine:", pos = [400, 150])
        # sort the mapping configuration list
        machine_names = sorted(machine_names, reverse = False)
        # add a listbox to select Machines from
        MachineListbox = dpg.add_listbox(items = machine_names, callback = updateSelectedMachine,
            pos = [400, 175], default_value = None, width = 250, num_items = 20)
        # add Config selection label
        dpg.add_text("Select a Configuration:", pos = [700, 150])
        # add a listbox to select Configs from
        ConfigListbox = dpg.add_listbox(items = ["Select a machine..."], callback = updateSelectedMapping,
            pos = [700, 175], default_value = None, width = 200, num_items = 20)
        # set the listbox' user_data
        dpg.set_item_user_data(MachineListbox, [MachineListbox, ConfigListbox, MachineNameText])
        # set the listbox' user_data
        dpg.set_item_user_data(ConfigListbox, [ConfigListbox, MappingConfigText])
        # check view flags
        if user_data[0]:
            # show the URL view on open
            showURLView("", "", "")
        if user_data[1]:
            # show the Results view on open
            showResultsView("", "", "")
        if user_data[2]:
            # show the Logs view on open
            showLogsView("", "", "")


## HELP WINDOW UI CALLBACKS
#__________________________________________________________________________________________________
# open github repo page
def openInBrowser(sender, app_data, user_data):
    """openInBrowser(user_data = [])
    
    opens the github repository in the user's web browser
    """
    web("https://github.com/masonritchason/KIM-Interface-Manager", new = 0, autoraise = True)

# generate an email draft
def emailDraft():
    """emailDraft(user_data = [])
    
    opens a new email addressed to Mason Ritchason (masonritchason@gmail.com)
    """
    # set a mailto link
    mailto = "mailto:masonritchason@gmail.com?subject=[KIM Interface Manager] Help Request&body=Hello, my name is <your name here>.I am requesting help with your software KIM Interface Manager.My issue is that <describe your issue>.I encounter it when I <describe how you create/recreate the issue>.<include extra info, context, images, etc.>I would love to see this issue resolved by <describe your suggested solution>."

    # open the mailto link
    web(mailto)

# contact card popup
def contactCard(sender, app_data, user_data):
    """contactCard(user_data = [])
    
    Navigation Menu -> Contact Card

    Opens a small "More help" contact card popup.
    """
    # clear the subsequent aliases
    clearWindow("contactPopup")
    # create the window
    ContactCard = dpg.window(tag = "contactPopup", label = "More Help", width = 500, height = 225, 
        no_move = False, no_close = False, no_collapse = True, no_resize = True, 
        pos = [(dpg.get_viewport_client_width() / 2) - 250, (dpg.get_viewport_client_height() / 2) - 137.5])
    # add items to the popup
    with ContactCard:
        # add a title label
        dpg.add_text("Need More Help?", color = [150, 150, 255])
        # add help instructions
        dpg.add_text("Make sure to consult the KIM Interface User's Manual.\n" +
            "Answers to questions and solutions to many issues can be found there.\n" +
            "Consult your IT Department with issues as well. If you are still\n" +
            "unable to solve your problem after doing so, click below to visit\n" +
            "the public KIM Interface Manager support page:")
        # add a go to github button
        dpg.add_button(label = "KIM Interface Manager on GitHub", width = 250, pos = [135, 130],
            callback = openInBrowser)
        # email label text
        dpg.add_text("Additionally, feel free to email Mason Ritchason with any questions:", pos = [10, 170])
        # email text
        dpg.add_button(label = "Email masonritchason@gmail.com", width = 250, pos = [135, 195],
            callback = emailDraft)

# help window
def helpWindow(sender, app_data, user_data):
    """helpWindow(user_data = [chapter, page_num, pos = [view - 685, 0]])
    
    Navigation Menu -> Help Window
    
    chapter: int; indicates the chapter to render in the help menu.
    page_num: int; the page number to render on the help window.
    pos: [x, y]; (optional) location of the help window. 
        Defaults to the right edge of the viewport.

    Opens the help pages window.
    """
    # save the chapter titles
    chapter_titles = ["System Environment", "The KIM Interface", "Getting Started", 
        "Mapping Configurations", "Machines", "Models", "System Information", 
        "i-Reporter Integration", "Administrative Notes"]
    # get the help chapter info
    chapter = user_data[0]
    page_num = user_data[1]
    pos = user_data[2]
    # is there a position passed?
    if not pos:
        # default value
        pos = [(dpg.get_viewport_width() - 685), 0]
    # else use the current position of the window
    else:
        pos = dpg.get_item_pos("helpWindow")
    # set the path to the folder of chapter pages in system files
    temp = os.path.join(sys_env_dir, "build", "help", "chap" + str(chapter))
    # hold a list of the page images
    pages = []
    # add each image to the list of pages
    for root, dirs, files in os.walk(top = temp, topdown = False):
        # for each file in the directory
        for file in files:
            # pull the image from the folder
            page = dpg.load_image(os.path.join(root, file))
            # add the image to the pages list
            pages.append(page)
    # create a texture registry
    with dpg.texture_registry():
        # generate a texture from the page
        Page = dpg.add_static_texture(width = pages[page_num][0], height = pages[page_num][1], 
            default_value = pages[page_num][3])
    # clear the subsequent aliases
    clearWindow("helpWindow")
    # enable the helpWindow
    HelpWindow = dpg.window(tag = "helpWindow", label = ("> Chapter " + str(chapter) + " - " 
        + chapter_titles[chapter - 1]), pos = pos, width = 670, height = 660, no_move = False, 
        no_close = False, no_collapse = True, no_title_bar = False, show = True)
    # add items to the HelpWindow
    with HelpWindow:
        # add previous chapter button if there is a previous chapter
        if chapter > 1:
            # add the previous chapter button
            dpg.add_button(label = "<< chapter " + str(chapter - 1), width = 100, pos = [185, 25], 
                callback = helpWindow, user_data = [chapter - 1, 0, "update"])
        # add previous page button if there is a previous page
        if page_num > 0:
            # add the previous button
            dpg.add_button(label = "< pg", width = 40, pos = [290, 25], callback = helpWindow,
                user_data = [chapter, page_num - 1, "update"])
        # add next page button if there is a next page
        if page_num < (len(pages) - 1):
            # add the next button
            dpg.add_button(label = "pg >", width = 40, pos = [335, 25], callback = helpWindow,
                user_data = [chapter, page_num + 1, "update"])
        # add next chapter button if there is a next chapter
        if chapter < 9:
            # add the next chapter button
            dpg.add_button(label = ">> chapter " + str(chapter + 1), width = 100, pos = [380, 25], 
                callback = helpWindow, user_data = [chapter + 1, 0, "update"])
        # show the requested help page
        dpg.add_image(texture_tag = Page, pos = [0, 50])


### Main Function Segment
#__________________________________________________________________________________________________
# verify the config folder
try:
    # create the folder (first run)
    os.mkdir(os.path.join(sys_env_dir, "config"))
except Exception:
    # folder exists
    pass

# verify the mapping configurations folder
try:
    # create the folder (first run)
    os.mkdir(os.path.join(sys_env_dir, "config", "mapping configurations"))
except Exception:
    # folder exists
    pass

# verify the KIM_interface_configuration.json file
try:
    # make a dict object to format the empty config file
    temp = {"timestamp":str(str(datetime.now()) + " | " + str(user)), "models":[], "machines":[]}
    # format the dict as JSON
    temp = dumps(temp, indent = 4)
    # create the file (first run)
    File = open(os.path.join(sys_env_dir, "config", "KIM_interface_configuration.json"), 'x')
    # write the dict to the file
    File.write(temp)
    File.close()
except Exception:
    # file exists
    pass

# verify the backups folder
try:
    # create the bin folder first (first run)
    os.mkdir(os.path.join(sys_env_dir, "bin"))
    # create the backups folder
    os.mkdir(os.path.join(sys_env_dir, "bin", "backups"))
except Exception:
    try:
        # create the backups folder
        os.mkdir(os.path.join(sys_env_dir, "bin", "backups"))
    except Exception:
        # bin and backups folders exist
        pass
    # backup folder exists
    pass

# verify the changelog.txt file
try:
    # create the file (first run)
    File = open(os.path.join(sys_env_dir, "logs", "changelog.txt"), 'x')
    File.close()
except Exception:
    # file exists
    pass

# create a backup
createConfigBackup()

# add items to the StartupWindow
with StartupWindow:
    # add welcome text
    dpg.add_text("Welcome to the KIM Interface Manager, " + str(user) + "!", pos = [10, 25])
    dpg.add_text("KIM Interface v" + version + " - " + version_date, pos = [10, 50])
    # add info text
    dpg.add_text("What can this software do?", pos = [10, 100])
    dpg.add_text("The KIM Interface Manager allows you to create, view,\n" +
                 "customize, and remove mapping configurations, machines, and\n" +
                 "models for the KIM Interface to use in i-Reporter forms.\n\n" + 
                 "To add a new configuration, use the Top Menu to navigate\n" +
                 "to the 'New...' menu and select 'Configuration'.", 
                 pos = [10, 125])
    # set temp path to the changelog.md file
    temp = os.path.join(sys_env_dir[:len(sys_env_dir) - 11], ".github", "CHANGELOG.md")
    # get the changelog.md text
    File = open(temp, 'r')
    # read and close the file
    lines = File.readlines()
    File.close()
    # remove the first 4 lines (header)
    lines = lines[4:]
    # hold a changetext variable
    changetext = ""
    # for each line in the file
    for line in lines:
        # if the line starts as a note
        if line[0] == '>':
            # ignore the line
            continue
        # process the markdown format
        line = line.replace('# ', '')
        line = line.replace('#', '')
        line = line.replace('`', '')
        # add the remaining line to the changetext
        changetext += "\n" + str(line)
    # create a changelog window element
    Changelog = dpg.window(tag = "changelogWindow", pos = [865, 125], width = 500, height = 500, 
        no_move = True, no_close = True, no_collapse = True, no_title_bar = True, show = True,
        no_background = False, no_resize = True)
    with Changelog:
        # add a text object to show the changelog
        dpg.add_text(changetext, wrap = 475)
    # add a changelog label
    dpg.add_text("Changelog - Latest", pos = [865, 100])
    # add an exit manager button
    dpg.add_button(label = "Save & Exit", width = 300, height = 50, 
        pos = [10, 620], callback = closeProgram)

# create the menu bar
MenuBar = dpg.viewport_menu_bar()

# add the menu items to the menu bar
with MenuBar:
    # add a main menu button
    MainMenu = dpg.menu(label = "File", indent = 0)
    # add the new menu item
    NewMenu = dpg.menu(label = "New", indent = 75)
    # add the edit menu item
    EditMenu = dpg.menu(label = "Edit", indent = 150)
    # add the view menu item
    ViewMenu = dpg.menu(label = "View", indent = 225)
    # add the delete menu item
    DeleteMenu = dpg.menu(label = "Delete", indent = 300)
    # add the information menu item
    InformationMenu = dpg.menu(label = "Information", indent = 375)
    # add the help menu item
    HelpMenu = dpg.menu(label = "Help", indent = 480)
    # set up the individual sub-menus
    with MainMenu:
        # add a main menu button
        dpg.add_menu_item(label = "Main Menu", callback = returnToStartup)
        # add a save and exit button
        dpg.add_menu_item(label = "Save & Exit", callback = closeProgram)
    with NewMenu:
        # add necessary items (config, machine, model)
        dpg.add_menu_item(label = "Mapping Configuration",
            callback = selectModel, user_data = ["addConfig"])
        dpg.add_menu_item(label = "Machine",
            callback = selectModel, user_data = ["addMachine"])
        dpg.add_menu_item(label = "Model",
            callback = addModel, user_data = ["addModel"])
    with EditMenu:
        # add necessary items (config, machine, model)
        dpg.add_menu_item(label = "Mapping Configuration", 
            callback = selectModel, user_data = ["editConfig"])
        dpg.add_menu_item(label = "Machine",
            callback = selectModel, user_data = ["editMachine"])
        dpg.add_menu_item(label = "Model",
            callback = selectModel, user_data = ["editModel"])
    with ViewMenu:
        # add necessary items (config, machine, model)
        dpg.add_menu_item(label = "Mapping Configuration", 
            callback = selectModel, user_data = ["viewConfig"])
        dpg.add_menu_item(label = "Machine",
            callback = selectModel, user_data = ["viewMachine"])
        dpg.add_menu_item(label = "Model",
            callback = selectModel, user_data = ["viewModel"])
    with DeleteMenu:
        # add necessary items (config, machine, model)
        dpg.add_menu_item(label = "Mapping Configuration", 
            callback = selectModel, user_data = ["removeConfig"])
        dpg.add_menu_item(label = "Machine",
            callback = selectModel, user_data = ["removeMachine"])
        dpg.add_menu_item(label = "Model",
            callback = selectModel, user_data = ["removeModel"])
    with InformationMenu:
        # add necessary items (open information)
        dpg.add_menu_item(label = "View Information", callback = informationWindow,
            user_data = [False, False, False])
        dpg.add_menu_item(label = "Show URL View", callback = showURLView,
            user_data = [True, False, False])
        dpg.add_menu_item(label = "Show Results View", callback = showResultsView,
            user_data = [False, True, False])
        dpg.add_menu_item(label = "Show Log View", callback = showLogsView,
            user_data = [False, False, True])
    with HelpMenu:
        # add necessary items (open help chapters)
        Chap1 = dpg.add_menu_item(label = "System Environment", callback = helpWindow,
            user_data = [1, 0, []])
        Chap2 = dpg.add_menu_item(label = "The KIM Interface", callback = helpWindow,
            user_data = [2, 0, []])
        Chap3 = dpg.add_menu_item(label = "Getting Started", callback = helpWindow,
            user_data = [3, 0, []])
        Chap4 = dpg.add_menu_item(label = "Mapping Configurations", callback = helpWindow,
            user_data = [4, 0, []])
        Chap5 = dpg.add_menu_item(label = "Machines", callback = helpWindow,
            user_data = [5, 0, []])
        Chap6 = dpg.add_menu_item(label = "Models", callback = helpWindow,
            user_data = [6, 0, []])
        Chap7 = dpg.add_menu_item(label = "System Information", callback = helpWindow,
            user_data = [7, 0, []])
        Chap8 = dpg.add_menu_item(label = "i-Reporter Integration", callback = helpWindow,
            user_data = [8, 0, []])
        Chap9 = dpg.add_menu_item(label = "Administrative Notes", callback = helpWindow,
            user_data = [9, 0, []])
        # more menu opens a special window with a business card style design
        Chap10 = dpg.add_menu_item(label = "More...", callback = contactCard)
    

# show viewport
dpg.setup_dearpygui()
# set the viewport icon
dpg.set_viewport_large_icon(os.path.join(sys_env_dir, "build", "icon.ico"))
dpg.set_viewport_small_icon(os.path.join(sys_env_dir, "build", "icon.ico"))
dpg.show_viewport()
# set the primary window and maximize the view
dpg.set_primary_window("startupWindow", True)
dpg.maximize_viewport()
# start dearpygui main loop
dpg.start_dearpygui()