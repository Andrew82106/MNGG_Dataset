import argparse
args_list = [
    {'name': '--mode', 'type': str, 'default': 'generate_clip'}
]

parser = argparse.ArgumentParser(description='Process some integers.')
for arg in args_list:
    arg_name = arg['name']
    del arg['name']
    parser.add_argument(arg_name, **arg)

args = parser.parse_args()