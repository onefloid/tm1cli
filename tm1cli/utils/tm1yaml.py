import json

import yaml
from TM1py.Objects import Process


class MultiLineString(str):
    pass


def multiline_string_representer(dumper, data):

    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


def process_representer(dumper, data):

    output_data = json.loads(data.body)

    # Convert to Multiline String
    for section_name in [
        "PrologProcedure",
        "MetadataProcedure",
        "DataProcedure",
        "EpilogProcedure",
    ]:
        process_section = output_data.get(section_name).replace("\r\n", "\n")
        output_data[section_name] = MultiLineString(process_section)

    return dumper.represent_mapping("!TM1py.ProcessObject", output_data)


def process_constructor(loader, node):
    fields = loader.construct_mapping(node, deep=True)
    return Process.from_dict(fields)


def dump_process(process: Process) -> str:
    yaml.add_representer(MultiLineString, multiline_string_representer)
    yaml.add_representer(Process, process_representer)
    return yaml.dump(
        process, default_flow_style=False, allow_unicode=True, sort_keys=False
    )


def load_process(process_yaml: str):
    yaml.add_constructor("!TM1py.ProcessObject", process_constructor)
    process = yaml.load(process_yaml, Loader=yaml.FullLoader)
    return process
