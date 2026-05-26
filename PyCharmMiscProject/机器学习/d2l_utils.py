import torch
from IPython import display
from d2l import torch as d2l
import collections
import re
import random
import os
import requests
import hashlib

# 定义 DATA_HUB，用于存储数据集的 URL 和 SHA-1 哈希值
DATA_HUB = dict()
DATA_URL = 'http://d2l-data.s3-accelerate.amazonaws.com/'

# 注册 time_machine 数据集
DATA_HUB['time_machine'] = (DATA_URL + 'timemachine.txt',
                                '090b5e7e70c295757f55df93cb0a180b9691891a')

def download(name, cache_dir=os.path.join('..', 'data')):
    """下载一个DATA_HUB中的文件，返回本地文件名"""
    # 确保请求的数据集在 DATA_HUB 中注册过
    assert name in DATA_HUB, f"{name} 不在 {DATA_HUB} 中"
    url, sha1_hash = DATA_HUB[name]
    # 创建缓存目录（如果不存在）
    os.makedirs(cache_dir, exist_ok=True)
    # 获取文件名
    fname = os.path.join(cache_dir, url.split('/')[-1])
    # 如果文件已存在，检查其哈希值
    if os.path.exists(fname):
        sha1 = hashlib.sha1()
        with open(fname, 'rb') as f:
            while True:
                data = f.read(1048576) # 每次读取 1MB
                if not data:
                    break
                sha1.update(data)
        # 如果哈希值匹配，说明文件完整，直接返回文件名
        if sha1.hexdigest() == sha1_hash:
            return fname  # 命中缓存
    # 如果文件不存在或哈希值不匹配，则下载文件
    print(f'正在从{url}下载{fname}...')
    r = requests.get(url, stream=True, verify=True)
    with open(fname, 'wb') as f:
        f.write(r.content)
    return fname

# 定义一个累加器类，用于累加多个变量
class Accumulator:
    """在n个变量上累加"""
    def __init__(self, n):
        self.data = [0.0] * n  # 初始化 n 个变量为 0

    def add(self, *args):
        # 将传入的参数和内部的 data 逐元素相加
        self.data = [a + float(b) for a, b in zip(self.data, args)]

    def reset(self):
        # 重置所有变量为 0
        self.data = [0.0] * len(self.data)

    def __getitem__(self, idx):
        # 通过索引获取 data 中的值
        return self.data[idx]

# 定义计算准确率的函数
def accuracy(y_hat, y):
    """计算预测正确的数量"""
    # 如果 y_hat 的维度大于 1 并且形状的第二个维度大于 1
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        # 沿着维度 1 找最大值的索引，即找到每个样本预测概率最大的类别
        y_hat = y_hat.argmax(axis=1)
    # 将 y_hat 的数据类型转换为和 y 一样
    cmp = y_hat.type(y.dtype) == y
    # 返回预测正确的数量
    return float(cmp.type(y.dtype).sum())

# 定义评估模型在任意数据集上精度的函数
def evaluate_accuracy(net, data_iter):
    """计算在指定数据集上模型的精度"""
    # 判断 net 是否是 torch.nn.Module 的实例
    if isinstance(net, torch.nn.Module):
        net.eval()  # 将模型设置为评估模式
    metric = Accumulator(2)  # 创建一个有两个变量的累加器，分别用于存储正确预测数和预测总数
    with torch.no_grad():  # 在这个代码块中不计算梯度
        for X, y in data_iter:
            # 累加正确预测数和总预测数
            metric.add(accuracy(net(X), y), y.numel())
    # 返回准确率
    return metric[0] / metric[1]

# 定义一个训练周期的函数
def train_epoch_ch3(net, train_iter, loss, updater):
    """训练模型一个迭代周期（定义见第3章）"""
    # 将模型设置为训练模式
    if isinstance(net, torch.nn.Module):
        net.train()
    # 训练损失总和、训练准确度总和、样本数
    metric = Accumulator(3)
    for X, y in train_iter:
        # 计算梯度并更新参数
        y_hat = net(X)
        l = loss(y_hat, y)
        if isinstance(updater, torch.optim.Optimizer):
            # 使用PyTorch内置的优化器和损失函数
            updater.zero_grad()  # 梯度清零
            l.mean().backward()  # 反向传播计算梯度
            updater.step()  # 更新参数
        else:
            # 使用定制的优化器和损失函数
            l.sum().backward()
            updater(X.shape[0])
        metric.add(float(l.sum()), accuracy(y_hat, y), y.numel())
    # 返回训练损失和训练精度
    return metric[0] / metric[2], metric[1] / metric[2]

