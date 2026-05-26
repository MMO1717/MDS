
import torch
from torchvision import datasets
from torchvision.transforms import ToTensor

# 定义一个转换函数，将图片数据转换为张量（Tensor）
# 这就像一个转换器，把图片格式变成电脑能处理的数字网格
transform = ToTensor()

# 下载并加载训练数据
# root="data"：数据存放的目录
# train=True：表示这是训练集
# download=True：如果目录里没有数据，就自动下载
# transform=transform：应用我们上面定义的转换器
training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=transform,
)

# 下载并加载测试数据
test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=transform,
)

print(f"Fashion-MNIST 数据集已加载！")
print(f"训练集数量: {len(training_data)}")
print(f"测试集数量: {len(test_data)}")
print("-" * 30)

# --- 查看单条数据 ---
# 取出训练集中的第一张图片和它的标签
image, label = training_data[0]

# 创建一个标签数字到文本名称的映射，方便我们看懂
labels_map = {
    0: "T-Shirt",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle Boot",
}

print(f"第一张图片的详细信息：")
print(f"图片尺寸 (通道数, 高, 宽): {image.shape}")
print(f"标签数字: {label}")
print(f"标签名称: {labels_map[label]}")


def train_fashion_mnist(
    num_epochs=5,
    batch_size=64,
    learning_rate=1e-3,
    show_samples=True,
    sample_count=9,
):
    """训练一个简单的Fashion-MNIST分类器，并在需要时展示预测图像。"""
    from torch.utils.data import DataLoader

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.nn.Sequential(
        torch.nn.Flatten(),
        torch.nn.Linear(28 * 28, 256),
        torch.nn.ReLU(),
        torch.nn.Dropout(0.2),
        torch.nn.Linear(256, 10),
    ).to(device)

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    train_loader = DataLoader(training_data, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=batch_size)

    history = []

    def evaluate(loader):
        model.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for features, targets in loader:
                features = features.to(device)
                targets = targets.to(device)

                outputs = model(features)
                loss = criterion(outputs, targets)

                total_loss += loss.item() * features.size(0)
                predictions = outputs.argmax(dim=1)
                correct += (predictions == targets).sum().item()
                total += targets.size(0)

        avg_loss = total_loss / total
        accuracy = correct / total
        return avg_loss, accuracy

    for epoch in range(1, num_epochs + 1):
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for features, targets in train_loader:
            features = features.to(device)
            targets = targets.to(device)

            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * features.size(0)
            predictions = outputs.argmax(dim=1)
            correct += (predictions == targets).sum().item()
            total += targets.size(0)

        train_loss = total_loss / total
        train_acc = correct / total
        val_loss, val_acc = evaluate(test_loader)

        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "train_acc": train_acc,
                "val_loss": val_loss,
                "val_acc": val_acc,
            }
        )

        print(
            f"Epoch {epoch:02d} | "
            f"train_loss={train_loss:.4f} train_acc={train_acc * 100:.2f}% | "
            f"val_loss={val_loss:.4f} val_acc={val_acc * 100:.2f}%"
        )

    if show_samples:
        _visualize_predictions(model, device, sample_count)

    return model, history


def _visualize_predictions(model, device, sample_count=9):
    """展示模型在测试集上的若干预测结果。"""
    import math
    import matplotlib.pyplot as plt

    sample_count = max(1, min(sample_count, len(test_data)))
    indices = torch.randperm(len(test_data))[:sample_count]

    images = []
    labels = []
    for idx in indices:
        img, target = test_data[int(idx)]
        images.append(img)
        labels.append(int(target))

    batch = torch.stack(images).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(batch)
        predictions = outputs.argmax(dim=1).cpu().tolist()

    cols = min(3, sample_count)
    rows = math.ceil(sample_count / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for ax, img, true_label, pred_label in zip(
        axes, images, labels, predictions
    ):
        ax.imshow(img.squeeze().cpu().numpy(), cmap="gray")
        ax.set_title(
            f"真:{labels_map[true_label]}\n预测:{labels_map[pred_label]}",
            fontsize=9,
        )
        ax.axis("off")

    for ax in axes[len(images) :]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()
