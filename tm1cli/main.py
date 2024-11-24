import os

import typer
from dotenv import load_dotenv
from TM1py import TM1Service

app = typer.Typer()

# Global state to store loaded configuration
config = {}

@app.callback()
def main(env_file: str = typer.Option(".env", help="Path to the .env file")):
    """
    CLI tool to interact with TM1 using TM1py.
    """
    load_dotenv(env_file)

    config["address"] = os.getenv("TM1_ADDRESS")
    config["user"] = os.getenv("TM1_USER")
    config["password"] = os.getenv("TM1_PASSWORD")
    config["ssl"] = os.getenv("TM1_SSL")
    config["port"] = os.getenv("TM1_PORT")

@app.command()
def tm1_version():
    with TM1Service(**config) as tm1:
        version = tm1.server.get_product_version()
        print(version)

@app.command()
def threads():
    with TM1Service(**config) as tm1:
        threads = tm1.sessions.get_threads_for_current()
        print(threads)

if __name__ == "__main__":
    app()