# v0.1.2 - 2024-11-25

### Features

- Add alias `procees ls` for `process list`
- New command: `whoami`

### Fixes

- Renamed *databases.template* to *databases.yaml.template*

### Chore

- Added repository url to pyproject.toml
- Improved test coverage

# v0.1.1 - 2024-11-24

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
