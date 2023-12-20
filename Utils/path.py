import os
import sys

rootname = 'makeDataset'

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.abspath(__file__)

root_path = current_dir.split(rootname)[0] + rootname

utils_path = os.path.join(root_path, 'Utils')

dataset_path = os.path.join(root_path, 'dataset')

shadow_path = os.path.join(root_path, 'shadow')
work_cache_path = os.path.join(shadow_path, 'work_cache')
if not os.path.exists(shadow_path):
    os.makedirs(shadow_path)
if not os.path.exists(work_cache_path):
    os.makedirs(work_cache_path)

dog_whistle_path = os.path.join(dataset_path, 'dogwhistle')

dog_whistle_insider_path = os.path.join(dog_whistle_path, 'Insider')
dog_whistle_insider_dev_path = os.path.join(dog_whistle_insider_path, 'dev.tsv')
dog_whistle_insider_test_path = os.path.join(dog_whistle_insider_path, 'test.tsv')
dog_whistle_insider_train_path = os.path.join(dog_whistle_insider_path, 'train.tsv')

dog_whistle_outsider_path = os.path.join(dog_whistle_path, 'Outsider')
dog_whistle_outsider_dev_path = os.path.join(dog_whistle_outsider_path, 'dev.tsv')
dog_whistle_outsider_test_path = os.path.join(dog_whistle_outsider_path, 'test.tsv')
dog_whistle_outsider_train_path = os.path.join(dog_whistle_outsider_path, 'train.tsv')

THUC_path = os.path.join(dataset_path, 'THUC')
THUC_all_data_path = os.path.join(THUC_path, 'all.txt')

MNGG_path = os.path.join(dataset_path, 'MNGG')

sys.path.append(root_path)
sys.path.append(utils_path)
sys.path.append(dataset_path)
sys.path.append(THUC_path)


if __name__ == '__main__':
    print(THUC_all_data_path)
    print(dog_whistle_insider_dev_path)