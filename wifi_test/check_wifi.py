import csv
import pandas as pd
import matplotlib.pyplot as plt

with open('2.4Gwifi.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = next(reader)  # 读取第一行，即列名
    link_quality_index = header.index('          Link Quality=60/70  Signal level=-50 dBm  ')  # 找到“link quality”这一列的索引
    data = []
    for row in reader:
        link_quality_data = row[link_quality_index].split('=')[1].split('  ')[0]  # 提取“link quality”这一列中等号后面的数据
        Signal_level_data = row[link_quality_index].split('Signal level=')[1].split(' ')[0].strip()
        data_dir = {'Link Quality': link_quality_data, 'Signal Level': Signal_level_data}
        data.append(data_dir)

df = pd.DataFrame(data, columns=['Link Quality', 'Signal Level'])  # 将列表转换为DataFrame对象
link_quality = df['Link Quality'][0].split('/')[0]  # 提取Link Quality和Signal Level的数值
signal_level = df['Signal Level'][0]

link_quality = int(link_quality)  # 将数值转换为数字类型
signal_level = int(signal_level)

data = {'Link Quality': link_quality, 'Signal Level': signal_level}  # 创建一个包含Link Quality和Signal Level的字典

df = pd.DataFrame(data, index=[0])  # 将字典转换为DataFrame对象

#绘制Link Quality的直方图
df['Link Quality'].plot(kind='hist')
plt.title('Link Quality Histogram')
plt.xlabel('Link Quality')
plt.ylabel('Frequency')
plt.show()

# 绘制Signal Level的密度图
df['Signal Level'].plot(kind='density')
plt.title('Signal Level Density Plot')
plt.xlabel('Signal Level')
plt.ylabel('Density')
plt.show()
