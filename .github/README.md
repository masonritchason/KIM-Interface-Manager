# Keyence IM-8001 (KIM) Interface Manager
For YAMADA NORTH AMERICA, INC.
Designed and Developed by Mason Ritchason

## Contribution Guidelines

**KIM Interface is not meant to be openly contributed to.**
This repository exists as a community hub for user support and information.
Contribution is only expected from the original developer, [@masonritchason](https://github.com/masonritchason).
Future contributors from YNA may be added if necessary.

## Requesting Features & Changes

**If you would like to request a change or a new feature:** 
* Submit a [discussion topic](https://github.com/masonritchason/KIM-Interface/discussions/74) if you would like a change or feature;
* Submit an [issue](https://github.com/masonritchason/KIM-Interface/issues) if you believe you have found a bug;
* Submit a [security advisory](https://github.com/masonritchason/KIM-Interface/security/advisories) if you believe there is a security issue.

## Purpose

**What:**
The purpose of the KIM Interface is to bridge the gap between **i-Reporter Forms (Gateway)** and **Keyence IM-8001 lineside machines**. 

**How:**
The software integrates the two systems, allowing YNA to utilize the information collected by Keyence IM-8001 machines quickly and directly.

## Documentation & Support

To improve YNA’s utilization of the KIM Interface software, a large suite of documentation has been created. 
This documentation will help new users learn to navigate, understand, and use the KIM Interface in an efficient, effective way.

>[!TIP]
>Reading `KIM Interface Manager User Manual` is the best way to understand the specifications of >the KIM Interface. The information included will outline each of the functions of the software, including a behind-the-scenes >explanation and a use guide.

Much of this software runs on the backbones of the YNA network. If any issues occur while using this software, please contact the IT Department to verify that the system is configured correctly. If the issue cannot be resolved by the network managers, you may contact Mason Ritchason (via GitHub) for support with the software. For more information on the development and design of the software, contact Mason Ritchason and request access to the software’s private repository. A history of the program’s development and versioning, including issue history, can be accessed from this repository.

>[!NOTE]
>Mason Ritchason – https://github.com/masonritchason

## System Files & Environment:

The KIM Interface is a medium-sized software that involves several components. Many of these components are “back-end” and will not require user interaction. However, these files are still necessary. Manipulation of the system files is highly discouraged; the system environment is configured to function in a specific way, so manually editing the environment will likely cause issues.

>[!IMPORTANT]
>KIM Interface is designed to run from the Gateway Host VM on YNA’s network. Users should operate the KIM Interface from the Gateway Host >to avoid network issues, permissions issues, etc.

The KIM Interface is installed and located at the following directory:

**Host > This PC > System (C:) > Program Files > ConMas Gateway > scripts > KIM Interface**

A KIM Interface Manager shortcut has also been placed on the desktop of the Gateway Host VM. You can quickly access it from there.

### The application folder

- `__pycache__` (folder): A Python dependency folder. Do not manipulate this folder in any way. Doing so can cause issues with Python’s environment, a very difficult issue to fix.
- `bin` (folder): A temporary, ‘garbage bin’ folder. The system utilizes this folder to save temporary files such as converted CSV sheets.
    - `backups`: The KIM Interface Manager holds backups of its configuration. Backups hold the KIM Interface configuration as specified by users. Models, Machines, and Mapping Configurations are included in backups. If the main KIM Interface configuration files are lost, damaged, or corrupted, loading a backup can help recover lost information. To do this, open the backup folder and copy the files KIM_interface_configuration.json and mapping configurations to the config folder inside application.
- `build` (folder): A dependency and system folder that holds integral information for the entire system. Altering this folder in any way will BREAK the software. Please do not interact with this folder or the files inside of it.
- `config` (folder): This file holds the configuration information that the KIM Interface software runs from. It holds Model, Machine, and general configuration information and is crucial to the system. Editing this file is not recommended, especially if the user is not literate in the JSON language syntax. Making changes to this file without understanding how JSON works or how the system formats its own configuration can cause fatal issues, possibly corrupting the entire system’s saved data. The configuration file is built up over time as users add, edit, and remove components of the Keyence IM-8001 machines and the i-Reporter forms that utilize their information. If this file is corrupted, it may mean a complete loss of the system YNA’s associates have built over time.
    - `mapping configurations` (folder): This folder contains the mapping configurations for each link between an i-Reporter form and a machine. The folder is critical to the functionality of the KIM Interface and should not be manipulated.
 
>[!NOTE]
>Each Model added to the KIM Interface system must have a subfolder in the mapping configurations folder. Additionally, all
>Machines must have a .json file in their respective Model subfolder. These folders and files are created by the software
>automatically, but if they are manipulated by the user after creation, issues may occur.

- `logs` (folder): A folder that holds the log information of the software. This folder is one that the user is encouraged to interact with. There are two types of logs held by the system:
    - `output logs` (folder): The output logs folder holds .txt files with dates and times. These .txt files hold the result set for the 50 most recent runs of the software. This folder is limited to a maximum of 50 logs at any given time. When the folder exceeds this number, log files are destroyed from oldest to newest;
    - `runtime_log.txt` (file): A .txt file that logs the runtime and the date/time of each software run. This log file is a compact way to analyze the speed of the software and to see when it is being used. The file is limited to 500 lines and will be trimmed, from oldest to newest, when it exceeds this limit.
    - `changelog.txt` (file): A .txt file that logs every change made in the KIM Interface Configuration. The information is pulled from the KIM Interface Manager and will include the timestamp of the change, the user making the change, the file that was impacted, and a short description of what was done to what virtual object.

>[!TIP]
>This can be used to track changes and further diagnose issues. Users and maintainers of the KIM Interface system can compare the time and date of an occurence to changes in the >`changelog.txt` file, effectively pinpointing the changes that could have created the issue.

- `KIM Interface Manager.exe` (executable; launcher): This file will run the system and MUST NOT be moved from this location. There is a shortcut in the main KIM Interface folder as well as on the Gateway Host VM Desktop. Users may copy those shortcuts.
- `KIM Interface Manager.spec` (executable component): This file instructs the executable when constructing the KIM Interface Manager program. Do not remove this file.
- `KIM_Interface.py` (component): This is the actual interface between the i-Reporter form and the Keyence IM-8001 machines. Interaction with this component is highly discouraged, as changes could completely corrupt the function of the system.
- `KIM_Interface_Manager.py` (component): This is the component that users will interact with. It allows for the manipulation of the KIM Interface configuration (adding/editing/removing Models, Machines, and Configurations for i-Reporter forms). See Chapter IV for more information on the KIM Interface Manager and how to use it.
- `KIM_Interface_Manager_Config.json` (configuration file): A separate configuration file that holds basic version information for the KIM Interface and the KIM Interface Manager.
- `results.txt` (file): This file holds the most recent result produced by the software. Users can interact with this file to see how the system produces and formats its information.

### Virtual Objects

The KIM Interface uses a virtualization of the physical production lines on YNA's floors. To do this, the system works with virtual **Models and Machines** that correspond to the real-world Model production lines and Keyence IM Machines.

#### Models

_‘Model’_ refers to the Model name that corresponds with the Keyence IM-8001 machines on YNA’s production floor. Model names are three characters in length and contain only numbers and capitalized letters. Examples are `3D4`, `TZ3`, and `T4P`. The KIM Interface stores defined Models in its configuration file and each Model ‘owns’ a set of machines. In the KIM Interface environment, Models hold the information for the line they run on. Each Model has a set of `base information` fields that indicate the basic information included on every machine for that Model. These often include `Program Name`, `Judgment`, `Operator`, and fields like that.

#### Machines

_‘Machine’_ refers to the name of the actual Keyence IM-8001 machine on YNA’s production floor. Machine names are prefixed by the Model they belong to and describe the process they measure. Examples are `3D4 HS DIFF OD LATHE 2` and `TZ3 HS SUPPORT ROLL FORM`. The KIM Interface stores defined Machines in its configuration file under ownership of its Model. In the KIM Interface environment, the Machine holds its own measurement information (specs).

#### Mapping Configurations

_‘Mapping Configuration’_ refers to a set of instructions that informs the system on the intended use of the information it collects. They essentially instruct the KIM Interface to send its information to the correct location/cluster on the i-Reporter form. Each Machine stores its Mapping Configurations and the KIM Interface refers to the instructions in each Configuration depending on which one is used. Mapping Configurations hold a `sheet` and `cluster` number ‘map’ for every piece of information that needs to be sent to an i-Reporter form. 

Machines must have a Mapping Configuration for every form that use their measurement information. For a form to populate with information processed by the KIM Interface, Gateway requires that there is a 'mapping' for that information. 'Mappings' essentially indicate two things: the information's name/origin/meaning and the actual value, and where that information needs to go on the i-Reporter form. Each Mapping Configuration has a unique numerical identifier. When you add a configuration, make sure to give each of them a unique identifier. If you use the same ID for multiple mapping configurations, you will likely experience errors. The KIM Interface Manager keeps you from duplicating IDs, but users who manually add Configurations may create duplicates.

## The Interface Itself

The `Interface` component is what connects to the measurement information collected by the Keyence IM-8001 machines. The machines store their measurement information in `CSV` (Excel) sheets on YNA’s network. Every time a lineside associate makes a measurement, that measurement is added to the `CSV` sheet with all the information it produced.

When the `Interface` component runs, it ‘retrieves’ the most recent measurement made by the Machine it is asked to access. It pulls the measurement from the machine’s measurement sheet and sends it directly to the i-Reporter form for mapping and input.

This component also manages the log information that the KIM Interface produces. Log information can be used to fix issues with the connection between an i-Reporter form and a Keyence IM-8001 machine, to see the recent results of the system, or assess the connection and speed of the KIM Interface itself.

The logs are useful in the case of errors on i-Reporter forms. The KIM Interface is designed to return a result set with a specific error code and description, even when results are not successfully generated. The error codes are outlined in the `Administrative Notes (Chapter VII)`. The log files can be accessed by navigating to the `logs` folder (found in the `application` folder).

>[!WARNING]
>Direct user interaction with this component is not possible as there is no UI or input. It is designed to be invoked solely by the i-Reporter form via the Gateway connection.

## Getting Started with KIM Interface

As stated previously, it is highly recommended that users interact with the KIM Interface directly on the `Gateway Host Virtual Machine (VM)`. To gain access to the VM, please contact the IT Department. Once users have access to the Gateway Host VM, they can begin interacting with the KIM Interface system.

The safest, most secure, and easiest way for users to interact with and manipulate the KIM Interface is to use the provided `KIM Interface Manager`. To open the `KIM Interface Manager`, locate the `KIM Interface Manager.exe` file on the `Gateway Host VM` desktop and double-click it.

In the `KIM Interface Manager`, users can manipulate all the information in the KIM Interface, including `Models`, `Machines`, and `Mapping Configurations` for i-Reporter forms. `Chapter IV` gives an in-depth guide for use of the `KIM Interface Manager`. It should be referenced frequently as users learn to manipulate the KIM Interface’s configuration.

>[!NOTE]
>The most common actions users will carry out will be adding, editing, and removing Mapping Configurations. Manipulating Machines and >Models will be uncommon unless YNA changes the Keyence IM-8001 machines used on the production floor (remove, add, update).

>[!IMPORTANT]
>It is highly recommended that users become comfortable with the KIM Interface Manager (via this documentation) before carrying out >large-scale changes to the KIM Interface. Changes are irreversible and repairing damages to the Interface’s configuration may take a >significant amount of work.

## The KIM Interface Manager

Using the `Manager` component of the KIM system is intentionally desinged to be approachable for users who are less familiar with software processes. However, understanding the processes is still highly recommended. To learn how to use the `Manager`, users should read `Chapter IV` of the `KIM Interface Manager User Manual`.

### What is Possible?

The following functions are packaged into the `Manager`:

- Models:
    - Adding Models
    - Viewing Model Information
    - Editing Model Information
    - Removing Models
- Machines:
    - Adding Machines
    - Viewing Machine Measurement Specifications
    - Editing Machine Measurement Specifications
    - Removing Machines
- Mapping Configurations:
    - Adding Mapping Configurations
    - Viewing Mapping Configuration Settings
    - Editing Mapping Configuration Settings
    - Removing Mapping Configurations
    - Duplicating Mapping Configurations
- System Information:
    - Average Runtime (time cost)
    - i-Reporter URL Call Generation
    - Result Viewing
    - Logs Viewing

>[!WARNING]
>Using the KIM Interface Manager without first becoming familiar with the processes will likely create problems. Users should read `Chapter IV` of the `KIM Interface Manager User Manual`.

## Administrative Notes

### Errors and Error Codes

The KIM Interface is fitted with a high level of resilience and error reporting. This facilitates an easier troubleshooting process, as operators can immediately tell what is wrong and who will need to be involved in the repair process. Each possible error case in the KIM Interface environment is coded and given a message. Below is an outline of each of the possible errors:

- `[Error 1] No machine name passed.` This error indicates that there was no machine name included in the `URL` call of the KIM Interface. Users must include a valid Keyence IM-8001 Machine name, as they appear in the `KIM Interface Manager`. See `Chapter VI` to ensure proper configuration of the machine name in the `URL`.
    - This is a **user error**; external assistance is unnecessary.
- `[Error 2] Invalid machine name passed.` This error indicates that the machine name passed to the KIM Interface was not found in the `KIM Interface configuration`. This means that either the machine name contained a typo, or the machine name requested does not exist and needs to be configured in the KIM Interface.
    - This is a **user error**; external assistance is unnecessary.
- `[Error 3] No mapping configuration ID passed.` This error indicates that there was no mapping configuration `ID` number included in the `URL` call of the KIM Interface. Users must include a valid mapping configuration `ID` for that machine as they are configured in the `KIM Interface Manager`.
    - This is a **user error**; external assistance is unnecessary.
- `[Error 4] Invalid mapping configuration ID format.` This error indicates that the mapping configuration `ID` number passed to the KIM Interface was not in a valid format. This means that the `ID` was passed as a non-numerical string of characters. Mapping configuration `IDs` must be purely numerical and contain the `'-'` character.
    - This is a **user error**; external assistance is unnecessary.
- `[Error 5] Undefined mapping configuration ID passed.` This error indicates that the mapping configuration `ID` number passed to the KIM Interface was not found in the `mapping configurations` defined for the machine requested. This likely means the user entered an incorrect `ID` number for the desired mapping configuration, or the user needs to define a new mapping configuration entirely.
    - This is a **user error**; external assistance is unnecessary.
- `[Error 6] Access to Keyence IM-8001 folder denied.` This error indicates that the KIM Interface was unable to gain access to the `Keyence IM-8001` folder. This error is very uncommon and means there has been some change in the `Gateway Host` environment or the `Keyence IM-8001` folder.
    - This is an **environment issue**; contact the IT Department.
- `[Error 7] Unable to locate Keyence IM-8001 folder.` This error indicates that the KIM Interface was unable to locate the `Keyence IM-8001` folder. This likely means there has been some change to the way the `Keyence IM-8001` folder is structured.
    - This is an **environment issue**; contact the IT Department.
- `[Error 8] Current measurement sheet for [machine name] could not be found.` This error indicates that the KIM Interface was unable to find an Excel sheet titled `Measurements.xlsx` or `Measurements.csv` in the machine's folder. This means that the sheet may have a different name or that it does not exist at all.
    - This is an **organization error**; contact the manager of the Keyence IM Machines.
- `[Error 9] Unable to open the current measurement sheet.` This error indicates that the current measurement sheet was located but the KIM Interface failed to open it. This could mean that the sheet is corrupt, uses an invalid character, or has some other kind of internal formatting error.
    - This is an **organization error**; contact the manager of the Keyence IM Machines.
- `[Error 10] No mapping configurations folder in KIM Interface file.` This error indicates that the KIM Interface environment folder is missing the internal `mapping configuration` files. This error is a critical issue as the KIM Interface cannot pass its results to the i-Reporter form through `Gateway` without a valid mapping. This is likely caused by a lack of defined mapping configurations in the `KIM Interface Manager`. Ensure there is at least one mapping configuration defined for the machine being accessed.
    - This is a **user error**; external assistance is unnecessary.
- `[Error Unknown] [description].` This error indicates that the KIM Interface encountered an unexpected error that would otherwise crash it. A `Python exception` message will be included in the return of this error, as well as the action the KIM Interface was carrying out when the error was produced.
    - This is an **environment issue**; contact the IT Department.

### Organization and Network Remarks

The KIM Interface connects several systems from across YNA’s network. Although a large effort was made to ensure resilience and adaptability within the system, there are some things that users of the KIM Interface should be aware of. Below are some remarks and best-practices that will help the KIM Interface run smoothly and seamlessly for YNA:

#### Setting Up a New Model

If YNA installs Keyence IM-8001 Machines on a new Model or Production Line, these guidelines will help ensure that users are loading the new Model into the KIM Interface properly

- Begin by creating the new Model, making sure that all the Model’s `Base Information` has been acquired from the engineers installing and managing the Keyence Machines;
- Configure each of the Machines next, carefully copying the Machine’s `name` and `Measurement Specifications`.

#### Using KIM Interface in a New i-Reporter Form

>[!IMPORTANT]
>Be sure to create a new `mapping configuration` for each machine sending data to the form. Follow the processes in `Chapter VI` to >ensure the connection is established correctly.

#### Folder Structure

KIM Interface assumes the following `Keyence IM-8001` folder structure:

**\\buckeye1\Keyence IM-8001\MSetting**

>[!WARNING]
>If this folder structure is obstructed or altered, the KIM Interface will fail to collect data from the Keyence IM-8001 Machine
>measurement sheets. Maintaining this folder structure is critical to the function of the program. If the folder structure needs to be
>changed, please contact the developer, as a patch will need to be distributed to YNA.

Users should verify that the Machine they are accessing has a folder inside the `MSetting` subfolder of the `Keyence IM-8001` folder. Even a machine that is correctly configured in the `KIM Interface Manager` will fail to access data if it does not have a folder in `MSetting`.

**Example:** If the user is accessing the `3D4 HS DIFF FIXED LATHE CENTER`, there must be a folder in `MSetting` for that specific name.
Inside this folder, there must be a `Measurements.csv` OR `Measurements.xlsx` file holding the Machine’s measurement results. If this file is absent, it will result in an `Error 8` instance.

### Developer Contact

Please remember that users are free to contact the developer at any time. KIM Interface is an ongoing development project and will always be open for issue submissions and feature requests. Users can contact the developer on GitHub via https://github.com/masonritchason.

Refer to this documentation frequently and the KIM Interface will become a powerful tool for managing the automatic collection of Keyence IM-8001 Machine data!

— Mason Ritchason, designer & developer; [@masonritchason](https://github.com/masonritchason)
