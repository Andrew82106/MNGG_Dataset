import os

with open("./MNGG.all.txt", "r", encoding='utf-8') as f:
    cont = f.read().split("。\tF")
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