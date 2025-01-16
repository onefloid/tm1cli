# TM1-CLI

![PyPI - License](https://img.shields.io/pypi/l/tm1cli)
![PyPI - Version](https://img.shields.io/pypi/v/tm1cli)

**TM1-CLI** is a command-line interface (CLI) tool to interact with TM1 servers using [TM1py](https://github.com/cubewise-code/tm1py).

---

## Features

- Easily execute TM1 functions via the command line.
- Manage multiple connection settings with `databases.yaml` file.
- Built with Python, powered by [Typer](https://typer.tiangolo.com/) for intuitive CLI design.

---

## Installation

### Using `pip`
Install the package directly from PyPI:

```bash
pip install tm1cli
```

### Using Poetry

Clone the repository and install using Poetry

```bash
git clone https://github.com/onefloid/tm1cli.git
cd tm1cli
poetry install
```

## Usage

### Commands

Connect to a TM1 server and print its version:

```bash
tm1cli tm1-version
tm1cli threads
tm1cli whoami

tm1cli process list
tm1cli process exists <process_name>
tm1cli process clone --from <source_db> --to <target_db>
tm1cli process dump <name> --folder <path> --format <json|yaml>
tm1cli process load <name> --folder <path> --format <json|yaml>

tm1cli cube list
tm1cli cube exists <cube_name>

tm1cli dimension list
tm1cli dimension exists <dimension_name>

tm1cli view list <cube_name>
tm1cli view exists <cube_name> <view_name>

tm1cli subset list <dimension_name>
tm1cli subset exists <dimension_name> <subset_name>
```

### All Available Commands

Run the following to see all available commands:

```bash
tm1cli --help
```

### Configuration

Connection settings are stored in a _databases.yaml_ file. Here's an example:

```yaml
databases:
  - name: mydb
    address: localhost
    port: 10001
    ssl: false
    user: admin
    password: ""

  - name: myremotedb
    address: tm1.example.com
    port: 20000
    ssl: false
    user: admin
    password: apple
```