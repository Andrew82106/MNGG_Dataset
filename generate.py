import pandas as pd
import tqdm
from Utils.path import *
from Utils.wash_news_data import wash_news_data
from Utils.generate_pair import generate_pair
from Utils.args_config import args
import jieba


def remove_duplicates(cant_pair):
    """
    移除字典中的重复值，确保键值对的唯一性
    Args:
    - cant_pair: 待处理的字典
    Returns:
    - unique_cant_pair: 不含重复值的字典
    """
    seen_values = set()
    unique_cant_pair = {}
    for key, value in cant_pair.items():
        if value not in seen_values:
            seen_values.add(value)
            unique_cant_pair[key] = value
    return unique_cant_pair


def generate_pair_process():
    """
    生成暗语对字典并处理重复值
    Returns:
    - cant_pair: 暗语对字典
    - word_pair: 键值对颠倒后的暗语对字典
    """
    cant_pair = {}
    # cant_pair[word]返回暗语词汇word的指代词汇
    cant_pair.update(generate_pair(dog_whistle_insider_dev_path))
    cant_pair.update(generate_pair(dog_whistle_insider_test_path))
    cant_pair.update(generate_pair(dog_whistle_insider_train_path))
    cant_pair = remove_duplicates(cant_pair)
    word_pair = {v: k for k, v in cant_pair.items()}
    # word_pair[word]返回词汇word的暗语词汇
    assert len(cant_pair) == len(word_pair), '存在不同暗语对有相同指代词的情况'
    print(f"读取暗语对长度：{len(cant_pair)}")
    return cant_pair, word_pair


def segment_and_insert_cant(custom_words, sentences, word_pair):
    """
    对句子进行分词，标记词语是否在word_pair中
    Args:
    - custom_words: 自定义词汇表列表
    - sentences: 待分词的句子列表
    - word_pair: 暗语对字典
    Returns:
    - segmented_sentences: 处理后的句子列表
    """
    for word in custom_words:
        jieba.add_word(word)

    # 对每个句子进行分词，并将包含暗语的句子的分词结果存储在新列表中
    segmented_sentences = []
    sum_of_cant = 0
    sum_of_word = 0
    how_many_sentence_has_cant = 0
    cant_max_count = 0
    for sentence in tqdm.tqdm(sentences, desc='processing sentences'):
        # 使用jieba分词
        cant_count = 0
        has_cant = False
        words = jieba.lcut(sentence)
        # 对于每个词语进行标记是否在word_pair中
        marked_words = []
        sum_of_word += len(words)
        for word in words:
            marked_words.append([word_pair[word], 1] if word in word_pair else [word, 0])
            if marked_words[-1][-1]:
                cant_count += 1
            has_cant |= marked_words[-1][-1]
            sum_of_cant += marked_words[-1][-1]
        if has_cant:
            cant_max_count = max(cant_count, cant_max_count)
            how_many_sentence_has_cant += 1
            segmented_sentences.append(marked_words)

    print(f"所有{len(sentences)}句中，有{how_many_sentence_has_cant}句有暗语，一句话中最多暗语数量为{cant_max_count}")
    print(f"共替换{sum_of_cant}词语，占总词语数{sum_of_word}的{100 * sum_of_cant / sum_of_word}%")
    print(f"现将{len(segmented_sentences)}句进行输出")
    return segmented_sentences


def save_as_bio_format(segmented_sentences, output_file_path):
    """
    将segmented_sentences中的句子信息输出为BIO标注格式的.bio文档
    Args:
    - segmented_sentences: 处理后的句子列表
    - output_file_path: 输出文件的路径
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for sentence in segmented_sentences:
            for word_info in sentence:
                word, is_cant = word_info
                if is_cant == 1:  # 是暗语词汇
                    if len(word) == 1:
                        file.write(f"{word}\tB-CANT\n")
                    else:
                        file.write(f"{word[0]}\tB-CANT\n")
                        for char in word[1:]:
                            file.write(f"{char}\tI-CANT\n")
                else:  # 非暗语词汇
                    for char in word:
                        file.write(f"{char}\tO\n")
            file.write('。 O\n')  # 句子结束标志
            file.write('\n')  # 句子结束标志
        print(f"successfully save data to {output_file_path}")


def output_word_pair(word_pair):
    D = {"word": [], "cant": []}
    for word in word_pair:
        cant = word_pair[word]
        D['word'].append(word)
        D['cant'].append(cant)
    pd.DataFrame(D).to_excel(os.path.join(MNGG_path, 'cant_word.xlsx'))
    print(f"successfully save cant word to {os.path.join(MNGG_path, 'cant_word.xlsx')}")


def generate_main(train_ratio=0.5, test_ratio=0.3, dev_ratio=0.2, clip_ratio=0.1, clip=False):
    """
    主要生成函数，调用各项处理流程并返回处理结果
    Returns:
    - train_segmented_sentences: 训练集的处理后的句子列表
    - test_segmented_sentences: 测试集的处理后的句子列表
    """
    if clip:
        train_ratio *= clip_ratio
        dev_ratio *= clip_ratio
        test_ratio *= clip_ratio
    sentences = wash_news_data(THUC_all_data_path)
    cant_pair, word_pair = generate_pair_process()
    custom_words = list(word_pair.keys())
    segmented_sentences = segment_and_insert_cant(custom_words, sentences, word_pair)
    output_train_file_path = os.path.join(MNGG_path, 'train.bio' if not clip else 'train.clip.bio')
    output_test_file_path = os.path.join(MNGG_path, 'test.bio' if not clip else 'test.clip.bio')
    output_dev_file_path = os.path.join(MNGG_path, 'dev.bio' if not clip else 'dev.clip.bio')

    # 根据 train_ratio 和 test_ratio 拆分数据集
    total_sentences = len(segmented_sentences)
    train_size = int(train_ratio * total_sentences)
    test_size = int(test_ratio * total_sentences)
    dev_size = int(dev_ratio * total_sentences)

    train_segmented_sentences = segmented_sentences[:train_size]
    test_segmented_sentences = segmented_sentences[train_size:train_size + test_size]
    dev_segmented_sentences = segmented_sentences[train_size + test_size:dev_size + train_size + test_size]

    # 保存为 .bio 文件
    save_as_bio_format(train_segmented_sentences, output_train_file_path)
    save_as_bio_format(test_segmented_sentences, output_test_file_path)
    save_as_bio_format(dev_segmented_sentences, output_dev_file_path)
    output_word_pair(word_pair)
    print("Summary：")
    print(f"是否裁剪：{'是' if clip else '否'}")
    print(f"输出训练集长度：{len(train_segmented_sentences)}")
    print(f"输出测试集长度：{len(test_segmented_sentences)}")
    print(f"输出开发集长度：{len(dev_segmented_sentences)}")
    print(f"共含暗语词汇数量：{len(word_pair)}")


if args.mode == 'generate_main':
    generate_main(
        train_ratio=args.train_ratio,
        test_ratio=args.test_ratio,
        dev_ratio=args.dev_ratio,
        clip=False
    )
elif args.mode == 'generate_clip':
    generate_main(
        train_ratio=args.train_ratio,
        test_ratio=args.test_ratio,
        dev_ratio=args.dev_ratio,
        clip_ratio=args.clip_ratio,
        clip=True
    )
