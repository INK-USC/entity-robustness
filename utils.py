import os
import argparse
import json
from pathlib import Path


def check_path(path):
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d)


def ensure_file_path(file_path):
    folder_path = os.path.dirname(file_path)
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)


def check_folder_path(folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)


def parse_cmd(argv):
    # example input: ['--key1', 'value1', '--key2', 'value2']
    p = argparse.ArgumentParser()
    args, extras = p.parse_known_args(argv)

    def foo(astr):
        if astr.startswith('--'):
            astr = astr[2:]
        astr = astr.replace('-', '_')
        return astr

    d = {foo(k): v for k, v in zip(extras[::2], extras[1::2])}
    return d


def read_args(parser, argv):
    if argv[1].endswith(".json"):
        json_dict = json.loads(Path(os.path.abspath(argv[1])).read_text())
        remaining_argv = argv[2:]
        cmd_dict = parse_cmd(remaining_argv)
        for key_to_add, value_to_add in cmd_dict.items():
            original_value = json_dict[key_to_add]
            original_type = type(original_value)
            # NoneType is not handled
            if original_type == bool:
                if value_to_add.lower() in ('yes', 'true', 't', 'y', '1'):
                    value_to_add = True
                elif value_to_add.lower() in ('no', 'false', 'f', 'n', '0'):
                    value_to_add = False
                else:
                    raise ValueError()
            else:
                value_to_add = original_type(value_to_add)
            json_dict[key_to_add] = value_to_add
        model_args, data_args, training_args = parser.parse_dict(json_dict)
    else:
        model_args, data_args, training_args = parser.parse_args_into_dataclasses()
    return model_args, data_args, training_args