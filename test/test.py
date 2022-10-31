#!/usr/bin/env python3.8
# @Time:2022/4/9
# @Author:CarryLee
# @File:test.py
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
# 设置pandas输出时Unicode字符的对齐
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width',1000)
pd.set_option('display.max_columns',500)
pd.set_option('display.max_colwidth',20)

if __name__ == "__main__":
    # 建立测试数据并转化成DataFrame格式
    item_list = [['牛奶', '面包'],
                 ['面包', '尿布', '啤酒', '土豆'],
                 ['牛奶', '尿布', '啤酒', '可乐'],
                 ['面包', '牛奶', '尿布', '啤酒'],
                 ['面包', '牛奶', '尿布', '可乐']
                 ]
    # item_df = pd.DataFrame(item_list)
    print(item_list)
    # 数据格式处理，传入模型的数据需要满足bool值的格式
    te = TransactionEncoder()
    df_tf = te.fit_transform(item_list)
    df = pd.DataFrame(df_tf, columns=te.columns_)
    print(df)

    # 计算频繁项集
    # use_colnames=True表示使用元素名字，默认的False使用列名代表元素, 设置最小支持度min_support
    frequent_itemsets = apriori(df,min_support=0.05,use_colnames=True)
    frequent_itemsets.sort_values(by='support',ascending=False,inplace=True)
    # 选择2频繁项集
    # print(frequent_itemsets[frequent_itemsets.itemsets.apply(lambda x: len(x)) == 2])

    # 计算关联规则
    # metric可以有很多的度量选项，返回的表列名都可以作为参数
    # antecedents：规则先导项
    # consequents：规则后继项
    # antecedent support：规则先导项支持度
    # consequent support：规则后继项支持度
    # support：规则支持度 （前项后项并集的支持度）
    # confidence：规则置信度 （规则置信度：规则支持度support / 规则先导项）
    # lift：规则提升度，表示含有先导项条件下同时含有后继项的概率，与后继项总体发生的概率之比
    # leverage：规则杠杆率，表示当先导项与后继项独立分布时，先导项与后继项一起出现的次数比预期多多少
    # conviction：规则确信度，与提升度类似，但用差值表示
    association_rule = association_rules(frequent_itemsets,metric='confidence',min_threshold=0.9)
    association_rule.sort_values(by='lift', ascending=False, inplace=True)
    print(association_rule)