# 定义一个动画绘制器类
class Animator:
    """在动画中绘制数据"""
    def __init__(self, xlabel=None, ylabel=None, legend=None, xlim=None,
                 ylim=None, xscale='linear', yscale='linear',
                 fmts=('-', 'm--', 'g-.', 'r:'), nrows=1, ncols=1,
                 figsize=(3.5, 2.5)):
        # 增量地绘制多条线
        if legend is None:
            legend = []
        d2l.use_svg_display()
        self.fig, self.axes = d2l.plt.subplots(nrows, ncols, figsize=figsize)
        if nrows * ncols == 1:
            self.axes = [self.axes]  # 将单个 Axes 包装成列表，统一处理
        self.X, self.Y, self.fmts = None, None, fmts
        self._xlabel = xlabel
        self._ylabel = ylabel
        self._legend = legend
        self._xlim = xlim
        self._ylim = ylim
        self._xscale = xscale
        self._yscale = yscale

    def add(self, x, y):
        # 向图表中添加多个数据点
        if not hasattr(y, "__len__"):
            y = [y]
        n = len(y)
        if not hasattr(x, "__len__"):
            x = [x] * n
        if not self.X:
            self.X = [[] for _ in range(n)]
        if not self.Y:
            self.Y = [[] for _ in range(n)]
        for i, (a, b) in enumerate(zip(x, y)):
            if a is not None and b is not None:
                self.X[i].append(a)
                self.Y[i].append(b)
        self.axes[0].cla()
        for x, y, fmt in zip(self.X, self.Y, self.fmts):
            self.axes[0].plot(x, y, fmt)
        # 设置每个子图的坐标轴参数
        xlabel = self._xlabel
        ylabel = self._ylabel
        legend = self._legend
        xlim = self._xlim
        ylim = self._ylim
        xscale = self._xscale
        yscale = self._yscale
        for ax in self.axes:
            d2l.set_axes(ax, xlabel, ylabel, xlim, ylim, xscale, yscale, legend)
        display.display(self.fig)
        display.clear_output(wait=True)

# 定义完整的训练函数
def train_ch3(net, train_iter, test_iter, loss, num_epochs, updater):
    """训练模型（定义见第3章）"""
    history = {"train_loss": [], "train_acc": [], "test_acc": []}
    animator = Animator(xlabel='epoch', xlim=[1, num_epochs], ylim=[0.3, 0.9],
                        legend=['train loss', 'train acc', 'test acc'])
    for epoch in range(num_epochs):
        train_metrics = train_epoch_ch3(net, train_iter, loss, updater)
        test_acc = evaluate_accuracy(net, test_iter)
        animator.add(epoch + 1, train_metrics + (test_acc,))
        train_loss, train_acc = train_metrics
        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["test_acc"].append(test_acc)
    print("\n训练结果汇总：")
    for i in range(num_epochs):
        print(f"第{i+1}轮 -> 训练损失: {history['train_loss'][i]:.4f}, "
              f"训练准确率: {history['train_acc'][i]:.4f}, "
              f"测试准确率: {history['test_acc'][i]:.4f}")
    train_loss, train_acc = history["train_loss"][-1], history["train_acc"][-1]
    test_acc = history["test_acc"][-1]
    # assert train_loss < 0.5, train_loss
    # assert train_acc <= 1 and train_acc > 0.7, train_acc
    # assert test_acc <= 1 and test_acc > 0.7, test_acc
    return history

def _read_time_machine():
    """将时间机器数据集加载到文本行的列表中"""
    # 使用本地定义的 download 函数下载并读取文件
    with open(download('time_machine'), 'r') as f:
        lines = f.readlines()
    # 将非字母字符替换为空格，并转换为小写
    return [re.sub('[^A-Za-z]+', ' ', line).strip().lower() for line in lines]

def tokenize(lines, token='word'):
    """将文本行拆分为单词或字符词元"""
    if token == 'word':
        # 按单词拆分
        return [line.split() for line in lines]
    elif token == 'char':
        # 按字符拆分
        return [list(line) for line in lines]
    else:
        print('错误：未知词元类型：' + token)

