r = [
    "./MNGG.train.bio",
    "./MNGG.dev.bio",
    "./MNGG.test.bio",
]


rate = 0.2


for filename in r:
    with open(filename, "r", encoding='utf-8') as f:
        cont = f.read()

        sentence = cont.split("。	O\n")

        print(f"file:{filename} total sentence:{len(sentence)}")

        newfileName = filename.replace(".bio", ".clip.bio")
        with open(newfileName, "w", encoding='utf-8') as f1:
            cnt = 0
            max_sentence_len = 100
            for i in sentence:
                if len(i) > max_sentence_len:
                    continue
                cnt += 1
                f1.write(i + "。	O\n")
                if cnt > len(sentence) * rate:
                    break
            print(f"new sentence count:{cnt}")