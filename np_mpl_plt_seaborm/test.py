########导入模块
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style('darkgrid')

np.random.seed(sum(map(ord, "aesthetics")))


def mysinplot(flip=1):
    x = np.linspace(0, 14, 100)
    for i in range(1, 7):
        plt.plot(x, np.sin(x + i * .5) * (7 - i) * flip)


mysinplot()
plt.show()

########导入数据
names = [
       'mpg'
    ,  'cylinders'
    ,  'displacement'
    ,  'horsepower'
    ,  'weight'
    ,  'acceleration'
    ,  'model_year'
    ,  'origin'
    ,  'car_name'
]
# df = pd.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data", sep='\s+', names=names)
df = pd.read_csv("./auto-mpg.data", sep='\s+', names=names)
df['maker'] = df.car_name.map(lambda x: x.split()[0])
df.origin = df.origin.map({1: 'America', 2: 'Europe', 3: 'Asia'})
df=df.applymap(lambda x: np.nan if x == '?' else x).dropna()
df['horsepower'] = df.horsepower.astype(float)
df.head()

#1. 一般绘图函数：factorplot 和 FacetGrid
# （1）根据2个维度变量绘图，画出model_year和mpg的关系图
sns.factorplot(data=df, x="model_year", y="mpg")
plt.show()

#通过添加kind参数，折线图改柱形图
sns.factorplot(data=df, x="model_year", y="mpg",kind="bar")
plt.show()

#（2）可以按照第3个维度绘制不同的关系图
sns.factorplot(data=df, x="model_year", y="mpg", col="origin")
plt.show()

#（3）各种不同的图
#柱形图，添加密度函数
g = sns.FacetGrid(df, col="origin")
g.map(sns.distplot, "mpg")
plt.show()

#散点图
g = sns.FacetGrid(df, col="origin")
g.map(plt.scatter, "horsepower", "mpg")
plt.show()

#添加线性回归线
plt.xlim(0, 250)
plt.ylim(0, 60)
plt.show()

#KDE等高线
df['tons'] = (df.weight/2000).astype(int)
g = sns.FacetGrid(df, col="origin", row="tons")
g.map(sns.kdeplot, "horsepower", "mpg")
plt.xlim(0, 250)
plt.ylim(0, 60)
plt.show()

#2. 矩阵图 pairplot and PairGrid
#不添加回归线
g = sns.pairplot(df["mpg", "horsepower", "weight", "origin"], hue="origin", diag_kind="hist")
for ax in g.axes.flat:
    plt.setp(ax.get_xticklabels(), rotation=45)
plt.show()

#添加回归
g = sns.PairGrid(df["mpg", "horsepower", "weight", "origin"], hue="origin")
g.map_upper(sns.regplot)
g.map_lower(sns.residplot)
g.map_diag(plt.hist)
for ax in g.axes.flat:
    plt.setp(ax.get_xticklabels(), rotation=45)
g.add_legend()
g.set(alpha=0.5)

#3. 联合绘图jointplot and JointGrid
#kde等高图
sns.jointplot("mpg", "horsepower", data=df, kind='kde')
plt.show()

#添加线性回归的图
sns.jointplot("horsepower", "mpg", data=df, kind="reg")
plt.show()

#添加多元回归的图
g = sns.JointGrid(x="horsepower", y="mpg", data=df)
g.plot_joint(sns.regplot, order=2)
g.plot_marginals(sns.distplot)
plt.show()