class Vocab:
    """文本词表"""
    def __init__(self, tokens=None, min_freq=0, reserved_tokens=None):
        if tokens is None:
            tokens = []
        if reserved_tokens is None:
            reserved_tokens = []
        # 统计词频并按出现频率排序
        counter = count_corpus(tokens)
        self._token_freqs = sorted(counter.items(), key=lambda x: x[1],
                                   reverse=True)
        # 初始化词表，未知词元 <unk> 的索引为 0
        self.idx_to_token = ['<unk>'] + reserved_tokens
        self.token_to_idx = {token: idx
                             for idx, token in enumerate(self.idx_to_token)}
        # 将满足最小频率要求的词元添加到词表中
        for token, freq in self._token_freqs:
            if freq < min_freq:
                break
            if token not in self.token_to_idx:
                self.idx_to_token.append(token)
                self.token_to_idx[token] = len(self.idx_to_token) - 1

    def __len__(self):
        # 返回词表长度
        return len(self.idx_to_token)

    def __getitem__(self, tokens):
        # 获取词元的索引，支持单个词元或词元列表
        if not isinstance(tokens, (list, tuple)):
            return self.token_to_idx.get(tokens, self.unk)
        return [self.__getitem__(token) for token in tokens]

    def to_tokens(self, indices):
        # 根据索引获取词元，支持单个索引或索引列表
        if not isinstance(indices, (list, tuple)):
            return self.idx_to_token[indices]
        return [self.idx_to_token[index] for index in indices]

    @property
    def unk(self):  # 未知词元的索引为0
        return 0

    @property
    def token_freqs(self):
        # 返回词频列表
        return self._token_freqs

def count_corpus(tokens):
    """统计词元的频率"""
    # 这里的tokens是1D列表或2D列表
    if len(tokens) == 0 or isinstance(tokens[0], list):
        # 将词元列表展平成一个列表
        tokens = [token for line in tokens for token in line]
    return collections.Counter(tokens)

def load_corpus_time_machine(max_tokens=-1):
    """返回时光机器数据集的词元索引列表和词表"""
    lines = _read_time_machine()
    tokens = tokenize(lines, 'char')
    vocab = Vocab(tokens)
    # 因为时光机器数据集中的每个文本行不一定是一个句子或一个段落，
    # 所以将所有文本行展平到一个列表中，并转换为索引
    corpus = [vocab[token] for line in tokens for token in line]
    if max_tokens > 0:
        corpus = corpus[:max_tokens]
    return corpus, vocab

def seq_data_iter_random(corpus, batch_size, num_steps):
    """使用随机抽样生成一个小批量子序列"""
    # 从随机偏移量开始对序列进行分区，随机范围包括num_steps-1
    corpus = corpus[random.randint(0, num_steps - 1):]
    # 减去1，是因为我们需要考虑标签
    num_subseqs = (len(corpus) - 1) // num_steps
    # 长度为num_steps的子序列的起始索引
    initial_indices = list(range(0, num_subseqs * num_steps, num_steps))
    # 在随机抽样的迭代过程中，
    # 来自两个相邻的、随机的、小批量中的子序列不一定在原始文本中相邻
    random.shuffle(initial_indices)

    def data(pos):
        # 返回从pos位置开始的长度为num_steps的序列
        return corpus[pos: pos + num_steps]

    num_batches = num_subseqs // batch_size
    for i in range(0, batch_size * num_batches, batch_size):
        # 在这里，initial_indices包含子序列的随机起始索引
        initial_indices_per_batch = initial_indices[i: i + batch_size]
        X = [data(j) for j in initial_indices_per_batch]
        Y = [data(j + 1) for j in initial_indices_per_batch]
        yield torch.tensor(X), torch.tensor(Y)

def seq_data_iter_sequential(corpus, batch_size, num_steps):
    """使用顺序分区生成一个小批量子序列"""
    # 从随机偏移量开始划分序列
    offset = random.randint(0, num_steps)
    num_tokens = ((len(corpus) - offset - 1) // batch_size) * batch_size
    Xs = torch.tensor(corpus[offset: offset + num_tokens])
    Ys = torch.tensor(corpus[offset + 1: offset + 1 + num_tokens])
    Xs, Ys = Xs.reshape(batch_size, -1), Ys.reshape(batch_size, -1)
    num_batches = Xs.shape[1] // num_steps
    for i in range(0, num_steps * num_batches, num_steps):
        X = Xs[:, i: i + num_steps]
        Y = Ys[:, i: i + num_steps]
        yield X, Y

class SeqDataLoader:
    """加载序列数据的迭代器"""
    def __init__(self, batch_size, num_steps, use_random_iter, max_tokens):
        if use_random_iter:
            self.data_iter_fn = seq_data_iter_random
        else:
            self.data_iter_fn = seq_data_iter_sequential
        self.corpus, self.vocab = load_corpus_time_machine(max_tokens)
        self.batch_size, self.num_steps = batch_size, num_steps

    def __iter__(self):
        return self.data_iter_fn(self.corpus, self.batch_size, self.num_steps)

def load_data_time_machine(batch_size, num_steps,
                           use_random_iter=False, max_tokens=10000):
    """返回时光机器数据集的迭代器和词表"""
    data_iter = SeqDataLoader(
        batch_size, num_steps, use_random_iter, max_tokens)
    return data_iter, data_iter.vocab
