# TM1-CLI

**TM1-CLI** is a command-line interface (CLI) tool to interact with TM1 servers using [TM1py](https://github.com/cubewise-code/tm1py). It supports environment-based configuration via `.env` files for flexible and secure connection management.

---

## Features

- Easily execute TM1 functions via the command line.
- Manage connection settings with `.env` files.
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

### Basic Command

Connect to a TM1 server and print its version:

```bash
tm1cli tm1-version
```

### Available Commands

Run the following to see all available commands:

```bash
tm1cli --help
```

### Configuration

Connection settings are stored in a .env file. Here's an example:

```
TM1_ADDRESS=localhost
TM1_USER=admin
TM1_PASSWORD=apple
TM1_SSL=true
TM1_PORT=12345
```