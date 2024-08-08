

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
from classes.Model import Model as Model
from classes.Machine import Machine as Machine
from classes.MappingConfiguration import MappingConfiguration as MappingConfiguration


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

    -> Interface_Config_File
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
    
    new_config_object: config; the edited config File object that needs to be
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


### Object-Returning Functions
# get Configs from the KIM Interface config file
def getConfigs(machine):
    """getConfigs(machine)
    
    Returns the list of configs currently in the passed machine.

    machine: machine Object; the machine to return its Configs.

    -> [config]
    """
    # create a list to hold the config objects
    configs = []
    # add Configs from each machine's config list in the machines list 
    for i in range(len(machine.mapping_configurations)):
        # save the current config
        curr = machine.mapping_configurations[i]
        # create a config object
        TempConfig = MappingConfiguration(curr['id'], curr['mappings'], machine)
        # append that object to the list
        configs.append(TempConfig)
    # return configs list
    return configs

# get Machines from the KIM Interface config file
def getMachines(model, get_configs):
    """getMachines(model, get_configs)
    
    Returns the list of Machines currently in the passed model.

    model: model Object; the model object to return its Machines.
    get_configs: bool; indicate whether to get config objects.

    -> [machine]
    """
    # create a list to hold the machine objects
    machines = []
    # add Machines from the passed model's machine list 
    for i in range(len(model.machines)):
        # save the current machine
        curr = model.machines[i]
        # create a machine object
        TempMachine = Machine(curr['name'], curr['measurements'], 
            curr['mapping_configurations'], model)
        # fix machine measurement character issues
        for j in range(len(TempMachine.measurements)):
            # save current measurement
            curr = TempMachine.measurements[j]
            # replace characters 
            curr = curr.replace('Ã˜', 'Ø')
            curr = curr.replace('Â±', '±')
            # save the changed measurement
            TempMachine.measurements[j] = curr
        # if the get configs flag is set
        if get_configs:
            # add the machine's Configs to its Configs attribute
            TempMachine.mapping_configurations = getConfigs(TempMachine)
        # append that object to the list
        machines.append(TempMachine)
    # return machines list
    return machines

# get Models from the KIM Interface config file
def getModels(get_machines, get_configs):
    """getModels(get_machines, get_configs)
    
    Returns the list of Models currently in the KIM Interface config file.

    get_machines: bool; indicate whether to get machine objects.
    get_configs: bool; indicate whether to continue after getMachines (config objects).

    -> [model]
    """
    # get the KIM Interface config
    Interface_Config_File = openConfigFile()
    # set models
    models = Interface_Config_File['models']
    # convert to a list of model objects
    for i in range(len(models)):
        # save current model
        curr = models[i]
        # create a new model object
        TempModel = Model(curr['name'], curr['base_information'], curr['machines'])
        # if the get_machines flag is set
        if get_machines:
            # add the model's Machines to its Machines attribute
            TempModel.machines = getMachines(TempModel, get_configs)
        # overwrite the model in the models list
        models[i] = TempModel
    # return models list
    return models

# return a model object flexibly
def dynamicGetModel(model_input):
    """
    Dynamically returns a model object from a passed DPG listbox item or a string.

    model_input: Model | DPG Listbox | str; some form of identifying information of a model.
    """
    #debug
    print("getModel: Trying value " + str(model_input) + " w/type: " + str(type(model_input)))
    # get model list
    models = getModels(get_machines = True, get_configs = True)
    # test if input is already a model
    if not (isinstance(model_input, Model)):
        #debug
        print("getModel: Value " + str(model_input) + " is not of Model Class type")
        # find the actual model object
        for i in range(len(models)):
            # save the current model
            curr = models[i]
            # do the model names match?
            try:
                if curr.name == dpg.get_value(model_input):
                    # return the current model
                    #debug
                    print("getModel: Value " + str(model_input) + " is of DPG Class type.")
                    return curr
            # input isn't a dpg item, it must be a string
            except Exception as ex:
                #debug
                print("getModel: Value " + str(model_input) + " is not of DPG Class type. Trying as string")
                if str(curr.name) == str(model_input):
                    # return the current model
                    #debug
                    print("getModel: Value " + str(model_input) + " is of string type.")
                    return curr
                #debug
                print("getModel: Value " + str(model_input) + " is not of string type")
    # the model is already a model, just return it
    else:
        return model_input

# return a machine object flexibly
def dynamicGetMachine(machine_input, model = None):
    """
    Dynamically returns a machine object from a passed DPG listbox item or a string.

    machine_input: Machine | DPG Listbox | str; some form of identifying information of a machine.
    model: (optional) Model; limits the search to a specific model object.
    """
    # hold a machines list
    machines = []
    # if a model is passed
    if not (model is None):
        # search is limited to this model, use its machine list
        machines = model.machines
    # model limiter wasn't passed; search all models
    else:
        # get model list
        models = getModels(get_machines = True, get_configs = True)
        # for each model in the list
        for curr_model in models:
            # for each machine in the model's list
            for machine in curr_model.machines:
                # append this machine to the list
                machines.append(machine)
    # test if input is already a machine
    if not (isinstance(machine_input, Machine)):
        # for each machine in the machines list
        for i in range(len(machines)):
            # save the current machine
            curr_machine = machines[i]
            # do the machine names match?
            try:
                # attempt with input as a DPG Listbox
                if curr_machine.name == dpg.get_value(machine_input):
                    # return the current machine
                    return curr_machine
            # input isn't a dpg item, it must be a string
            except Exception as ex:
                if str(curr_machine.name) == str(machine_input):
                    # return the current machine
                    return curr_machine
    # the machine is already a machine, just return it
    else:
        return machine_input

# return a config object flexibly
def dynamicGetConfig(config_input, machine = None):
    """
    Dynamically returns a config object from a passed DPG listbox item or a string.

    config_input: Config | DPG Listbox | str; some form of identifying information of a config.
    machine: (optional) Machine; limits the search to a specific machine object.
    """
    # hold a configs list
    configs = []
    # if a machine is passed
    if not (machine is None):
        # search is limited to this machine, use its config list
        configs = machine.mapping_configurations
    # machine limiter wasn't passed; search all machines
    else:
        # get model list
        models = getModels(get_machines = True, get_configs = True)
        # for each model in the list
        for curr_model in models:
            # for each machine in the model's list
            for curr_machine in curr_model.machines:
                # for each config in the machine's list
                for curr_config in curr_machine.mapping_configurations:
                    # append this config to the list
                    configs.append(curr_config)
    # test if input is already a config
    if not (isinstance(config_input, MappingConfiguration)):
        # for each config in that machine's config list
        for i in range(len(configs)):
            # save the current config
            curr_config = configs[i]
            # do the config ids match?
            try:
                # attempt with input as a DPG Listbox
                if curr_config.id_num == dpg.get_value(config_input):
                    # return the current config
                    return curr_config
            # input isn't a dpg item, it must be a string
            except Exception as ex:
                if str(curr_config.id_num) == str(config_input):
                    # return the current config
                    return curr_config
    # the config is already a config, just return it
    else:
        return config_input


