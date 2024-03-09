import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.distributions.empirical_distribution import ECDF #pip install statsmodels




dim = 47
goal_appro_factor = 0.86
plot = True


def generate_vector(filename):
    factors = []
    count = 0
    with open(filename, 'r') as file:
        for line in file:
            if 'appro_factor' in line:
                _1, _2, _3, value, _5, _6, _7, _8, _9, _10, _11, _12 = line.split()
                value = float(value.strip(','))  # 去掉末尾的逗号并转换为浮点数
                if(value < 1.1):
                    factors.append(value) #有时会出现approx factor极大的情况，见dim47，seed73124，这是算法有误
                count += 1
                if count == 500: #调整count，选择读取多少数据
                    break
    return np.array(factors)

v = generate_vector(f'log_{dim}.txt')




# 计算偏度
skewness = stats.skew(v)
print(f'偏度: {skewness}')
print(f'均值: {np.mean(v)}')
print(f'标准差: {np.std(v)}')

# 如果偏度小于0，则数据为左偏分布
if skewness < 0:
    print('数据集 v 是左偏分布的。')
else:
    print('数据集 v 不是左偏分布的。')


# 进行 Shapiro-Wilk 测试检验正态性
shapiro_test = stats.shapiro(v)
#print(f'Shapiro-Wilk 测试结果: {shapiro_test}')

# 如果 p 值小于0.05，则拒绝正态分布的假设
if shapiro_test.pvalue < 0.05:
    print('数据集 v 不服从正态分布。')
else:
    print('数据集 v 服从正态分布。')


if(plot):
    # 绘制直方图
    ## appro_factor 是左偏分布
    sns.histplot(v, bins=int(2000/5), color='blue', kde=True, edgecolor='black', linewidth=2)
    plt.title('')
    plt.xlabel('appro_factor')
    plt.ylabel('Density')
    plt.xlim([0.85, 1.1])
    # 添加垂直线
    plt.axvline(x=goal_appro_factor, color='r', linestyle='--')
    plt.savefig(f'distribution_{dim}.jpg', format='jpeg')
    plt.clf()






# 使用Box-Cox变换
v_transformed, lamda = stats.boxcox(v)   #v_transformed = (v**lamda - 1)/lamda 
print(f'lamda: {lamda}')
goal_appro_factor_transformed = (goal_appro_factor**lamda - 1)/lamda

# 再次用进行 Shapiro-Wilk 测试检验正态性
shapiro_test = stats.shapiro(v_transformed)
if shapiro_test.pvalue < 0.05:
    print('数据集 v after boxcox 不服从正态分布。')
else:
    print('数据集 v after boxcox 服从正态分布。')


if(plot):
    # 绘制直方图
    ## appro_factor after boxcox
    sns.histplot(v_transformed, bins=int(180/5), color='blue', kde=True, edgecolor='black', linewidth=2)
    plt.title('')
    plt.xlabel('appro_factor after boxcox')
    plt.ylabel('Density')
    # 添加垂直线
    plt.axvline(x=goal_appro_factor_transformed, color='r', linestyle='--')
    plt.savefig(f'distribution_transformed{dim}.jpg', format='jpeg')
    plt.clf()


# 计算变换后的数据小于goal_appro_factor的概率
probability = stats.norm.cdf(goal_appro_factor_transformed, loc=np.mean(v_transformed), scale=np.std(v_transformed))
print("dim:", dim)
print(f'变换后v < {goal_appro_factor} 的概率是: {probability}',f'需要{1/probability}次实验才能找到一个比目标更短的向量')
print(f'loc (mean of v_transformed) is: {np.mean(v_transformed)}')
print(f'scale (standard deviation of v_transformed) is: {np.std(v_transformed)}')