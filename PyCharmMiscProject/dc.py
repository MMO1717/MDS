import csv
import os


def generate_table():
    # 定义表格表头
    headers = ["对比维度", "传统硬件方案 (长亮补光)", "岐黄智诊方案 (TRIZ时间分离)"]

    # 定义表格数据（这正是您PPT这一页需要向评委展示的核心逻辑）
    data = [
        ["物理矛盾应对", "无法调和：光强引发反光，光弱导致偏色", "运用 原理1(分割) 与 原理19(周期性作用)"],
        ["光照策略 (时间维)", "持续固定光源长时间照射 (连续态)", "毫秒级多频闪光 (暗光+强光 时间分割)"],
        ["特征提取 (空间维)", "色差与高光反光同时存在，特征相互掩盖", "暗光提取真实本色，强光穿透反光提取沟壑纹理"],
        ["底层融合算法", "脏数据直接输入模型，准确率极低", "纯净切片数据HDR时序融合，重构3D真实舌象"],
        ["最终效果", "基层复杂环境下，识别准确率断崖式下降", "彻底消除环境光与反光干扰，获取医疗级纯净数据"]
    ]

    # 1. 在控制台打印 Markdown 格式表格
    print("========== 岐黄智诊 TRIZ 核心突破对比表 ==========\n")
    # 打印表头
    print(f"| {headers[0]:<15} | {headers[1]:<30} | {headers[2]:<35} |")
    print("|" + "-" * 17 + "|" + "-" * 32 + "|" + "-" * 37 + "|")
    # 打印数据行
    for row in data:
        print(f"| {row[0]:<15} | {row[1]:<30} | {row[2]:<35} |")
    print("\n==================================================\n")

    # 2. 生成 HTML 文件 (为了方便直接复制粘贴到 PPT)
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
                font-family: 'Microsoft YaHei', sans-serif;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px 15px;
                text-align: center;
            }
            th {
                background-color: #0056b3;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            td:first-child {
                font-weight: bold;
                background-color: #e9ecef;
                color: #333;
            }
            td:last-child {
                color: #0056b3;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h2 style="font-family: 'Microsoft YaHei', sans-serif; text-align: center; color: #333;">岐黄智诊 - 分割原理(时间分离) 核心突破</h2>
        <table>
            <thead>
                <tr>
"""
    # 拼接表头 HTML
    for header in headers:
        html_content += f"                    <th>{header}</th>\n"
    html_content += """                </tr>
            </thead>
            <tbody>
"""
    # 拼接数据 HTML
    for row in data:
        html_content += "                <tr>\n"
        for item in row:
            html_content += f"                    <td>{item}</td>\n"
        html_content += "                </tr>\n"

    html_content += """            </tbody>
        </table>
    </body>
    </html>
"""

    html_filename = "triz_presentation_table.html"
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ 成功！已在当前目录生成网页文件：{html_filename}")
    print(f"👉 使用方法：双击打开 {html_filename}，按 Ctrl+A 全选网页中的表格，然后直接 Ctrl+V 粘贴到您的 PPT 中即可！")


if __name__ == "__main__":
    generate_table()