### Validation Functions
# validates the input of an ADDED config
def validateAddConfigInput(model, machine, new_id, info_checks, measurement_checks, 
    info_maps, measurement_maps):
    """
    validateAddConfigInput(model, machine, new_id, info_checks, measurement_checks, 
            info_maps, measurement_maps)

    model: model; model the config belongs to.
    machine: machine; machine the config belongs to.
    new_id: str; input id of the config.
    info_checks: [DPG Checkboxes]; list of the checkboxes used to select included model info.
    measurement_checks: [DPG Checkboxes]; list of the checkboxes used to 
        select included machine measurements.
    info_maps: [DPG Inputs]; list of the inputs used to assign each model info a sheet/cluster map.
    measurement_maps: [DPG Inputs]; list of the inputs used to assign each machine measurement a 
        sheet/cluster map.

    Takes a full set of information that defines a Configuration 
    and returns the validation of that info.
    
    -> [Boolean:result, Config|Error]
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
            # get the machine's config list
            machine_configs = openMachineConfiguration(machine['name'])
            machine_configs = machine_configs['mappings']
            # check that it is unique
            for config in machine_configs:
                # if the config IDs match
                if config['id'] == new_id:
                    # overlapping IDs, not unique
                    return [False, 
                        {"error":"Mapping Configuration IDs must be unique.\n"
                        + "The ID " + new_id + " for " + machine['name'] 
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
                    {"item":model['model_base_information'][index], 
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
                    {"item":machine['measurements'][index], 
                    "sheet":int(sheet), "cluster":int(cluster), "type":"string", "value":""})
        # increment the model_info_loop
        index += 1
    # if here, the config information can make a config Object
    config = {"id":new_id, "configuration":[]}
    # add each of the maps to the configuration list
    for curr_map in map_list:
        # add the item
        config["configuration"].append(curr_map)
    # return the config
    return [True, config]

# validates the input of an EDITED config
def validateEditConfigInput(model, machine, config, new_id, prior_id, checks, inputs):
    """
    validateEditConfigInput(model, machine, config, new_id, prior_id, checks, inputs)

    model: model; model the config belongs to
    machine: machine; machine the config belongs to
    config: config; the config being edited
    id: str; edited input id of the config
    prior_id: str; original id of the config
    checks: [DPG Checkboxes]; list of the checkboxes used to select included maps
    inputs: [DPG Inputs]; list of the inputs used to assign each map a sheet/cluster map

    Takes a full edited Configuration and returns the validation of that info.
    
    -> [Boolean:result, Config|Error]
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
            # get the machine's config list
            machine_configs = openMachineConfiguration(machine['name'])
            machine_configs = machine_configs['mappings']
            # check that it is unique
            for config in machine_configs:
                # if the config IDs match
                if config['id'] == new_id:
                    # is the match with the prior ID
                    if config['id'] == prior_id:
                        # skip this config, the ID can match its previous ID
                        continue
                    else:
                        # overlapping IDs, not unique
                        return [False, 
                            {"error":"Mapping Configuration IDs must be unique.\n"
                            + "The ID " + new_id + " for " + machine['name'] 
                            + " has already been assigned.\n"
                            + "Choose a different Mapping Configuration" 
                            + " ID for this new Configuration."}]
    # create a map list to hold the verified mapping items
    map_list = []
    # track the index of the config's map list
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
                    {"item":config['configuration'][index]['item'], "sheet":sheet, 
                    "sheet":int(sheet), "cluster":int(cluster), "type":"string", "value":""})
        # increment the model_info_loop
        index += 1
    # if here, the config information can make a config Object
    config = {"id":new_id, "configuration":[]}
    # add each of the maps to the configuration list
    for curr_map in map_list:
        # add the item
        config["configuration"].append(curr_map)
    # return the config
    return [True, config]

# validates the input of an ADDED machine
def validateAddMachineInput(model, machine_name, measurements):
    """
    validateAddMachineInput(model, machine_name, measurements)

    model: model; model the config belongs to.
    machine_name: str; the new machine's name.
    measurements: [DPG Inputs]; list of the DPG items used to assign each machine measurement 
        a specification. 

    Takes a full set of information defining a machine and returns the validation of that info.
    
    -> [Boolean:result, machine|Error]
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
            # get the model's machine list
            model_machines = model['model_machines']
            # check that the name is unique
            for curr_machine in model_machines:
                # if the machine names match
                if curr_machine == machine_name:
                    # overlapping names, not unique
                    return [False, 
                        {"error":"Machine names must be unique.\n"
                        + "The Machine '" + machine_name + "' for " + model['model_name']
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
    # if here, the machine information can make a machine Object
    machine = {"name":machine_name, "measurements":[]}
    # add each of the measurements to the measurement list
    for meas in meas_list:
        # add the item
        machine['measurements'].append(meas)
    # return the machine
    return [True, machine]        

# validates the input of an EDITED machine
def validateEditMachineInput(model, machine, new_name, prior_name, checks, inputs):
    """
    validateEditMachineInput(model, machine, machine_name, prior_name, checks, inputs)

    model: model; model the machine belongs to.
    machine: machine; machine being edited
    new_name: DPG Input Item; the Inputbox holding the machine's name after editing.
    prior_name: str; name of the machine before editing.
    checks: [DPG Checkboxes]; list of the DPG items used to select measurements.
    inputs: [DPG Inputs]; list of the DPG items used to assign each machine measurement 
        an edited specification.

    Takes an edited machine and returns the validation of that info. 
    
    -> [Boolean:result, machine|Error]
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
            # get the model's machine list
            model_machines = model['model_machines']
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
                            + "The Machine '" + new_name + "' for " + model['model_name']
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
    # if here, the machine information can make a machine Object
    machine = {"name":new_name, "measurements":[]}
    # add each of the measurements to the measurement list
    for meas in meas_list:
        # add the item
        machine['measurements'].append(meas)
    # return the machine
    return [True, machine]   

