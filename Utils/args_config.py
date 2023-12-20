import argparse
args_list = [
    {'name': '--mode', 'type': str, 'default': 'generate_clip'},
    {'name': '--train_ratio', 'type': float, 'default': 0.5},
    {'name': '--test_ratio', 'type': float, 'default': 0.3},
    {'name': '--dev_ratio', 'type': float, 'default': 0.2},
    {'name': '--clip_ratio', 'type': float, 'default': 0.1},
    {'name': '--clip', 'type': bool, 'default': True},
]

parser = argparse.ArgumentParser(description='Process some integers.')
for arg in args_list:
    arg_name = arg['name']
    del arg['name']
    parser.add_argument(arg_name, **arg)

args = parser.parse_args()