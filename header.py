#!/usr/bin/env python3.8
# @Time:2022/4/29
# @Author:CarryLee
# @File:header.py
import pandas as pd

# 根据《地表水环境质量标准GB3838-2002》中所列出的项目，value1到value5分别为Ⅰ类到Ⅴ类水质标准值
status1 = ['溶解氧', '高锰酸盐', 'COD', 'BOD', '氨氮', '总磷', '总氮', '铜', '锌', '氟化物', '硒', '砷', '汞', '镉', '六价铬', '铅', '氰化物',
           '挥发酚', '石油类', '阴离子表面活性剂', '硫化物', '粪大肠菌群']
status2 = ['溶解氧', '高锰酸盐', 'COD', 'BOD', '氨氮', '总磷', '总氮', '铜', '锌', '氟化物', '硒', '砷', '汞', '镉', '六价铬', '铅', '氰化物',
           '挥发酚', '石油类', '阴离子表面活性剂', '硫化物', '粪大肠菌群', '劣Ⅴ类', 'Ⅴ类', 'Ⅳ类', 'Ⅲ类']
values1 = [7.5, 2, 15, 3, 0.15, 0.01, 0.2, 0.01, 0.05, 1.0, 0.01, 0.05, 0.00005, 0.001, 0.01, 0.01, 0.005, 0.002,
           0.05, 0.2, 0.05, 200]
values2 = [6, 4, 15, 3, 0.5, 0.025, 0.5, 1.0, 1.0, 1.0, 0.01, 0.05, 0.00005, 0.005, 0.05, 0.01, 0.05, 0.002, 0.05,
           0.2, 0.1, 2000]
values3 = [5, 6, 20, 4, 1.0, 0.05, 1.0, 1.0, 1.0, 1.0, 0.01, 0.05, 0.0001, 0.005, 0.05, 0.05, 0.2, 0.005, 0.05, 0.2,
           0.2, 10000]
values4 = [3, 10, 30, 6, 1.5, 0.1, 1.5, 1.0, 2.0, 1.5, 0.02, 0.1, 0.001, 0.005, 0.05, 0.05, 0.2, 0.01, 0.5, 0.3,
           0.5, 20000]
values5 = [2, 15, 40, 10, 2.0, 0.2, 2.0, 1.0, 2.0, 1.5, 0.02, 0.1, 0.001, 0.01, 0.1, 0.1, 0.2, 0.1, 1.0, 0.3, 1.0,
           40000]


# 设置pandas输出格式
def set_pandas():
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_colwidth', 50)


# 获取数据集并进行预处理，填充Excel表格中的空白，将有些粪大肠菌群的数据中末尾所带的"L"给去掉
def get_dataset(name):
    dataSet = pd.read_excel(name, header=1, dtype=str)
    dataSet = dataSet.replace(['\n', ' '], '')
    dataSet = dataSet.replace('', '0')
    dataSet = dataSet.fillna(0)
    dataSet['粪大肠菌群个/L'] = dataSet['粪大肠菌群个/L'].str.replace('L', '', regex=True)
    return dataSet


# 内含检测时间、水温、pH、溶解氧、电导率、浊度、高锰酸盐浓度（每4行里有1行）、氨氮（每4行里有1行）、总磷（每4行里有1行）、总氮（每4行里有1行）、叶绿素和藻密度数据。仅作数据展示
def get_extra_dataset(path, option=1):
    dataSet1 = pd.merge(pd.read_excel(path + '/cpt2019_example.xls', header=1, dtype=str).drop(index=0),
                        pd.read_excel(path + '/cpt2020_example.xls', header=1, dtype=str).drop(index=0), how="outer")
    emptyDataSet = pd.DataFrame(data=dataSet1.iloc[:, 0], index=dataSet1.index, columns=['监测时间'])
    dataSet2 = pd.merge(pd.read_excel(path + '/gdzz2019_example.xls', header=1, dtype=str).drop(index=0),
                        pd.read_excel(path + '/gdzz2020_example.xls', header=1, dtype=str).drop(index=0), how="outer")
    dataSet2 = pd.merge(emptyDataSet, dataSet2, how="left", on="监测时间")
    dataSet3 = pd.merge(pd.read_excel(path + '/nlz2019_example.xls', header=1, dtype=str).drop(index=0),
                        pd.read_excel(path + '/nlz2020_example.xls', header=1, dtype=str).drop(index=0), how="outer")
    dataSet3 = pd.merge(emptyDataSet, dataSet3, how="left", on="监测时间")
    dataSet4 = pd.merge(pd.read_excel(path + '/qt2019_example.xls', header=1, dtype=str).drop(index=0),
                        pd.read_excel(path + '/qt2020_example.xls', header=1, dtype=str).drop(index=0), how="outer")
    dataSet4 = pd.merge(emptyDataSet, dataSet4, how="left", on="监测时间")
    dataSet5 = pd.merge(pd.read_excel(path + '/scd2019_example.xls', header=1, dtype=str).drop(index=0),
                        pd.read_excel(path + '/scd2020_example.xls', header=1, dtype=str).drop(index=0), how="outer")
    dataSet5 = pd.merge(emptyDataSet, dataSet5, how="left", on="监测时间")
    if option == 1:
        return dataSet1
    elif option == 2:
        return dataSet2
    elif option == 3:
        return dataSet3
    elif option == 4:
        return dataSet4
    else:
        return dataSet5