# validates the input of an ADDED model
def validateAddModelInput(model_name, base_information):
    """
    validateAddModelInput(model_name, base_information)

    model_name: str; name of the new model
    base_information: [DPG Inputs]; list of the DPG items used to assign each model base
        information field a header. 

    Takes a full set of information defining a model and returns the validation of that info.
    
    -> [Boolean:result, model|Error]
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
            # get the model list
            models = getModels(get_machines = False, get_configs = False)
            # check that the name is unique
            for curr_model in models:
                # if the model names match
                if curr_model.name == model_name:
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
    # if here, the model information can make a model Object
    model = Model(name = model_name, base_information = [], machines = [])
    # add each base information to the base information list
    for info in info_list:
        # add the item
        model.base_information.append(info)
    # return the model
    return [True, model]  

# validates the input of an EDITED model
def validateEditModelInput(model, new_name, prior_name, checks, inputs):
    """
    validateEditModelInput(model, new_name, prior_name, checks, inputs)

    model: model; model being edited.
    new_name: DPG Input Item; the Inputbox holding the model's name after editing.
    prior_name: str; name of the model before editing.
    checks: [DPG Checkboxes]; list of the DPG items used to select base information.
    inputs: [DPG Inputs]; list of the DPG items used to assign each model base 
        information an edited header. 
    
    Takes an edited model and returns the validation of that info.
    
    -> [Boolean:result, model|Error]
    """
    # debug
    print("Validating edited Model name " + str(new_name) + " of type " + str(type(new_name)))
    # check that a name was entered
    if (not new_name) or (new_name is None):
        # debug
        print("Value " + str(new_name) + " is empty.")
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
            # get the model list
            models = getModels(get_machines = True, get_configs = True)
            # check that the name is unique
            for curr_model in models:
                # if the model names match
                if curr_model.name == new_name:
                    # if the match is with the prior model name
                    if curr_model.name == prior_name:
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
    # if here, the model information can make a model Object
    model = Model(name = new_name, base_information = [], machines = model.machines)
    # add each of the base information headers to the list
    for info in info_list:
        # add the item
        model.base_information.append(info)
    # return the model
    return [True, model]


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
    """commitConfigEdits(user_data = [continueCode, model, machine, 
        config, new_id, prior_id, checks, inputs])
    
    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning this config
    machine: machine; machine Object owning this config
    config: config; config Object being edited
    new_id: DPG item; Input box holding the edited ID of the config
    prior_id: str; ID of the config before edits
    checks: [DPG Checkboxes]; list of edited selected config items
    inputs: [DPG Input boxes]; list of edited selected config item maps

    Commits a user edit to a mapping configuration in the system environment.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model that owns this config
    model = user_data[1]
    # get the machine that owns this configuration
    machine = user_data[2]
    # get the edited config
    config = user_data[3]
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
    # validate the new config's information
    validation = validateEditConfigInput(model, machine, config, 
        new_id, prior_id, checks, inputs)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new config object
        showWarningPopup(validation[1]['error'])
    # valid config input
    else:
        # input was valid, continue
        EditedConfig = validation[1]
        # get the machine file
        machine_file = openMachineConfiguration(machine['name'])
        # get the index of the edited config
        config_index = machine_file['mappings'].index(config)
        # update the value of that index
        machine_file['mappings'][config_index] = EditedConfig
        # timestamp the file
        machine_file = timestamp(machine_file, str(machine['name']) + ".json", 
            "Edit Configuration: " + str(machine['name']) + "; ID # " + str(EditedConfig['id']))
        # dump config to JSON
        machine_file = dumps(machine_file, indent = 4)
        # overwrite the config file
        File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
            machine['name'][:3], machine['name'] + ".json"), 'w')
        # overwrite the config
        File.write(machine_file)
        # close the file
        File.close()
        # update the config Object in runtime memory
        config = getConfigObject(machine, config['id'])
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
            dpg.add_text("Your edits to " + machine['name'] + "'s configuration\n"
                + "ID # " + str(config['id']) + " have been saved.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewConfig, user_data = [model, machine, config])

# add a new configuration to the mappings files
def commitConfigAdd(sender, app_data, user_data):
    """commitConfigAdd(user_data = [continueCode, model, machine, config_id, 
        model_info_checks, machine_measurement_checks, model_info_mappings, machine_meas_mappings])
    
    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning this config's machine
    machine: machine; machine Object owning this config
    config_id: str; new config's ID number
    model_info_checks: [DPG Checkboxes]; selected model base info for config
    machine_measurement_checks: [DPG Checkboxes]; selected machine measurements for config
    model_info_mappings: [DPG Input boxes]; maps for selected model base info 
    machine_meas_mappings: [DPG Input boxes]; maps for selected machine measurements

    Commits an addition of a new mapping configuration to the system environment.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model that owns the config
    model = user_data[1]
    # get the machine that owns the config
    machine = user_data[2]
    # get the config ID
    config_id = dpg.get_value(user_data[3])
    # get the selection information lists
    model_info_checks = user_data[4]
    machine_measurement_checks = user_data[5]
    info_mappings = user_data[6]
    meas_mappings = user_data[7]
    # validate the new config's information
    validation = validateAddConfigInput(model, machine, config_id, 
        model_info_checks, machine_measurement_checks, info_mappings, meas_mappings)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new config object
        showWarningPopup(validation[1]['error'])
    # valid config input
    else:
        # input was valid, continue
        NewConfig = validation[1]
        # get the machine file
        machine_file = openMachineConfiguration(machine['name'])
        # add the new config to the machine object
        machine_file['mappings'].append(NewConfig)
        # fix corrupt character writing
        for curr_mapping in machine_file['mappings']:
            for curr_item in curr_mapping['configuration']:
                curr_item['item'] = curr_item['item'].replace('Ã˜', 'Ø')
                curr_item['item'] = curr_item['item'].replace('Â±', '±')
        # write the machine's information to its file after appending the new mapping
        # timestamp the file
        machine_file = timestamp(machine_file, str(machine['name']) + ".json", 
            "Add Configuration: " + str(machine['name']) + "; ID # " + str(NewConfig['id']))
        # reformat the machine_file text into JSON
        machine_file = dumps(machine_file, indent = 4)
        # open the machine's file
        File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
            str(model['model_name']), str(machine['name']) + ".json"), 'w')
        # write to the file
        File.write(machine_file)
        # close the machine file
        File.close()
        # update the config Object in runtime memory
        config = getConfigObject(machine, NewConfig['id'])
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
                + "\nfor " + machine['name'] + " has been added.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewConfig, user_data = [model, machine, config])

# duplicates a config in the mapping configurations file
def commitConfigDuplicate(sender, app_data, user_data):
    """commitConfigDuplicate(user_data = [continueCode, model, machine, config, ConfigID])
    
    continueCode: str; continue code correspdonding to the action being performed.
    model: model; the model owning the duplicated config.
    machine: machine; the machine owning the duplicated config.
    config: config; config Object to be duplicated.
    ConfigID: DPG Inputbox; Item holding the duplicate config's ID

    Commits the duplication of a mapping configuration in the system environment
    """
    # get continue code
    continueCode = user_data[0]
    # get the model
    model = user_data[1]
    # get the machine
    machine = user_data[2]
    # get the duplicated config
    config = user_data[3]
    # get the ID
    ConfigID = dpg.get_value(user_data[4])
    # get the machine file
    machine_file = openMachineConfiguration(machine['name'])
    # validate the config's ID
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
        # get the machine's config list
        machine_configs = machine_file['mappings']
        # check that it is unique
        for config in machine_configs:
            # if the config IDs match
            if config['id'] == ConfigID:
                # overlapping IDs, not unique
                showWarningPopup("Mapping Configuration IDs must be unique.\n"
                    + "The ID " + ConfigID + " has already been assigned.\n"
                    + "Choose a different Mapping Configuration ID for this new Configuration.")
                # destroy the popup
                clearWindow("duplicateConfigPopup")
                return
    # ID is acceptable, duplicate the config
    temp = config
    DuplicateConfig = temp
    # set the duplicate config's ID
    DuplicateConfig.update(id = ConfigID)
    # add the new config to the machine object
    machine_file['mappings'].append(DuplicateConfig)
    # fix corrupt character writing
    for curr_mapping in machine_file['mappings']:
        for curr_item in curr_mapping['configuration']:
            curr_item['item'] = curr_item['item'].replace('Ã˜', 'Ø')
            curr_item['item'] = curr_item['item'].replace('Â±', '±')
    # write the machine's information to its file after appending the new mapping
    # timestamp the file
    machine_file = timestamp(machine_file, str(machine['name']) + ".json", 
        "Duplicate Configuration: " + str(machine['name']) + "; ID # " + str(DuplicateConfig['id']))
    # reformat the machine_file text into JSON
    machine_file = dumps(machine_file, indent = 4)
    # open the machine's file
    File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
        model['model_name'], machine['name'] + ".json"), 'w')
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
            + "\nfor " + machine['name'] + " has been created.")
        # add an Okay button
        dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
            callback = viewConfig, user_data = [model, machine, config])

# removes a config from the mapping configurations file
def commitConfigRemove(sender, app_data, user_data):
    """commitConfigRemove(user_data = [continueCode, model, machine, config])
    
    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning this config's machine
    machine: machine; machine Object owning this config
    config: config; config Object to be removed

    Commits the removal of a mapping configuration from the system environment.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model Object owning this config
    model = user_data[1]
    # get the machine Object to be removed
    machine = user_data[2]
    # get the removed config
    config = user_data[3]
    # get the machine file
    machine_file = openMachineConfiguration(machine['name'])
    # initialize a list index
    index = 0
    # find the config in the list
    for curr_mapping in machine_file['mappings']:
        # if the names match
        if curr_mapping['id'] == config['id']:
            # remove that config from the list
            machine_file['mappings'].remove(config)
            # break the loop
            break
        # increment the index
        index += 1
    # timestamp the file
    machine_file = timestamp(machine_file, str(machine['name']) + ".json", 
        "Remove Configuration: " + str(machine['name']) + "; ID # " + str(config['id']))
    # convert the new config to json
    machine_file = dumps(machine_file, indent = 4)
    # open the machine config file
    File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
        model['model_name'], machine['name'] + ".json"), 'w')
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
        dpg.add_text("Your mapping configuration ID # " + config['id'] 
            + "\nfor " + machine['name'] + " has been removed.")
        # add an Okay button
        dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
            callback = selectModel, user_data = ["removeConfig"])

