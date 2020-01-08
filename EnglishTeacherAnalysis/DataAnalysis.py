import re

import inline as inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')
from pylab import mpl, matplotlib

#解决seaborn中文字体显示问题
mpl.rcParams['font.sans-serif'] = ['SimHei']
#把plt默认的图片size调大一点
plt.rc('figure', figsize=(10, 10))
plt.rcParams["figure.dpi"] =mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# %matplotlib inline



data_kdgd = pd.read_csv("幼儿园.csv")
data_pmsc = pd.read_csv("中小学.csv")
data_trn = pd.read_csv("外语培训.csv")
data_clg = pd.read_csv("职业院校.csv")
# data_tic = pd.read_csv("teachinchina.csv")
data_jlc = pd.read_csv("jobleadchina.csv")
# data_gm = pd.read_csv("groupmembers.csv")

data_kdgd.info()
# print(type(data_kdgd))
# print(data_kdgd.sample(5))
# print(data_kdgd.head(5))

# 把来自万行教师的四个数据集组合成一个Dataframe
data_kdgd['type'] = '幼儿园'
data_pmsc['type'] = '中小学'
data_trn['type'] = '外语培训'
data_clg['type'] = '职业院校'
data_wx = pd.concat([data_kdgd, data_pmsc, data_trn, data_clg])
data_wx.info()
# print(data_wx)
# print(type(data_kdgd['type']))
# print(data_kdgd.type)
data_series_kdgd_title = data_kdgd['title']
data_series_kdgd_type = data_kdgd['type']
data_series_kdgd_salary = data_kdgd['salary']
data_combin_kdgd = pd.concat([data_series_kdgd_title, data_series_kdgd_salary, data_series_kdgd_type], axis=1)
# print(data_combin_kdgd)
data_selected_kdgd = data_kdgd[['title', 'salary', 'type']]
# print(data_selected_kdgd)
data_selected_kdgd.to_csv('data_selected_kdgd.csv', sep='\t', encoding='utf-8', index='false')
data_combin_kdgd.to_csv('data_combin_kdgd.csv', sep='\t', encoding='utf-8', index='false')

# 万行教师数据清洗
# 清洗出省份、城市
# 经验、学历
# 工资

# 1. 清洗出省份、城市
# print(data_wx[['area', 'type']].sample(10))
data_wx_area = data_wx['area'].str.split('-', expand=True)
# print(data_wx_area)
# print(type(data_wx_area))
# print(data_wx_area[0])
data_wx['province'] = data_wx_area[0]
data_wx['city'] = data_wx_area[1]

data_wx.loc[data_wx['province'] == '北京', 'city'] = '北京'
data_wx.loc[data_wx['province'] == '上海', 'city'] = '上海'
data_wx.loc[data_wx['province'] == '天津', 'city'] = '天津'
data_wx.loc[data_wx['province'] == '重庆', 'city'] = '重庆'


# 2. 清洗出经验、学历
data_wx_exp_degree = data_wx['exp_title'].str.split('/', expand=True)
data_wx['exp'] = data_wx_exp_degree[0]
data_wx['degree'] = data_wx_exp_degree[1]
# print(type(data_wx['exp'].unique()))
degree_map = {'大专':'大专', '不限':'学历不限', '大学本科以上':'本科', '大学本科':'本科',
              '大专以上':'大专', '不限以上':'学历不限', '中专以上':'中专', '硕士以上':'硕士',
              '硕士':'硕士', '高中以上':'高中', '中专':'中专'}
data_wx['degree'] = data_wx['degree'].map(degree_map)
# print(data_wx.sample(5))
# data_wx.to_csv('data_wx.csv', sep='\t', encoding='utf-8', index='false')

# 3. 清洗出工资
print(data_wx['salary'].unique())
def get_salary(data):
    pat_K = r"(.*)K-(.*)K"
    pat_W = r"(.*)W-(.*)W"
    pat = r"(.*)-(.*)/"
    if '面议' in data:
        return np.nan
    if '享公办教师薪资待遇' in data:
        return np.nan
    if 'K' in data and '月' in data:
        low, high = re.findall(pattern=pat_K, string=data)[0]
        return (float(low)+float(high))/2
    if 'W' in data and '年' in data:
        low, high = re.findall(pattern=pat_W, string=data)[0]
        return (float(low)+float(high))/2*10/12
    if 'K' not in data and '月' in data:
        low, high = re.findall(pattern=pat, string=data)[0]
        return (float(low)+float(high))/2/1000

data_wx['salary_clean'] = data_wx['salary'].apply(get_salary)

print(data_wx['salary_clean'].sample(20))

data_wx['salary_clean'] = np.round(data_wx['salary_clean'], 1)
print(data_wx['salary_clean'].sample(20))