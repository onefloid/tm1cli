# Changelog

## v0.1.7 - 2025-05-20

### Features

- New command: `version` for tm1cli version
- Support `TM1_` environment variables as alternative to config file `database.yaml`

### Docs

- Minor improvements in the readme

## v0.1.6 - 2025-01-16

### Features

- New watch option for exists command, e.g: `cube exists <cube_name> --watch`

## v0.1.5 - 2025-01-16

### Features

- New command: `cube exists`
- New command: `view exists`
- New command: `dimension list`
- New command: `dimension exists`
- New command: `subset list`
- New command: `subset exists`


### Chore

- Improved testing

## v0.1.4 - 2024-11-29

### Features

- New command: `cube list`
- New command: `view list`

### Fix

- Fix case error in _**u**til_ folder

### Chore

- Added CI Job for linting
- Added CI Job for publishing to pypi
- Autoformat files
- Fix linting errors

## v0.1.3 - 2024-11-29

### Features

- New command: `process dump` a process as yaml or json file
- New command: `process load` a process from a yaml or json file

The yaml representation uses multi-line strings for the script
sections to make it easy to version your dumps with Git in a 
human-readable format.

### Docs

- Improved cli helptexts
- Added beautiful badges in the readme file

### Chore

- Added license file
- Various refactorings


## v0.1.2 - 2024-11-25

### Features

- Add alias `procees ls` for `process list`
- New command: `whoami`

### Fixes

- Renamed *databases.template* to *databases.yaml.template*

### Chore

- Various refactorings
- Improved docs

## v0.1.1 - 2024-11-24

### Features

- Configure multiple databases in one yaml configuration
- Specify database with the `-d` or `--database` option
- New command: Get `threads` as json or as command line table
- New command `process exists`
- New command `process list`
- New command `process clone`
- Formatting errors in red font


### Breaking changes

- .env configuration is replaced with yaml config

# v0.1.0 - 2024-11-20

### Features

- Get TM1 Server Version with `tm1-version`
