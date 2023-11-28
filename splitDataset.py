import os
import re


def is_illegal_character(char):
    # 列举合法字符范围：汉字、标点、字母、数字
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789，。！？、；：‘’“”（）()<>《》&#8203;``【oaicite:0】``&#8203;……—·￥—·\t\n')

    # 检查字符是否在合法范围内
    return char not in valid_chars and not ('\u4e00' <= char <= '\u9fff')


with open("./MNGG.all.txt", "r", encoding='utf-8') as f:
    cont = f.read().split("。\tF")
    """
    for jj in cont:
        for j in jj:
            if is_illegal_character(j):
                raise Exception(f"illegal character:{j}")
    """
    for i in cont:
        if "。\tF" in i:
            print(i)
            exit()
    print("pass test")
    n = len(cont)
    TrainRatio = 0.4
    DevRatio = 0.2
    TestRatio = 0.4
    TrainN = int(TrainRatio * n)
    DevN = int(DevRatio * n)

    with open("./MNGG.train.txt", "w", encoding='utf-8') as f:
        for i in range(TrainN):
            f.write(cont[i].lstrip('\n'))
            f.write("。\tF\n\n")

    with open("./MNGG.dev.txt", "w", encoding='utf-8') as f:
        for i in range(TrainN, TrainN + DevN):
            f.write(cont[i].lstrip('\n'))
            f.write("。\tF\n\n")

    with open("./MNGG.test.txt", "w", encoding='utf-8') as f:
        for i in range(TrainN + DevN, n):
            f.write(cont[i].lstrip('\n'))
            f.write("。\tF\n\n")

if os.path.exists("./MNGG.all.bio"):
    with open("./MNGG.all.bio", "r", encoding='utf-8') as f:
        cont = f.read().split("。\tF")
        """
        for j in cont:
            if is_illegal_character(j):
                raise Exception("illegal character")
        """
        for i in cont:
            if "。\tF" in i:
                print(i)
                exit()
        print("pass test")
        n = len(cont)
        TrainRatio = 0.4
        DevRatio = 0.2
        TestRatio = 0.4
        TrainN = int(TrainRatio * n)
        DevN = int(DevRatio * n)

        with open("./MNGG.train.bio", "w", encoding='utf-8') as f:
            for i in range(TrainN):
                f.write(cont[i].lstrip('\n'))
                f.write("\n")

        with open("./MNGG.dev.bio", "w", encoding='utf-8') as f:
            for i in range(TrainN, TrainN + DevN):
                f.write(cont[i].lstrip('\n'))
                f.write("\n")

        with open("./MNGG.test.bio", "w", encoding='utf-8') as f:
            for i in range(TrainN + DevN, n):
                f.write(cont[i].lstrip('\n'))
                f.write("\n")