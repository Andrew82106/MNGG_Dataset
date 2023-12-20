import re


def read_file_content(file_path):
    """
    读取文件内容
    :param file_path: 文件路径
    :return: 文件内容
    """
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print("文件不存在")
        return None
    except Exception as e:
        print("读取文件出错:", str(e))
        return None


def wash_content(content):
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if content is None:
        return []

    # 以句号分割内容
    sentences = content.split("。")

    cleaned_sentences = []
    for sentence in sentences:
        cleaned_sentence = re.sub(r'[^\u4e00-\u9fff0-9a-zA-Z,;!！；，]', '', sentence)
        english_chars_count = sum(
            1 for char in cleaned_sentence if char in 'qwertyuiopsadfghjklzxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM')
        if len(cleaned_sentence) > 20 and english_chars_count == 0:
            cleaned_sentences.append(cleaned_sentence)

    return cleaned_sentences


def wash_news_data(r):
    c = read_file_content(r)
    b = wash_content(c)
    print(f'successfully cleaning {r}')
    return b


if __name__ == '__main__':
    print(wash_news_data('/Users/andrewlee/Desktop/Projects/A/makeDataset/dataset/THUC/all.txt'))