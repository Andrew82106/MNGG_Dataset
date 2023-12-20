import tqdm
import pandas as pd


def generate_pair_raw(r):
    df = pd.read_table(r)
    cant_pair = {}
    total_length = len(df)

    for ID, Index in tqdm.tqdm(enumerate(range(total_length)), total=total_length, desc='Generating pair'):
        instance = df.iloc[Index:Index + 1]
        Cant = instance['CantToDecode'][ID]
        code = instance['code'][ID]
        HiddenWords = instance['HiddenWords'][ID].split(",")[int(code)]
        cant_pair[Cant] = HiddenWords

    return cant_pair


import re


def is_valid_word(word):
    # 检查词语是否合法
    if 6 >= len(word) >= 2:
        for I in word:
            if not bool(re.search(r'[\u4e00-\u9fff]', I)):
                return False
        return True
    else:
        return False


def clean_invalid_pairs(raw_pair):
    cleaned_pair = {}
    for key, value in raw_pair.items():
        # 检查key和value是否合法
        if "蝴蝶" in key + value:
            pass
        if is_valid_word(key) and is_valid_word(value):
            cleaned_pair[key] = value
    return cleaned_pair


def generate_pair(r):
    raw_pair = generate_pair_raw(r)
    cleaned_pair = clean_invalid_pairs(raw_pair)
    print(f"successfully generate pair from file {r}")
    return cleaned_pair


if __name__ == '__main__':
    r0 = '/Users/andrewlee/Desktop/Projects/A/makeDataset/dataset/dogwhistle/Insider/dev.tsv'
    cp = generate_pair(r0)
    print(len(cp))
