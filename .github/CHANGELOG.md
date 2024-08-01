# Changelog

All notable changes to this project will be documented in this file.

### KIM Interface v1.2.0
##### What's Changed in `v1.2.0`
* `CHANGELOG.md` view added in startup window.
* `Help` window added in-app:
    * Users are able to open a windowed view of the user's manual in the `Manager`.
    * A `Contact Card` has been added to allow quick access to more help.
* KIM Interface v1.2.0 by @masonritchason in https://github.com/masonritchason/KIM-Interface-Manager/pull/5

#### Patch 3 `v1.1.43`
##### What's Changed
* GitHub Features
    * Moved from Private to Public
    * SECURITY.md and Security features
    * CODEOWNERS Code-owners
    * Code of Conduct
    * CONTRIBUTION.md
    * Issue templates (Bug Reports, Features, Security Alert)
    * README.md update
    * KIM Interface v1.1.43 by @masonritchason in #98
>[!NOTE]
>`#98` refers to a `pull request` in the original repository.
>This `pull request` was a fix for a small grammatical issue.

#### Patch 2 `v1.1.42`
Packaging Error
Application package was not updated from `v1.1.3` to `v1.1.4` in the initial release of `v1.1.4`. This patch fixes that issue.

#### Patch 1 `v1.1.41`
Hotfix for a set of issues with the documentation file.
No new features.

### KIM Interface v1.1.4
##### What's Changed in `v1.1.4`
* Final patch of KIM Interface `v1.1`
* Dependencies included in package as `requirements.txt`.
* User signature control has been added.
    * The user login on the OS of the Gateway VM will be used to sign the `Manager` component.
    * Signing the `Manager` means two things:
        * Users will know they are active in the `Manager` when their YNA Windows username shows at the top of the application window.
        * Changes made to configuration files now receive a user signature as well as the timestamp.
* A Changelog system has been added.
    * Every change made in the Manager is logged in the `changelog.txt` file.
    * This has been added as an extension of the log suite to bolster the troubleshooting resources available to users.

#### Patch 1 `v1.1.31`
Quick patch to update the KIM Interface Manager's configuration file.
No new features.

### KIM Interface v1.1.3
##### What's Changed in `v1.1.3`
The QOL Overhaul!
* The KIM_Logger component has been integrated into the Interface component itself.
    * There was no need for the two to be separate. This leaves less space for interfacing issues, data loss, etc.
* Information being logged has been expanded to include more useful troubleshooting tools.
* Configuration backups have been added.
    * Each time the Manager is opened or closed, a backup of the configuration files will be generated.
    * 25 configuration backups are included in the backups folder.
    * They can be loaded at any time to repair a damaged or lost configuration set.
* Configuration file timestamping has been implemented.
    * When a configuration file is opened and edited in any way, or when a new file is created, the file is given a timestamp value.
    * The timestamp value will indicate the most recent change time of that file. It is used to give backups a timestamp.
* Slight Menu optimizations
    * Navigation menu

### KIM Interface v1.1.2-stable
##### What's Changed in `v1.1.2-stable`
* KIM Interface v1.1.2 by @masonritchason in #87
>[!NOTE]
>`#87` refers to a `pull request` in the original repository.
>This `pull request` was the development of the initial `Information` window.
* `Simulator` function removed; renamed to `Information` window.
* Issue with `Interface` component integration crashing the `Manager` resolved; integration removed.
* Tidy-up of build files included in package.

###### Stability
Stability is restored in this version of the software.

### KIM Interface v1.1.1-alpha (Pre-release)
##### What's Changed in `v1.1.1-alpha`
* KIM Interface 1.1.1-alpha by @masonritchason in #85
>[!NOTE]
>`#85` refers to a `pull request` in the original repository.
>This `pull request` was the development of the Measurement Filter options.
* Measurement Filtering & Validation:
    * Measurements will be compared against their corresponding Machine measurement specifications.
    * Two Filtering Options
        * Filter by removal: measurements that are out-of-spec are "trashed" by the system, sending a blank measurement value instead;
        * Allow NG data: measurements that are out-of-spec are allowed through the system, relying on the configuration of the i-Reporter form to indicate NG status.

###### Alpha Release
Potentially-unstable features from https://github.com/masonritchason/KIM-Interface/releases/tag/v1.1.0-alpha. Beware of using this release.

### KIM Interface 1.1.0-alpha (Pre-release)
##### What's Changed in `v1.1.0-alpha`
* KIM Interface v1.1.0-alpha by @masonritchason in #82
>[!NOTE]
>`#82` refers to a `pull request` in the original repository.
>This `pull request` was the development of the `Simulator` window, the predecessor to the `Information` window.
* The Simulator Window under initial development (unstable)
    * The URL Generation widget was added.
    * The Logs View widget was added.
    * The Results View widget was added.

###### Alpha Release
Potentially-unstable features implemented in the Simulator component. Beware of using this release.

### KIM Interface v1.0.3
##### What's Changed in `v1.0.3`
* Duplication of `Mapping Configurations`;
    * Users are able to easily create copies from an existing `Mapping Configuration`.
* Cascading Field Removal;
    * Previously, when a field was removed from a `Model` or a `Machine`, the Configurations under those objects were not affected.
        * This was allowing non-existent information to leak into the environment.
    * Now, that removal will cascade through to all of the subsequent `Mapping Configurations` under those objects.

### KIM Interface v1.0.2
##### What's Changed in `v1.0.2`
* Program renamed from `Keyence Retriever` to `KIM Interface`;
* Refactored into a package-based application using `PyInstaller`;
* Mapping editor by @masonritchason in #66;
>[!NOTE]
>`#66` refers to a `pull request` in the original repository.
>This `pull request` was the initial development of the `Mapping Configuration Editor`, the predecessor to the `KIM Interface Manager`.
* Major documentation overhaul

### Keyence Retriever 1.0.1
##### What's Changed in `v1.0.1`
This sub-version of KR Script 1 introduced the initial implementation of mapping configurations.
* The script is now able to map information to i-Reporter forms dynamically.
**This means:**
* Users can design forms that use only partial measurement sets;
* Users can define multiple mapping configurations for the same measurements to allow for multiple measurement populations over time.

### Keyence Retriever 1.0
**The initial build of the Keyence Retriever script is complete and can be used on YNA's server with i-Reporter forms.**