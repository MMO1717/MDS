# Seq2Seq + Attention 模型详解

## 1. 宏观视角：我们在做什么？

我们要把一个序列（比如英文句子 "I love you"）转换成另一个序列（比如法文句子 "Je t'aime"）。

*   **输入**：`X` (源序列，长度 $T$)
*   **输出**：`Y` (目标序列，长度 $T'$)

这就需要两个主要部分：
1.  **编码器 (Encoder)**：负责“读懂”源句子。
2.  **解码器 (Decoder)**：负责“写出”目标句子。

---

## 2. 编码器 (Encoder)：读懂源句子

编码器就是一个 RNN（通常是 GRU 或 LSTM）。

*   **输入**：源句子 `X`，形状 `(batch_size, num_steps)`。
*   **处理**：
    1.  **Embedding**：把每个单词变成一个向量。
    2.  **RNN**：一步步读入单词向量，更新自己的**隐藏状态 (Hidden State)**。
*   **输出**：
    1.  **`outputs` (所有时刻的隐藏状态)**：
        *   形状：`(num_steps, batch_size, num_hiddens)`
        *   含义：这是编码器对**每个单词**的理解。比如第 1 个时刻的 output 包含了 "I" 的信息，第 2 个时刻包含了 "I" 和 "love" 的信息（因为 RNN 有记忆）。
        *   **关键点**：这就是 Attention 机制中的 **Key (K)** 和 **Value (V)**。
    2.  **`state` (最后一个时刻的隐藏状态)**：
        *   形状：`(num_layers, batch_size, num_hiddens)`
        *   含义：这是编码器读完整个句子后的“总结”。
        *   **作用**：它将作为解码器的**初始状态**。

---

## 3. 注意力机制 (Attention)：核心魔法

在普通的 Seq2Seq 中，解码器只能看到编码器的**最后一个状态**（那个“总结”）。如果句子很长，这个“总结”可能会丢失很多细节。

**Attention 的作用**：让解码器在生成每个词时，都能**回头看一遍**源句子的所有单词（`outputs`），并挑出当前最相关的部分。

### 具体步骤（以加性注意力为例）：

假设解码器现在要生成第 $t$ 个词。

1.  **Query (Q)**：解码器在 $t-1$ 时刻的隐藏状态 $s_{t-1}$。
    *   含义：“我现在生成到了这一步，我想找点相关的信息。”
    *   形状：`(batch_size, 1, num_hiddens)`

2.  **Key (K) & Value (V)**：编码器的所有输出 `outputs`。
    *   含义：源句子每个单词的信息。
    *   形状：`(batch_size, num_steps, num_hiddens)`

3.  **计算分数 (Score)**：
    *   把 $Q$ 和每个 $K$ 进行比较（通过线性变换和 tanh 激活函数）。
    *   公式：$score = v^T \tanh(W_q Q + W_k K)$
    *   含义：计算解码器当前状态与源句子每个单词的**匹配程度**。

4.  **计算权重 (Attention Weights)**：
    *   对分数做 **Softmax**。
    *   含义：把分数变成概率（加起来等于 1）。比如对 "I love you"，权重可能是 `[0.1, 0.8, 0.1]`，说明当前最关注 "love"。
    *   **Masked Softmax**：如果源句子有填充（Padding），我们要把填充部分的权重设为 0，不关注它们。

5.  **计算上下文向量 (Context Vector)**：
    *   用权重对 $V$ 进行加权求和。
    *   $Context = \sum (weight_i \times V_i)$
    *   含义：这就是解码器当前最需要的源句子信息（比如主要包含了 "love" 的含义）。
    *   形状：`(batch_size, 1, num_hiddens)`

---

## 4. 解码器 (Decoder)：写出目标句子

解码器也是一个 RNN。

*   **输入**：
    1.  **`X`**：上一个生成的词（或者训练时的真实标签）。
    2.  **`state`**：解码器自己的隐藏状态。
    3.  **`enc_outputs`**：编码器的输出（用于 Attention）。

*   **处理流程（Forward）**：
    对于每一个时间步 $t$：
    1.  **准备 Query**：取上一步的隐藏状态 `state[-1]`。
    2.  **计算 Context**：用 Query 去 `enc_outputs` 里找信息（Attention），得到 `context`。
    3.  **拼接 (Concatenate)**：
        *   把当前输入的词向量 `embed(x)` 和 `context` 拼在一起。
        *   含义：解码器不仅看到了“上一个词”，还看到了“源句子的相关信息”。
        *   形状：`(batch_size, 1, embed_size + num_hiddens)`
    4.  **RNN 更新**：
        *   把拼接后的向量扔进 GRU。
        *   更新解码器的隐藏状态 `state`。
        *   得到输出 `out`。
    5.  **预测**：
        *   把 `out` 通过全连接层，映射到词表大小。
        *   得到预测概率分布（比如下一个词是 "Je" 的概率是 0.9）。

---

## 5. 训练过程 (Training)

1.  **Teacher Forcing**：
    *   在训练时，我们不使用解码器上一步预测的词作为下一步的输入（因为刚开始预测的很烂）。
    *   我们直接把**真实的标签**（Ground Truth）作为输入。
    *   比如目标是 "Je t'aime"，我们给解码器的输入序列是 `[<bos>, Je, t'aime]`，期望输出是 `[Je, t'aime, <eos>]`。

2.  **计算损失**：
    *   把解码器的预测结果 `Y_hat` 和真实标签 `Y` 做对比（CrossEntropy）。
    *   **Masking**：同样，我们要忽略掉填充部分的损失。

3.  **反向传播**：
    *   计算梯度，更新所有参数（编码器、解码器、Attention 层）。

---

## 总结：数据流向图

1.  **源句子** $\rightarrow$ **编码器** $\rightarrow$ **Key/Value (所有隐藏状态)**
2.  **解码器初始状态** $\leftarrow$ **编码器最终状态**
3.  **解码器循环**：
    *   **上一时刻状态 (Query)** $+$ **Key/Value** $\xrightarrow{Attention}$ **上下文向量 (Context)**
    *   **上下文向量** $+$ **当前输入词** $\rightarrow$ **RNN** $\rightarrow$ **新状态 & 输出**
    *   **输出** $\rightarrow$ **预测下一个词**