# add config flow
def addConfig(sender, app_data, user_data):
    """
    addConfig(user_data = [continueCode, model, machine])
    
    SelectMachineWindow -> AddConfigWindow

    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    model: model; the model owning the machine that is being added to.
    machine: machine; the machine owning the new config.
    
    Invokes the UI flow from the SelectMachineWindow to the AddConfigWindow.
    Invoked by the menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model Object owning this config
    model = getModelObject(user_data[1])
    # get the machine Object to be removed
    machine = getMachineObject(user_data[2])
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
        dpg.add_text("Machine Name: " + machine['name'], pos = [75, 200])
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
        for curr_info in model['model_base_information']:
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
        for meas in machine['measurements']:
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
            user_data = ["viewConfig", model, machine, NewConfigID, info_checkboxes, measurement_checkboxes, 
            info_mappings, measurement_mappings], pos = [50, 620],
            width = 300)

# remove config flow
def removeConfig(sender, app_data, user_data):
    """removeConfig(user_data = [continueCode, model, machine, config])

    ViewConfigWindow -> RemoveConfigWindow

    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    model: model; the model owning the machine that is being removed from.
    machine: machine; the machine owning the removed config.
    config: config; the config being removed.
    
    Invokes the UI flow from the ViewConfigWindow to the RemoveConfigWindow.
    Invoked by the selection of "Remove config" in ViewConfigWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model
    model = user_data[1]
    # get machine 
    machine = user_data[2]
    # get the config from the selected ID
    config = getConfigObject(machine, user_data[3])
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
        dpg.add_text("Confirm permanent removal of " + str(config) + "?", color = [255, 0, 50])
        # add a Cancel button
        dpg.add_button(label = "Cancel", pos = [10, 150], width = 180, height = 25,
            callback = deleteItem, user_data = ["removeConfig"])
        # add a Delete button
        dpg.add_button(label = "Delete", pos = [200, 150], width = 180, height = 25,
            callback = commitConfigRemove, user_data = ["removeConfig", model, machine, config])

# edit config flow
def editConfig(sender, app_data, user_data):
    """editConfig(user_data = [continueCode, model, machine, config])

    ViewConfigWindow -> EditConfigWindow

    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    model: model; the model owning the machine that is being edited.
    machine: machine; the machine owning the edited config.
    config: config; the config being edited.
    
    Invokes the UI flow from the ViewConfigWindow to the EditConfigWindow.
    Invoked by the selection of "Edit config" in ViewConfigWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model
    model = user_data[1]
    # get machine 
    machine = user_data[2]
    # get the config from the selected ID
    config = getConfigObject(machine, user_data[3])
    # set the prior_id value before edits made
    prior_id = config['id']
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
        dpg.add_text("Configuration ID #:\n\nfor " + machine['name'], pos = [75, 100])
        # add an input box to allow editing of ID
        IDInput = dpg.add_input_text(pos = [210, 100], width = 100, default_value = config['id'],
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
        for curr_map in config['configuration']:
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
            ["editConfig", model, machine, config, IDInput, prior_id, checks, inputs])

# duplicate config flow
def duplicateConfig(sender, app_data, user_data):
    """duplicateConfig(user_data = [continueCode, model, machine, config])
    
    ViewConfigWindow -> DuplicateConfigWindow

    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    model: model; the model owning the config that is being duplicated.
    machine: machine; the machine owning the duplicated config.
    config: config; the config being duplicated.

    Invokes the UI flow from the viewConfigWindow to the duplicateConfigWindow.
    Invoked by clicking the Duplicate this config button on the viewConfigWindow
    """
    # get continue code
    continueCode = user_data[0]
    # get the model
    model = user_data[1]
    # get the machine
    machine = user_data[2]
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
            ["duplicateConfig", model, machine, DuplicatedConfig, IDInput])
        # add a cancel button
        dpg.add_button(label = "Cancel", pos = [200, 100], 
            callback = deleteItem, user_data = ["duplicateConfigPopup"])

# view config flow
def viewConfig(sender, app_data, user_data):
    """viewConfig(user_data = [model, machine, config])

    SelectConfigWindow -> ViewConfigWindow

    model: model; the model owning the machine that is being viewed.
    machine: machine; the machine owning the viewed config.
    config: config; the config being viewed.
    
    Invokes the UI flow from the SelectConfigWindow to the ViewConfigWindow.
    Invoked by the selection of a config or the menu bar.
    """
    # get the model
    model = user_data[0]
    # get machine 
    machine = user_data[1]
    # get the config from the selected ID
    config = dynamicGetConfig(user_data[2], machine)
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
        dpg.add_text("Configuration ID #: " + str(config.id_num) + "\nfor " + machine.name, 
            pos = [75, 100])
        # add a mapping list
        dpg.add_text("Cluster Mappings:", pos = [75, 200])
        # set a positional offset
        pos_offset = 1
        # for each mapping in the list
        for curr_mapping in config.mappings:
            # add a text item for that field
            dpg.add_text("-   " + str(curr_mapping['item']) + "; sheet #" + str(curr_mapping['sheet']) 
                + "; cluster #" + str(curr_mapping['cluster']), pos = [80, 200 + (pos_offset * 25)])
            # increment positional offset
            pos_offset += 1
        # add config Actions side panel
        dpg.add_text("Configuration Actions:", pos = [800, 200])
        # add action buttons
        dpg.add_button(label = "Edit this Configuration       ->", pos = [800, 225],
            callback = editConfig, user_data = ["editConfig", model, machine, config])
        dpg.add_button(label = "Remove this Configuration     !!", pos = [800, 250],
            callback = removeConfig, user_data = ["removeConfig", model, machine, config])
        dpg.add_button(label = "Duplicate this Configuration  ->", pos = [800, 275],
            callback = duplicateConfig, user_data = ["duplicateConfig", model, machine, config])

# select config flow
def selectConfig(sender, app_data, user_data):
    """selectConfig(user_data = [continueCode, model, machine])

    StartupWindow -> SelectConfigWindow
    
    continueCode: str; the continue code that dictates the next window to open;
        the current action flow of the program.
    model: model; the model owning the machine that is being selected from.
    machine: machine; the machine being selected from.

    Invokes the UI flow from the StartupWindow to the SelectConfigWindow.
    Invoked by the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get model
    model = user_data[1]
    # get machine
    machine = user_data[2]
    # find the actual machine object
    machine = dynamicGetMachine(machine, model)
    # clear windows
    clearWindowRegistry(["selectModelWindow", "selectMachineWindow"])
    # create a SelectMapping window
    SelectConfigWindow = dpg.window(tag = "selectConfigWindow", pos = [900, 18], width = 500, height = 702, 
        no_move = True, no_close = True, no_collapse = True, no_title_bar = True, no_resize = True)
    # add items to the new window
    with SelectConfigWindow:
        # mapping listbox (hidden at first)
        list_items = []
        # create a configs list
        for i in range(len(machine.mapping_configurations)):
            # add the config id to the list
            list_items.append(machine.mapping_configurations[i].id_num)
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
            dpg.set_item_user_data(SelectConfigButton, [model, machine, ConfigListbox])
            

