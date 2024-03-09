import re
import pandas as pd

# 初始化数据列表
data = []

# 打开并读取日志文件
with open('pump_n/logging_pump_n.txt', 'r') as file: #修改文件名
    for line in file:
        # 使用正则表达式匹配需要的数据
        match = re.search(r'pump:(\d+), dim:(\d+), f:(\d+), T\(单个pump\):\s+(\d+\.\d+)s, TT\(截止所有pump\):\s+(\d+\.\d+)s, quality:\s+(\d+\.\d+), \(r0/gh\):\s+(\d+\.\d+)', line)
        if match:
            # 如果匹配成功，将数据添加到列表中
            data.append([float(x) if '.' in x else int(x) for x in match.groups()])

# 创建pandas DataFrame
df = pd.DataFrame(data, columns=['pump', 'dim', 'f', 'T', 'TT', 'quality', 'approx_factor'])

# 将DataFrame保存为Excel文件
df.to_excel('pump_n_data.xlsx', index=False)