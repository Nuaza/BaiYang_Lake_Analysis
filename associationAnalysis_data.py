#!/usr/bin/env python3.8
# @Time:2022/4/8
# @Author:CarryLee
# @File:associationAnalysis_data.py
# @Info:白洋淀水质检测数据关联分析，分析白洋淀各个监测数据间关联关系

import pandas as pd
from header import status1 as status
from header import values3
from header import get_dataset
from mlxtend.frequent_patterns import apriori, fpgrowth
from mlxtend.frequent_patterns import association_rules


def get_data(path):
    dataSet = get_dataset(path)
    line = dataSet.shape[0]  # 获取行数
    column = dataSet.shape[1] - 11  # 获取列数
    data = pd.DataFrame(index=[i for i in range(line)], columns=status)
    for i in range(line):
        if float(dataSet.loc[i][6]) < values3[0]:
            data.loc[i][0] = True
        else:
            data.loc[i][0] = False
        for j in range(7, column + 6):
            if float(dataSet.loc[i][j]) > values3[j - 6]:
                data.loc[i][j - 6] = True
            else:
                data.loc[i][j - 6] = False
    return data

def get_apriori_itemsets(path, min_support, sort_by):
    data = get_data(path)
    frequentItemSets = apriori(data, min_support=min_support, use_colnames=True)
    frequentItemSets.sort_values(by=sort_by, ascending=False, inplace=True)
    # 输出频繁2-项集
    # print(frequentItemSets[frequentItemSets.itemsets.apply(lambda x: len(x)) == 2])
    return frequentItemSets


def get_itemsets_without_frozenset(path, min_support, sort_by, algorithm="apriori", k=0):
    if algorithm == "apriori":
        frequentItemsets = get_apriori_itemsets(path, min_support, sort_by)
    else:
        frequentItemsets = get_fpgrowth_itemsets(path, min_support, sort_by)
    prod = []
    if k != 0:
        frequentItemsets = frequentItemsets[frequentItemsets.itemsets.apply(lambda x: len(x)) == k]
    for i in frequentItemsets['itemsets']:
        prod.append(str(i))
    new_set = [x.replace('frozenset', '').replace('})', '').replace('({', '').replace("'", "") for x in prod]
    frequentItemsets['itemsets'] = new_set
    return frequentItemsets


def get_fpgrowth_itemsets(path, min_support, sort_by):
    data = get_data(path)
    frequentItemSets = fpgrowth(data, min_support=min_support, use_colnames=True)
    frequentItemSets.sort_values(by=sort_by, ascending=False, inplace=True)
    return frequentItemSets


def get_association_rule(path, min_support=0.05):
    frequentItemSets = get_apriori_itemsets(path, min_support=min_support, sort_by='support')
    # 计算关联规则
    association_rule = association_rules(frequentItemSets, metric='confidence', min_threshold=0.9)
    association_rule.sort_values(by='lift', ascending=False, inplace=True)
    association_rule.columns = ['规则先导项', '规则后继项', '先导项支持度', '后继项支持度', '支持度', '置信度', '提升度', '杠杆率', '确信度']
    # 消去frozenset
    prod1, prod2 = [], []
    for i in association_rule['规则先导项']:
        prod1.append(str(i))
    for j in association_rule['规则后继项']:
        prod2.append(str(j))
    new_set1 = [x.replace('frozenset', '').replace('})', '').replace('({', '').replace("'", "") for x in prod1]
    new_set2 = [x.replace('frozenset', '').replace('})', '').replace('({', '').replace("'", "") for x in prod2]
    association_rule['规则先导项'], association_rule['规则后继项'] = new_set1, new_set2
    return association_rule


def print_rule_to_excel(association_rule, name):
    association_rule.to_excel('./result/' + name + '_关联规则分析结果.xlsx', index=False)