## MACHINE UI CALLBACKS
#__________________________________________________________________________________________________
# makes an edit to a machine in the KIM Interface configuration file
def commitMachineEdits(sender, app_data, user_data):
    """commitMachineEdits(user_data = [continueCode, model, machine, 
        new_name, prior_name, checks, inputs])
    
    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning the edited machine.
    machine: machine; machine Object being edited.
    new_name: DPG item; Input box holding the edited name of the machine.
    prior_name: str; Name of the machine before edits.
    checks: [DPG Check Boxes]; list of edited selected machine measurements.
    inputs: [DPG Input Boxes]; list of edited selected machine measurements maps.

    Takes a machine with edits and overwrites that machine in the config."""
    # get continue code
    continueCode = user_data[0]
    # get model
    model = user_data[1]
    # get machine
    machine = getMachineObject(user_data[2])
    # get the new machine name
    new_name = user_data[3]
    # get the name prior to editing
    prior_name = user_data[4]
    # get the edited machine information
    checks = user_data[5]
    inputs = user_data[6]
    # validate the passed machine information
    validation = validateEditMachineInput(model, machine, new_name, prior_name, checks, inputs)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the edited machine object
        showWarningPopup(validation[1]['error'])
    # edits were valid
    else:
        # update the machine
        EditedMachine = validation[1]
        # reflect edits to measurement fields in configs
        File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
            model['model_name'], machine['name'] + ".json"), 'r')
        # read the file contents
        machine_file = File.read()
        # close the machine file
        File.close()
        # format the machine file as JSON
        machine_file = loads(machine_file)
        # create a list to hold the removed measurements
        removed_meas = []
        # calculate removed measurements
        for meas in machine['measurements']:
            # if this measurement isnt in the EditedMachine's list
            if meas not in EditedMachine['measurements']:
                # add the measurement to the removed list
                removed_meas.append(meas)
        # for each config in the machine file
        for config in machine_file['mappings']:
            # create a list to store removed mapping items
            removed_items = []
            # for each mapped Item in the Configuration
            for i in range(len(config['configuration'])):
                # if the current item in the mapped item list was removed
                if config['configuration'][i]['item'] in removed_meas:
                    # add this index value to the removed list
                    removed_items.append(i)
            # reverse the list of removed indexes (remove from right to left (large to small index))
            removed_items.reverse()
            # for each index needing removed
            for index in removed_items:
                # remove that item by index
                config['configuration'].pop(index)
        # update the machine's name
        machine_file['machine'] = EditedMachine['name']
        # timestamp the file
        machine_file = timestamp(machine_file, str(EditedMachine['name']) + ".json", 
            "Edit Machine: " + str(EditedMachine['name']))
        # format the new machine file text as JSON
        machine_file = dumps(machine_file, indent = 4)
        # overwrite the machine file
        File = open(os.path.join(sys_env_dir, "config", "mapping configurations", 
            model['model_name'], machine['name'] + ".json"), 'w')
        # write the new JSON to the file
        File.write(machine_file)
        # close the machine file
        File.close()
        # get the KIM Interface config file 
        Interface_Config_File = openConfigFile()
        # get the index of the machine in the machine list
        machines = getMachines()
        # get the index from the list
        machine_index = machines.index(machine)
        # update that machine's measurement list
        Interface_Config_File['machines'][machine_index] = EditedMachine
        # get a list of Models
        models = getModels()
        # find the model's index in the model list
        model_index = models.index(model)
        # find the machine index in the model's machine list
        machine_index = model['model_machines'].index(machine['name'])
        # update the machine's name in the model's Machines list
        model['model_machines'][machine_index] = EditedMachine['name']
        # update the model in the config file
        Interface_Config_File['models'][model_index] = model
        # overwrite the KIM Interface config file
        overwriteConfigFile(Interface_Config_File, "Edit Machine: " + str(EditedMachine['name']))
        # set the machine file directory with the old machine name
        old_machine_file = os.path.join(
            sys_env_dir, "config", "mapping configurations", 
            model['model_name'], machine['name'] + ".json")
        # set the machine file directory with the new machine name
        new_machine_file = os.path.join(
            sys_env_dir, "config", "mapping configurations", 
            model['model_name'], EditedMachine['name'] + ".json")
        # update the model's folder in config folder
        os.rename(old_machine_file, new_machine_file)
        # update the model and machine objects in runtime 
        model = getModelObject(model['model_name'])
        machine = getMachineObject(EditedMachine['name'])
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
            dpg.add_text("Your edits to " + machine['name'] + "\nhave been saved.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewMachine, user_data = [model, machine])

# adds a new machine to the KIM Interface configuration file
def commitMachineAdd(sender, app_data, user_data):
    """commitMachineAdd(user_data = continueCode, model, machine_name, measurements_list)
    
    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning the added machine.
    machine_name: DPG item; Input box holding the name of the new machine.
    measurements_list: [DPG Input Boxes]; list of entered machine measurements.

    Adds a new machine to a model in the KIM Interface config."""
    # get continue code
    continueCode = user_data[0]
    # get model
    model = user_data[1]
    # get new machine name
    machine_name = dpg.get_value(user_data[2])
    # get the measurements for this machine
    measurements_list = user_data[3]
    # validate the new machine input
    validation = validateAddMachineInput(model, machine_name, measurements_list)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new config object
        showWarningPopup(validation[1]['error'])
    # valid config input
    else:
        # format the new machine information
        NewMachine = validation[1]
        # open KIM Interface config
        Interface_Config_File = openConfigFile()
        # add the new machine to the machines list
        Interface_Config_File['machines'].append(NewMachine)
        # get the index of the machine's model in KIM Interface config
        model_index = Interface_Config_File['models'].index(model)
        # add the new machine to its model
        Interface_Config_File['models'][model_index]['model_machines'].append(NewMachine['name'])
        # overwrite the KIM Interface config file
        overwriteConfigFile(Interface_Config_File, "Add Machine: " + str(NewMachine['name']))
        # create a default config for the new machine (ID# 1)
        # convert machine information to JSON
        machine_config = {"timestamp":str(str(datetime.now()) + " | " + str(user)), "machine":NewMachine["name"], 
            "mappings":[{"id":"1", "configuration":[]}]}
        # add each model base info to the default mapping
        for info in model['model_base_information']:
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
            model['model_name'], NewMachine['name'] + ".json"), 'x')
        # write the machine info into the file
        File.write(machine_config)
        # close the file
        File.close()
        # update the model and machine objects in runtime 
        model = getModelObject(model['model_name'])
        machine = getMachineObject(NewMachine['name'])
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
            dpg.add_text("Your new machine " + machine['name'] 
                + "\nfor " + model['model_name'] + " has been added.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewMachine, user_data = [model, machine])

# removes a machine from the KIM Interface configuration file
def commitMachineRemove(sender, app_data, user_data):
    """commitMachineRemove(user_data = continueCode, model, machine)
    
    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning the removed machine.
    machine: machine; machine being removed.

    Removes a machine from a model in the KIM Interface config."""
    # get continue code
    continueCode = user_data[0]
    # get model
    model = user_data[1]
    # get machine
    machine = user_data[2]
    # get the KIM Interface config file
    Interface_Config_File = openConfigFile()
    # remove the machine from the KIM Interface config['machines'] list
    Interface_Config_File['machines'].remove(machine)
    # update the model in the KIM Interface config file
    # get the index of the model in the model list
    model_index = Interface_Config_File['models'].index(model)
    # update that model's machine list
    Interface_Config_File['models'][model_index]['model_machines'].remove(machine['name'])
    # overwrite the KIM Interface config file
    overwriteConfigFile(Interface_Config_File, "Remove Machine: " + str(machine['name']))
    # remove machine file in model folder in mapping configurations
    os.remove(os.path.join(sys_env_dir, "config", "mapping configurations", 
        model['model_name'], machine['name'] + ".json"))
    # update the model object in runtime 
    model = getModelObject(model['model_name'])
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
        dpg.add_text("Your machine " + machine['name'] 
            + "\nhas been removed.")
        # add an Okay button
        dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
            callback = selectModel, user_data = ["removeMachine"])

