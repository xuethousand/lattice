import re
import pandas as pd #pip install openpyxl


dim = 67

# 读取日志文件
with open(f'log_{dim}.txt', 'r') as file:
    content = file.read()

# 使用正则表达式匹配关键信息
pattern = r"norm\(\|sv\|\) (\d+\.\d+), appro_factor (\d+\.\d+), 2\*log\(det\) (\d+\.\d+), cpu time (\d+\.\d+), wall time (\d+\.\d+)"
matches = re.findall(pattern, content)

# 将匹配的信息转换为pandas DataFrame
df = pd.DataFrame(matches, columns=['norm', 'appro_factor', '2*log(det)', 'cpu_time', 'wall_time'])
# 将字符串转换为浮点数
df = df.astype(float)
# 将DataFrame保存为Excel文件
df.to_excel(f'data_{dim}.xlsx')