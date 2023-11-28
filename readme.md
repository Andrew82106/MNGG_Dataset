# Mystique Naming Glossary Gathering

"Mystique Naming Glossary Gathering" 是一个专门为了让计算机理解暗语（Cant）而设计的数据集。暗语是一种特殊的语言形式，通常由特定社群或群体使用，其目的是隐藏信息或传递特定意义。该数据集致力于解决暗语的两个关键任务：暗语的发现和暗语的解释。

## 数据

- train：MNGG.train.txt
- test：MNGG.test.txt
- dev：MNGG.dev.txt


- train(bio format)：MNGG.train.bio
- test(bio format)：MNGG.test.bio
- dev(bio format)：MNGG.dev.bio

train，test，dev比率为2：2：1

## 数据集任务：

1. **暗语的发现任务：** 这个任务旨在帮助计算机发现、识别并学习暗语的模式和特征。数据集中包含了各种形式的暗语文本，算法需要能够自动辨识文中的暗语文本并标记。
2. **暗语的解释任务：** 此任务旨在训练计算机理解并解释暗语的含义。数据集中提供了暗语的上下文。算法需要通过上下文信息进行MASK动作，从而实现暗语的解释。

## 数据集来源:

我们使用[dogwhistle dataset](https://github.com/JetRunner/dogwhistle)中insider的词汇作为暗语词汇，使用THUCNEWS的新闻数据作为基座文本，将基座文本中的词语用暗语词汇进行替换，然后进行数据集的拆分，就得到了MNGG数据集

代码层面，首先准备好dogwhistle数据集和THUC数据集，然后：

```python
python mergeDataset.py
python splitDataset.py
```

即可


如果要生成bio格式的序列标注数据，修改``mergeDataset.py``中的bio标记为：

```python
bio = 1
```

即可