# updates the edit machine measurements subwindow
def editMachineSubwindow(sender, app_data, user_data):
    """editMachineSubwindow(user_data = [continueCode, model, machine, checks, inputs])

    Subwindow segment of the EditMachineWindow

    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning the added machine.
    machine: machine; machine being edited.
    checks: [DPG Check Boxes]; list of edited selected machine measurements.
    inputs: [DPG Input Boxes]; list of edited selected machine measurements maps.
    
    Allows for dynamic addition of model Base Information
    """
    # get continue code
    continueCode = user_data[0]
    # get the model owning the edited machine
    model = user_data[1]
    # get the selected machine
    machine = user_data[2]
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
        for meas in machine['measurements']:
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
        dpg.set_item_user_data("addMeasurementButton", [model, machine, checks, inputs])
        # add informational text
        dpg.add_text("! - De-selecting an existing Measurement Field will\n" 
                    + "    remove it from the Machine's list and ALL the Machine's\n"
                    + "    configurations. This should be avoided, if possible.", 
                    pos = [400, 25], color = [150, 150, 255])
        # add a Finish Editing button
        dpg.add_button(label = "Finish Editing Machine...", width = 270, pos = [75, 500],
            callback = commitMachineEdits, user_data = 
            ["editMachine", model, machine, "machineNameInput", machine['name'], checks, inputs])

def updateMachineMidEdit(sender, app_data, user_data):
    """updateMachineMidEdit(user_data = [model, machine, new_spec])
    
    model: model; the model owning the machine being edited.
    machine: machine; the machine being edited.
    new_spec: DPG Inputbox; input box containing the title of the new specification.

    Adds a new specification to a machine's list mid-edit and refreshes the edit window.
    """
    # get the model owning the machine
    model = user_data[0]
    # get the machine
    machine = user_data[1]
    # get the new measurement specification
    new_spec = dpg.get_value(user_data[2])
    # get the KIM Interface config file
    Interface_Config_File = openConfigFile()
    # find the machine in KIM Interface config
    machine_index = Interface_Config_File['machines'].index(machine)
    # add a new measurement field to the machine
    machine['measurements'].append(new_spec)
    # update the machine in the KIM Interface config file
    Interface_Config_File['machines'][machine_index] = machine
    # overwrite the KIM Interface config file
    overwriteConfigFile(Interface_Config_File, "Edit Machine: " + str(machine['name']))
    # update the editMachineSubwindow
    editMachineSubwindow(sender = "", app_data = "", 
        user_data = ["editMachine", model, machine, [], []])
    # delete the popup
    deleteItem(sender = "", app_data = "", user_data = ["fieldValuePopup"])

# adds a new measurement to the edited machine
def addMachineMeasurementField(sender, app_data, user_data):
    """addMachineMeasurementField(user_data = [model, machine, checks, inputs])
    
    model: model; the model owning the machine being edited.
    machine: machine; the machine being edited.
    checks: [DPG Check Boxes]; list of edited selected machine measurements.
    inputs: [DPG Input Boxes]; list of edited selected machine measurements maps.

    Prompts the user to enter a new Measurement Specification.
    """
    # get model
    model = user_data[0]
    # get machine
    machine = user_data[1]
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
            callback = updateMachineMidEdit, user_data = [model, machine, NewFieldInput])
        # add a cancel button
        dpg.add_button(label = "Cancel", pos = [165, 100], 
            callback = deleteItem, user_data = ["fieldValuePopup"])

# add machine flow
def addMachine(sender, app_data, user_data):
    """addMachine(user_data = continueCode, model)
    
    SelectModelWindow -> AddMachineWindow

    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning the added machine.
    
    Invokes the UI flow from the SelectModelWindow to the AddMachineWindow.
    Invoked by the menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get the model
    model = getModelObject(user_data[1])
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
        # display the model's existing machines
        for machine in model['model_machines']:
            # add this name to the window
            dpg.add_text(machine, pos = [1000, 200 + (pos_offset * 25)])
            # increment the positional offset
            pos_offset += 1
        # add the Add New machine button
        dpg.add_button(label = "Add new Machine...", width = 270, pos = [50, 600],
            callback = commitMachineAdd, user_data = ["addMachine", model, MachineNameEntry, measurement_entries])

# remove machine flow
def removeMachine(sender, app_data, user_data):
    """removeMachine(user_data = continueCode, model, machine)
    
    ViewMachineWindow -> RemoveMachineWindow
    
    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning the removed machine.
    machine: machine; machine Object being removed.
    
    Invokes the UI flow from the ViewMachineWindow to the RemoveMachineWindow.
    Invoked by the selection of "Remove machine" in ViewMachineWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get model
    model = user_data[1]
    # get machine
    machine = getMachineObject(user_data[2])
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
        dpg.add_text("Confirm permanent removal of " + str(machine) + "?", color = [255, 0, 50])
        # add a Cancel button
        dpg.add_button(label = "Cancel", pos = [10, 150], width = 180, height = 25,
            callback = deleteItem, user_data = ["removeMachine"])
        # add a Delete button
        dpg.add_button(label = "Delete", pos = [200, 150], width = 180, height = 25,
            callback = commitMachineRemove, user_data = ["removeMachine", model, machine])

