import pandas as pd
import tqdm
import numpy as np
import jieba
import re


def remove_extra_whitespace(text):
    # 去除文本中的非断行空白字符（包括空格、制表符等）
    text = re.sub(r'\s+', ' ', text)
    # 去除文本两端的空白字符
    text = text.strip()
    return text


bio = 1
THUC_path = "./THUC/all.txt"
dogWhistle_path = "./CantPair.xlsx"


def read_cantPair():
    df = pd.read_excel(dogWhistle_path)
    pair = {}
    cantLst = []
    for i in tqdm.tqdm(range(len(df)), desc="reading cant pairs"):
        cant = df.iloc[i, 1]
        refer = df.iloc[i, 2]
        if refer in cantLst:
            continue
        cantLst.append(cant)
        # 一个词语可能有多个暗语词汇对应
        if refer not in pair:
            pair[refer] = []
        pair[refer].append(cant)
    print(f"num of refer:{len(pair)}")
    return pair


def tokenize_with_position(text):
    words = list(jieba.cut(text, cut_all=False))
    word_positions = []

    start = 0
    for word in words:
        start = text.find(word, start)
        end = start + len(word)
        word_positions.append([word, (start, end), 0])
        start = end

    return word_positions


if __name__ == '__main__':
    pair = read_cantPair()
    with open(THUC_path, "r", encoding='utf-8') as f:
        content = remove_extra_whitespace(f.read())
    word_positions = tokenize_with_position(content)
    cnt = 0
    for refer in tqdm.tqdm(pair, desc='processing pairs'):
        cant = pair[refer][0]
        for i in pair[refer]:
            if "。" not in i:
                cant = i
                break
        for Index in range(len(word_positions)):
            word = word_positions[Index][0]
            if refer == word:
                word_positions[Index][0] = cant
                word_positions[Index][2] = 1
                cnt += 1
    filename = "./MNGG.all.txt"
    if bio:
        filename = "./MNGG.all.bio"
    print(f"finish processing pairs using {cnt} words with a replace ratio of {100 * cnt / len(word_positions)}%")
    print(f"process mode:{'bio' if bio else 'T/F'}")
    with open(filename, "w", encoding='utf-8') as f:
        for i in tqdm.tqdm(word_positions, desc="writing datasets"):
            if not bio:
                for j in i[0]:
                    f.write(f"{j}\t{'F' if i[2] == 0 else 'T'}\n")
            else:
                cnt = 0
                for j in i[0]:
                    if cnt > 0:
                        f.write(f"{j}\t{'I-CANT' if i[2] == 1 else 'O'}\n")
                    else:
                        f.write(f"{j}\t{'B-CANT' if i[2] == 1 else 'O'}\n")
                        cnt = 1
                    if j == '。':
                        f.write("。\tF\n")

    print("end")