# edit machine flow
def editMachine(sender, app_data, user_data):
    """editMachine(user_data = continueCode, model, machine)

    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object owning the edited machine.
    machine: machine; machine Object being edited.

    ViewMachineWindow -> EditMachineWindow

    Invokes the UI flow from the ViewMachineWindow to the EditMachineWindow.
    Invoked by the selection of "Edit machine" in ViewMachineWindow;
    and from the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get model
    model = user_data[1]
    # get machine
    machine = getMachineObject(user_data[2])
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
            width = 200, default_value = machine['name'])
        # open the editMachineSubwindow
        editMachineSubwindow(sender = "", app_data = "", 
            user_data = ["editMachine", model, machine, [], []])

# view machine flow
def viewMachine(sender, app_data, user_data):
    """viewMachine(user_data = model, machine)

    SelectMachineWindow -> ViewMachineWindow
    
    model: model; model Object owning the viewed machine.
    machine: machine; machine Object being viewed.
    
    Invokes the UI flow from the SelectMachineWindow to the ViewMachineWindow.
    Invoked by the selection of a machine or the menu bar.
    """
    # get model
    model = user_data[0]
    # get machine
    machine = dynamicGetMachine(user_data[1], model)
    # clear windows
    clearWindowRegistry()
    # enable the ViewMachineWindow
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
        dpg.add_text("Machine name: " + machine.name, pos = [75, 100])
        # add a measurement list
        dpg.add_text("Machine Measurements:", pos = [75, 200])
        # set a positional offset
        pos_offset = 1
        # for each measurement field in the list
        for meas in machine.measurements:
            # add a text item for that field
            dpg.add_text("-   " + meas, pos = [80, 200 + (pos_offset * 25)])
            # increment positional offset
            pos_offset += 1
        # add machine Actions side panel
        dpg.add_text("Machine Actions:", pos = [800, 200])
        # add action buttons
        dpg.add_button(label = "Edit this Machine                   ->", pos = [800, 225],
            callback = editMachine, user_data = ["editMachine", model, machine])
        dpg.add_button(label = "Remove this Machine                 !!", pos = [800, 250],
            callback = removeMachine, user_data = ["removeMachine", model, machine])
        dpg.add_button(label = "Add a Configuration to this Machine ->", pos = [800, 275],
            callback = addConfig, user_data = ["addConfig", model, machine])

# select machine flow
def selectMachine(sender, app_data, user_data):
    """selectMachine(user_data = continueCode, model)

    continueCode: str; continue code correspdonding to the action being performed.
    model: model; model Object being selected from.

    StartupWindow -> SelectMachineWindow
    
    Invokes the UI flow from the StartupWindow to the SelectMachineWindow.
    Invoked by the main menu bar.
    """
    # get continue code
    continueCode = user_data[0]
    # get model & models list
    model = user_data[1]
    # find the actual model object
    model = dynamicGetModel(model)
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
        for machine in model.machines:
            # add it to the list
            list_items.append(machine.name)
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
                dpg.set_item_user_data(MachineListbox, [continueCode, model, MachineListbox])
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
                dpg.set_item_user_data(SelectMachineButton, [model, MachineListbox])          


## MODEL UI CALLBACKS
#__________________________________________________________________________________________________
# makes an edit to a model in the KIM Interface config file
def commitModelEdits(sender, app_data, user_data):
    """
    commitModelEdits(user_data = model, new_name, prior_name, 
        base_info_checks, base_info_inputs)

    model: model; model being edited.
    new_name: DPG Input Box; DPG Item holding the edited model name.
    prior_name: str; the model name before edits.
    base_info_checks: [DPG Checkboxes]; Checkboxes indicating the selected base
        information to include after edits.
    base_info_inputs: [DPG Input boxes]; Input boxes holding the edited base information
        headers.

    Takes a model with edits and overwrites that model in the KIM Interface config."""
    # get model
    model = user_data[0]
    # get the edited model name
    new_name = dpg.get_value(user_data[1])
    # get the model name prior to edits
    prior_name = user_data[2]
    # get the selected model information fields
    checks = user_data[3]
    # get the base information header inputs
    inputs = user_data[4]
    # validate the edited model input
    validation = validateEditModelInput(model, new_name, prior_name, checks, inputs)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new model object
        showWarningPopup(validation[1]['error'])
    # valid model input
    else:
        # input was valid, continue
        edited_model = validation[1]
        # open the KIM Interface config file
        Interface_Config_File = openConfigFile()
        # if the model name has been changed
        if edited_model.name != model.name:
            # update the machine names in the model machine list
            for machine in edited_model:
                # change the first three characters to match the new model name
                machine.name = edited_model.name + machine.name[3:]
        # find the unedited model in the config file
        model_index = Interface_Config_File['models'].index(Model.modelToDict(model))
        # put the edited model in KIM Interface config
        Interface_Config_File['models'][model_index] = Model.modelToDict(edited_model)
        # overwrite the KIM Interface config file
        overwriteConfigFile(Interface_Config_File, "Edit Model: " + str(edited_model.name))
        # update the model object in runtime memory
        model = edited_model
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
            dpg.add_text("Your edits to " + model.name + "\nhave been saved.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewModel, user_data = [model])

# adds a new model to the KIM Interface config
def commitModelAdd(sender, app_data, user_data):
    """
    commitModelAdd(user_data = model_name, model_base_info)

    model_name: DPG Input Box; DPG Item holding the new model name.
    model_base_info: [DPG Input boxes]; Input boxes holding the new model 
        base information headers.

    Adds a new model in the KIM Interface config."""
    # get model name
    model_name = dpg.get_value(user_data[0])
    # get the base information list
    model_base_info = user_data[1]
    # validate the new model input
    validation = validateAddModelInput(model_name, model_base_info)
    # check that it was valid
    if not validation[0]:
        # DO NOT accept the new model object
        showWarningPopup(validation[1]['error'])
    # valid model input
    else:
        # input was valid, continue
        new_model = validation[1]
        # add the new model to the KIM Interface config file (open KIM Interface config)
        Interface_Config_File = openConfigFile()
        # add the new model to the models list
        Interface_Config_File['models'].append(Model.modelToDict(new_model))
        # overwrite the KIM Interface config file
        overwriteConfigFile(Interface_Config_File, "Add Model: " + new_model.name)
        # update model object in runtime memory
        model = new_model
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
            dpg.add_text("Your new model " + str(model) + " has been added.")
            # add an Okay button
            dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
                callback = viewModel, user_data = [model])

# removes a model from the KIM Interface configuration file
def commitModelRemove(sender, app_data, user_data):
    """
    commitModelRemove(user_data = model)

    model: model; model being removed.

    Removes a model in the KIM Interface config."""
    # get the removed model
    model = user_data[0]
    # get the KIM Interface config file
    Interface_Config_File = openConfigFile()
    # remove that model from the list
    Interface_Config_File['models'].remove(Model.modelToDict(model))
    # overwrite the KIM Interface config file
    overwriteConfigFile(Interface_Config_File, "Remove Model: " + model.name)
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
        dpg.add_text("The " + str(model) + " has been removed.")
        # add an Okay button
        dpg.add_button(label = "Okay!", pos = [125, 100], width = 150, height = 25,
            callback = selectModel, user_data = ["removeModel"])

# update the edit model information subwindow
def editModelSubwindow(sender, app_data, user_data):
    """updateEditModelSubwindow(user_data = [model, checks, inputs])

    Subwindow segment of the EditModelWindow

    model: model; model being edited.
    checks: [DPG Check Boxes]; list of edited selected model information headers.
    inputs: [DPG Input Boxes]; list of edited selected model information header maps.

    Allows for dynamic addition of model Base Information
    """
    # get the selected model
    model = user_data[0]
    # get the current checks list
    checks = user_data[1]
    # get the current inputs list
    inputs = user_data[2]
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
        for info in model.base_information:
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
        dpg.set_item_user_data("addBaseInfoButton", [model, checks, inputs])
        # add informational text
        dpg.add_text("! - De-selecting an existing Base Information Field will\n" 
                    + "    remove it from the Model's list and ALL the Model's\n"
                    + "    Machine lists. This should be avoided, if possible.", 
                    pos = [400, 50], color = [150, 150, 255])
        # add a Finish Editing button
        dpg.add_button(label = "Finish Editing Model...", width = 270, pos = [75, 500],
            callback = commitModelEdits, user_data = [model, "modelNameInput",
                model.name, base_info_checks, base_info_inputs])

def updateModelMidEdit(sender, app_data, user_data):
    """updateModelMidEdit(user_data = [model, new_base_info])
    
    model: model; the model being edited.
    new_base_info: DPG Inputbox; input box containing the title of the new base information.

    Adds a new base information field to a model's list mid-edit and refreshes the edit window.
    """
    # get the model
    model = user_data[0]
    # add the new base information header to the model
    model.base_information.append(dpg.get_value(user_data[1]))
    # convert the model to a dict
    model_json = Model.modelToDict(model)
    # get the KIM Interface config file
    Interface_Config_File = openConfigFile()
    # find the model in the config file
    for i in range(len(Interface_Config_File['models'])):
        # save the current model
        curr_model = Interface_Config_File['models'][i]
        # if the model names match
        if curr_model['name'] == model.name:
            # save the new model here
            Interface_Config_File['models'][i] = model_json
    # overwrite the KIM Interface config file
    overwriteConfigFile(Interface_Config_File, "Edit Model: " + model.name)
    # update the editModelSubwindow
    editModelSubwindow(sender = "", app_data = "", user_data = [model, [], []])
    # delete the popup
    deleteItem(sender = "", app_data = "", user_data = ["fieldValuePopup"])

# adds a new model base info field
def addModelInfoField(sender, app_data, user_data):
    """addBaseInfoField(user_data = [model checks, inputs])
    
    model: model; model being edited.
    checks: [DPG Check Boxes]; list of edited selected model information headers.
    inputs: [DPG Input Boxes]; list of edited selected model information header maps.

    Adds a new blank base information field to the model while editing
    """
    # get the model
    model = user_data[0]
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
            callback = updateModelMidEdit, user_data = [model, NewFieldInput])
        # add a cancel button
        dpg.add_button(label = "Cancel", pos = [200, 100], 
            callback = deleteItem, user_data = ["fieldValuePopup"])

# add model flow
def addModel(sender, app_data, user_data):
    """addModel(user_data = [])

    StartupWindow -> AddModelWindow

    Invokes the UI flow from the StartupWindow to the AddModelWindow.
    Invoked by the menu bar.
    """
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
            + "-  Each Model has a set of base information;\n"
            + "   this base information is added to each Machine.\n"
            + "-  Model names must be unique.", pos = [75, 100])
        # enter model name label
        dpg.add_text("Enter the new Model name:", pos = [75, 200])
        # model name entry box
        ModelNameEntry = dpg.add_input_text(width = 200, pos = [75, 225], hint = "Model name...")
        # add base information setting panel
        # add base info panel label
        dpg.add_text("Enter Model base information (non-measurement column headers):", pos = [400, 200])
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
        models = getModels(get_machines = False, get_configs = False)
        # for each model in KIM Interface config
        for curr_model in models:
            # add this name to the window
            dpg.add_text(str(curr_model.name), pos = [1000, 200 + (pos_offset * 25)])
            # increment the positional offset
            pos_offset += 1
        # add the Add New model button
        dpg.add_button(label = "Add new Model...", width = 270, pos = [50, 600],
            callback = commitModelAdd, user_data = [ModelNameEntry, base_information_entries])

# remove model flow
def removeModel(sender, app_data, user_data):
    """removeModel(user_data = continueCode, model)

    model: model; model being removed.

    ViewModelWindow -> RemoveModelWindow
    
    Invokes the UI flow from the ViewModelWindow to the RemoveModelWindow.
    Invoked by the selection of "Remove model" in ViewModelWindow;
    and from the main menu bar.
    """
    # get information from call
    #debug
    print("Model input before getting model: " + str(user_data[0]) + " with type " + str(type(user_data[0])))
    model = dynamicGetModel(user_data[0])
    #debug
    print("Model after getting model: " + str(model) + " with type " + str(type(model)))
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
        dpg.add_text("Confirm permanent removal of " + str(model) + "?", color = [255, 0, 50])
        # add a Cancel button
        dpg.add_button(label = "Cancel", pos = [10, 150], width = 180, height = 25,
            callback = deleteItem, user_data = ["removeModel"])
        # add a Delete button
        dpg.add_button(label = "Delete", pos = [200, 150], width = 180, height = 25,
            callback = commitModelRemove, user_data = [model])

# edit model flow
def editModel(sender, app_data, user_data):
    """editModel(user_data = model)

    model: model; model being edited.
    
    ViewModelWindow -> EditModelWindow

    Invokes the UI flow from the ViewModelWindow to the EditModelWindow.
    Invoked by the selection of "Edit model" in ViewModelWindow;
    and from the main menu bar.
    """
    # get the selected model
    model = dynamicGetModel(user_data[0])
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
            default_value = model.name)
    # open the subwindow
    editModelSubwindow(sender, app_data, user_data = [model, [], []])

# view model flow
def viewModel(sender, app_data, user_data):
    """viewModel(user_data = model)

    model: model; model being viewed.

    SelectModelWindow -> ViewModelWindow
    
    Invokes the UI flow from the SelectModelWindow to the ViewModelWindow.
    Invoked by the selection of a model or the menu bar.
    """
    # get info from user data
    model = dynamicGetModel(user_data[0])
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
        dpg.add_text("Model name: " + model.name, pos = [75, 100])
        # add a base information list
        dpg.add_text("Model Base Information:", pos = [75, 200])
        # set a positional offset
        pos_offset = 1
        # for each field in the base info list
        for i in range(len(model.base_information)):
            # add a text item for that field
            dpg.add_text("-   " + model.base_information[i], pos = [80, 200 + (pos_offset * 25)])
            # increment positional offset
            pos_offset += 1
        # add a machine list
        dpg.add_text("Model Machines:", pos = [400, 200])
        # set a positional offset
        pos_offset = 1
        # for each machine in the machine list
        for i in range(len(model.machines)):
            # add a text item for that machine
            dpg.add_text("-   " + model.machines[i].name, pos = [400, 200 + (pos_offset * 25)])
            # increment positional offset
            pos_offset += 1
        # add model Actions side panel
        dpg.add_text("Model Actions:", pos = [800, 200])
        # add action buttons
        dpg.add_button(label = "Edit this Model             ->", pos = [800, 225],
            callback = editModel, user_data = [model])
        dpg.add_button(label = "Remove this Model           !!", pos = [800, 250],
            callback = removeModel, user_data = [model])
        dpg.add_button(label = "Add a Machine to this Model ->", pos = [800, 275],
            callback = addMachine, user_data = ["addMachine", model])

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
        dpg.add_button(label = "<- Main Menu / Select...",
            callback = returnToStartup, pos = [10, 25])
        # add select model label (always visible)
        dpg.add_text("Select a Model:", pos = [75, 50])
        # pull models from KIM Interface config
        models = getModels(get_machines = True, get_configs = True)
        # create a name list
        list_items = []
        # for each model in KIM Interface config
        for model in models:
            # add the name to the list
            list_items.append(model.name)
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
                dpg.set_item_user_data(SelectModelButton, [ModelListbox])


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
    # check that a machine is selected
    if not machine_name == "Default":
        # add the machine_name to the url, replacing spaces with underscore for URL format
        url += "machine_name=" + str(machine_name.replace(' ', '_'))
        # check that a mapping configuration is selected
        if not mapping_config == "Default":
            # add the current mapping_config to the url
            url += "&mapping_config=" + mapping_config
        # else reset the url and warn the user to select a config
        else:
            # show a warning Popup
            showWarningPopup("Please select a Mapping Configuration to generate a URL.")
            # clear the url value
            url = ""
    # else reset the url and warn the user to select a machine
    else:
        # show a warning Popup
        showWarningPopup("Please select a Machine to generate a URL.")
        # clear the url value
        url = ""
    # update the url box
    dpg.set_value(URLBox, url)

# updates the selected mapping configuration
def updateSelectedMapping(sender, app_data, user_data):
    """updateSelectedMapping(user_data = [ConfigurationListbox, MappingConfigText])
    
    ConfigurationListbox: DPG Listbox; Listbox holding the selected config.
    MachineNameText: DPG Text; Item holding the current selected mapping_config.

    Updates the selected mapping config with the current selection in the Configurations listbox.
    """
    # get the current value of the machine Listbox
    machine_name = dpg.get_value(user_data[0])
    # set the machine text value
    dpg.set_value(user_data[1], machine_name)

# updates the mapping configuration selection Listbox items
def updateMappingConfigurationList(sender, app_data, user_data):
    """updateMappingConfigurationList(user_data = [ConfigurationListbox, config_list])
    
    ConfigurationListbox: DPG Listbox; Listbox holding the selected config.
    config_list: [configuration id]; list of configuration ids from the selected machine.

    Updates the list of configs to show in the Information window.
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
    
    MachineListbox: DPG Listbox; Listbox holding the selected machine.
    ConfigurationListbox: DPG Listbox; Listbox holding the selected config.
    MachineNameText: DPG Text; Item holding the current selected machine_name.

    Updates the selected machine name with the current selection in the Machines listbox.
    """
    # get the current value of the machine Listbox
    machine_name = dpg.get_value(user_data[0])
    # set the machine text value
    dpg.set_value(user_data[2], machine_name)
    # get the configuration objects
    models = getModels(get_machines = True, get_configs = True)
    # find the machine in the model list
    for model in models:
        # go through each machine 
        for machine in model.machines:
            # does the machine name match?
            if machine.name == machine_name:
                # save this machine's Configs
                config_list = machine.mapping_configurations
    # update the list to just hold IDs
    for i in range(len(config_list)):
        # set the current index of the list to just the ID
        config_list[i] = config_list[i].id_num
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

    Creates a widget view that shows the machine and configs being requested;
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
        # get the configuration objects (Models & Machines, no configs)
        models = getModels(get_machines = True, get_configs = False)
        # create a machine List
        machine_names = []
        # for each model
        for model in models:
            # for each machine in the model list
            for machine in model.machines:
                # add the model's Machines to the list (name only)
                machine_names.append(machine.name)
        # add machine selection label
        dpg.add_text("Select a Machine:", pos = [400, 150])
        # sort the mapping configuration list
        machine_names = sorted(machine_names, reverse = False)
        # add a listbox to select Machines from
        MachineListbox = dpg.add_listbox(items = machine_names, callback = updateSelectedMachine,
            pos = [400, 175], default_value = None, width = 250, num_items = 20)
        # add config selection label
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
            callback = addModel)
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