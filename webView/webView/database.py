#!/usr/bin/env python3.8
# @Time:2022/5/5
# @Author:CarryLee
# @File:database.py
import pandas as pd
from django.http import HttpResponse
from dataModel.models import *

# 导入上级模块
import sys

sys.path.append('..')
from header import get_dataset
from associationAnalysis_data import get_association_rule as get_rule1
from associationAnalysis_data import get_itemsets_without_frozenset as get_itemsets1
from associationAnalysis_standard import get_association_rule as get_rule2
from associationAnalysis_standard import get_itemsets_without_frozenset as get_itemsets2


def get_original_data():
    return get_dataset('./../data/example.xlsx')


def updateData(request):
    data = get_original_data()
    ass_rule1 = get_rule1(path='./../data/example.xlsx')
    ass_rule2 = get_rule2(path='./../data/example.xlsx')
    itemsets1 = get_itemsets1(path="./../data/example.xlsx", min_support=0.1, sort_by="support")
    itemsets2 = get_itemsets2(path="./../data/example.xlsx", min_support=0.05, sort_by="support")
    for i in range(data.shape[0]):
        OriginalData(id=i, 所属水系=data.loc[i][0], 所属城市=data.loc[i][1], 断面名称=data.loc[i][2], 日期=data.loc[i][3],
                     水温=data.loc[i][4], pH=data.loc[i][5], 溶解氧=data.loc[i][6], 高锰酸盐=data.loc[i][7],
                     COD=data.loc[i][8], BOD=data.loc[i][9], 氨氮=data.loc[i][10], 总磷=data.loc[i][11], 总氮=data.loc[i][12],
                     铜=data.loc[i][13], 锌=data.loc[i][14], 氟化物=data.loc[i][15], 硒=data.loc[i][16], 砷=data.loc[i][17],
                     汞=data.loc[i][18], 镉=data.loc[i][19], 六价铬=data.loc[i][20], 铅=data.loc[i][21], 氰化物=data.loc[i][22],
                     挥发酚=data.loc[i][23], 石油类=data.loc[i][24], 阴离子表面活性剂=data.loc[i][25], 硫化物=data.loc[i][26],
                     粪大肠菌群=data.loc[i][27], 水质类别=data.loc[i][32]).save()
    for j in range(ass_rule1.shape[0]):
        AssociationRulesWithData(id=j, antecedents=ass_rule1.loc[j][0], consequents=ass_rule1.loc[j][1],
                                 ant_support=round(ass_rule1.loc[j][2], 2), con_support=round(ass_rule1.loc[j][3], 2),
                                 support=round(ass_rule1.loc[j][4], 2), confidence=round(ass_rule1.loc[j][5], 2),
                                 lift=round(ass_rule1.loc[j][6], 2), leverage=round(ass_rule1.loc[j][7], 2),
                                 conviction=round(ass_rule1.loc[j][8], 2)).save()
    for k in range(ass_rule2.shape[0]):
        AssociationRulesWithStandard(id=k, antecedents=ass_rule2.loc[k][0], consequents=ass_rule2.loc[k][1],
                                     ant_support=round(ass_rule2.loc[k][2], 2),
                                     con_support=round(ass_rule2.loc[k][3], 2), support=round(ass_rule2.loc[k][4], 2),
                                     confidence=round(ass_rule2.loc[k][5], 2), lift=round(ass_rule1.loc[k][6], 2),
                                     leverage=round(ass_rule2.loc[k][7], 2), conviction=round(ass_rule2.loc[k][8], 2)).save()
    for l in range(itemsets1.shape[0]):
        FrequentItemsetsWithData(id=l, itemsets=itemsets1.loc[l][1], support=round(itemsets1.loc[l][0], 2)).save()
    for m in range(itemsets2.shape[0]):
        FrequentItemsetsWithStandard(id=m, itemsets=itemsets2.loc[m][1], support=round(itemsets2.loc[m][0], 2)).save()
    return HttpResponse("刷新数据成功!<a href='index'>点击返回主页面</a>")


def upload_data(file_path, min_support, option=1, algorithm="apriori"):
    # option为0更新原始数据，为1更新data的频繁项集数据，为2更新data的关联规则数据，为3更新standard的频繁项集数据，其它则更新standard的关联规则数据
    if option == 0:
        data = get_dataset(file_path)
        OriginalData.objects.all().delete()
        for i in range(data.shape[0]):
            OriginalData(id=i, 所属水系=data.loc[i][0], 所属城市=data.loc[i][1], 断面名称=data.loc[i][2], 日期=data.loc[i][3],
                         水温=data.loc[i][4], pH=data.loc[i][5], 溶解氧=data.loc[i][6], 高锰酸盐=data.loc[i][7],
                         COD=data.loc[i][8], BOD=data.loc[i][9], 氨氮=data.loc[i][10], 总磷=data.loc[i][11],
                         总氮=data.loc[i][12], 铜=data.loc[i][13], 锌=data.loc[i][14], 氟化物=data.loc[i][15],
                         硒=data.loc[i][16],
                         砷=data.loc[i][17], 汞=data.loc[i][18], 镉=data.loc[i][19], 六价铬=data.loc[i][20],
                         铅=data.loc[i][21], 氰化物=data.loc[i][22],
                         挥发酚=data.loc[i][23], 石油类=data.loc[i][24], 阴离子表面活性剂=data.loc[i][25], 硫化物=data.loc[i][26],
                         粪大肠菌群=data.loc[i][27], 水质类别=data.loc[i][32]).save()
    elif option == 1:
        itemsets1 = get_itemsets1(path=file_path, min_support=min_support, sort_by="support", algorithm=algorithm)
        FrequentItemsetsWithData.objects.all().delete()
        for l in range(itemsets1.shape[0]):
            FrequentItemsetsWithData(id=l, itemsets=itemsets1.loc[l][1], support=round(itemsets1.loc[l][0], 2)).save()
    elif option == 2:
        ass_rule1 = get_rule1(path=file_path, min_support=min_support)
        AssociationRulesWithData.objects.all().delete()
        for j in range(ass_rule1.shape[0]):
            AssociationRulesWithData(id=j, antecedents=ass_rule1.loc[j][0], consequents=ass_rule1.loc[j][1],
                                     ant_support=round(ass_rule1.loc[j][2], 2),
                                     con_support=round(ass_rule1.loc[j][3], 2),
                                     support=round(ass_rule1.loc[j][4], 2), confidence=round(ass_rule1.loc[j][5], 2),
                                     lift=round(ass_rule1.loc[j][6], 2), leverage=round(ass_rule1.loc[j][7], 2),
                                     conviction=round(ass_rule1.loc[j][8], 2)).save()
    elif option == 3:
        itemsets2 = get_itemsets2(path=file_path, min_support=min_support, sort_by="support", algorithm=algorithm)
        FrequentItemsetsWithStandard.objects.all().delete()
        for m in range(itemsets2.shape[0]):
            FrequentItemsetsWithStandard(id=m, itemsets=itemsets2.loc[m][1],
                                         support=round(itemsets2.loc[m][0], 2)).save()
    else:
        ass_rule2 = get_rule2(path=file_path, min_support=min_support)
        AssociationRulesWithStandard.objects.all().delete()
        for k in range(ass_rule2.shape[0]):
            AssociationRulesWithStandard(id=k, antecedents=ass_rule2.loc[k][0], consequents=ass_rule2.loc[k][1],
                                         ant_support=round(ass_rule2.loc[k][2], 2),
                                         con_support=round(ass_rule2.loc[k][3], 2),
                                         support=round(ass_rule2.loc[k][4], 2),
                                         confidence=round(ass_rule2.loc[k][5], 2), lift=round(ass_rule2.loc[k][6], 2),
                                         leverage=round(ass_rule2.loc[k][7], 2), conviction=round(ass_rule2.loc[k][8], 2)).save()


def updateArticle(request):
    Article(id=1, context='欢迎来到白洋淀监测数据关联分析可视化系统。本系统是根据Apriori'
                          '关联分析算法所计算挖掘出的频繁项集和关联规则，通过设置合理的支持度与置信度的阈值从而得到具有可信度的数据来进行的可视化展示。').save()
    Article(id=2, context='湿地是陆地生态系统和水生生态系统相互结合，作为二者的转换区而形成的独特的生态系统，是动植物赖以生存繁衍的重要环境，'
                          '也是自然界和生物圈中最富有生物多样性的生态系统。因其具有抵御洪水、改善气候、控制污染和美化环境等功能价值而被誉为“地球之肾”，'
                          '是我国华北平原为数不多并且面积巨大的淡水湖泊型湿地。2017年，中共中央、国务院正式设立雄安新区，'
                          '而白洋淀作为雄安新区的后花园，是其打造新时代生态文明典范城市的重要一部分，在区域生态体系的构建中也具有重要战略意义').save()
    Article(id=3, context='近些年以来，随着高强度人类活动的影响，白洋淀水域生态环境正面临着严峻的考验。部分入淀水量减少、淀区富营养化加剧、生物多样性降低，'
                          '淀区严重退化。因此，通过科学地分析白洋淀生态环境的变化趋势，明确主要影响因子，并通过大数据领域的关联分析法得到其中隐藏的规律，'
                          '便可为白洋淀水污染治理提供依据，也可以为雄安新区的生态环境建设与管理提供重要参考。').save()
    Article(id=4, context='本系统正是针对目前学术界对于白洋淀生态系统关联分析方面研究相对稀少的情况下而做出的。本系统主要根据生态监测的确切数据，'
                          '结合我国地表水环境质量标准，对白洋淀各个监测数据之间关联关系的分析，以及白洋淀生态状态与各个监测数据的关联分析的分析；'
                          '确定上述两点是否具有关联关系。然后运用经典的Apriori算法挖掘出数据的频繁项集，再从中产生关联规则。'
                          '根据关联规则，就可以推测出数据背后所隐藏的关系，研究出这些关联关系对生态保护的影响和建议。').save()
    Article(id=5, context='白洋淀位于河北省雄安新区境内，是华北平原最大的淡水湖泊湿地，享有“华北之肾”、“华北明珠”等美誉。').save()
    Article(id=6, context='白洋淀 (115°38′~116°09′E，38°43′~39°01′) 位于位于太行山前永定河和滹沱河冲积扇交汇处的扇缘洼地上，'
                          '属河海流域大清河南支水系，是华北地区最大的淡水湖泊。淀区由保定市、沧州市交界的143个相互联系的大小淀泊和3700多条沟壕构成，'
                          '总面积约为366km²，四周以堤坝为界限。').save()
    Article(id=7, context='白洋淀主要接纳瀑河、唐河、漕河、潴龙河、孝义河、清水河、府河、萍河及白沟引河九大河流入湖, 后经海河、大清河汇入渤海。'
                          '淀区正常蓄水量4亿吨, 湿地总面积约366平方千米, 呈西北高、东南低地势, 海拔跨度约2500m。流域四季分明,'
                          ' 属暖温带季风型大陆性半湿润半干旱气候，年平均温度为12.82℃、年平均降水量约为524.8mm。').save()
    Article(id=8, context='本次白洋淀监测数据主要采集自图中的采蒲台、光淀张庄、南刘庄、圈头以及烧车淀地区。').save()
    Article(id=9, context='随着信息时代的迅速发展，数据作为其中一种重要的传输载体，也正处于迅速发展的阶段当中。近年来，大数据作为其中的一个热点词汇，'
                          '也正逐步受人关注。大数据一词最早由美国学者阿尔温·托夫勒提出，他认为，信息化阶段是继农业阶段、工业阶段以来的第三次浪潮，'
                          '而大数据正是这第三次浪潮中的“华彩乐章”。大数据具有容量大（Volume）、类型多（Variety）、存取速度快（Velocity）、'
                          '应用价值高（Value）以及真实性（Veracity）的特点。时至今日，大数据已经被社会各界接受并广泛运用于日常生活之中，'
                          '对人们的生产、生活与思维方式产生越来越多的影响。').save()
    Article(id=10, context='但伴随着大数据而来的则是一系列的问题。例如，如何从大量的数据中获取到有效的、有价值的信息便是其中之一。'
                           '随着人们对这个问题研究的日益深入，一门基于大数据与数据库和人工智能的新领域——数据挖掘，便得以在近几年快速发展起来。').save()
    Article(id=11, context='数据挖掘即从数据库里的大量数据中，揭示出隐含的、先前未知的并且具有潜在利用价值的信息的过程。不管是为完整的信息，还是受到了干扰的信息，'
                           '数据挖掘都能通过对其数据的转换分析，或者对数据的模块化处理来进行识别和筛选操作，并提取和处理其中的有用信息。通过数据挖掘获取到的数据中的规律，'
                           '通常可以被广泛使用于市场分析、工程设计等各种应用，并为决策者提供合理且科学的数据分析报告，帮助其做出最优化的决策。').save()
    Article(id=12, context='目前常用于数据挖掘的有几个经典的算法，例如偏向人工智能与机器学习领域的神经网络法，偏向概率学与统计学的决策树法以及关联规则法等。'
                           '本系统就是根据关联分析方法获取到关联规则，从而实现数据挖掘的。').save()
    Article(id=13, context='温度与pH值在水质标准中没有确切的量纲').save()
    Article(id=14, context='对于水温而言，人为造成的环境水温变化应限制在：').save()
    Article(id=15, context='周平均最大温度升≤1').save()
    Article(id=16, context='周平均最大温度降≤2').save()
    Article(id=17, context='对于pH值而言，只要处于6~9的区间内就是正常的。').save()
    Article(id=18, context='溶解在水中的空气中的分子态氧称为溶解氧').save()
    Article(id=19, context='溶解氧的值是研究水体自净程度的依据。当水中的溶解氧被消耗后要恢复到正常状态时，若其所需时间较短，'
                           '则说明该水体的自净能力较强，或者水体污染不严重。反之则说明该水体污染较为严重，自净能力弱甚至无。').save()
    Article(id=20, context='按照Ⅲ类水质标准来进行对比的话，则图中正常溶解氧含量应该≥5mg/L，即橙色与红色的分界线。').save()
    Article(id=21, context='高锰酸盐指数为水体受亚铁盐、亚硝酸盐等还原性无机物质和有机物污染程度的相对条件性指标').save()
    Article(id=22, context='按照Ⅲ类水质标准，正常的高锰酸盐含量应该≤6mg/L，即图中的虚线部分。').save()
    Article(id=23, context='化学需氧量(COD)是使用化学方法测量水样中被氧化的还原性物质的量，在一定的条件下，'
                           '氧化1L水样中还原性物质所消耗的氧化剂的量，其直观地反映了水体受还原性物质污染的程度').save()
    Article(id=24, context='按照Ⅲ类水质标准，正常的化学需氧量应该≤20mg/L，即图中的虚线部分。').save()
    Article(id=25, context='生化需氧量(BOD)是指在特定条件下，微生物分解一定量的水中的可氧化物质所消耗的溶解氧的含量，'
                           '通常规定以5天为一个标准周期来测量生化需氧量，即BOD₅').save()
    Article(id=26, context='按照Ⅲ类水质标准，正常的五日生化需氧量应该≤4mg/L，即图中的虚线部分。').save()
    Article(id=27, context='以游离氨(NH₃)和铵离子(NH₄+)形式存在的化合氮即为氨氮。氨氮是水体中的营养素，可导致水体富营养化现象的产生，'
                           '是水体中的主要耗氧污染物，对鱼类和某些水生生物具有毒害').save()
    Article(id=28, context='按照Ⅲ类水质标准，正常的五日生化需氧量应该≤1.0mg/L，即图中的虚线部分。').save()
    Article(id=29, context='磷是生物生长的必要元素，但过量的磷含量会导致湖泊富营养化、浮游生物和淡水藻类大量繁殖、'
                           '水的含氧量下降以及水质恶化等问题').save()
    Article(id=30, context='按照Ⅲ类水质标准，正常的五日生化需氧量应该≤0.05mg/L，即图中的虚线部分。').save()
    Article(id=31, context='总氮作为水体监测分析中的常规因子，也是衡量水质污染的重要指标之一').save()
    Article(id=32, context='按照Ⅲ类水质标准，正常的五日生化需氧量应该≤1.0mg/L，即图中的虚线部分。').save()
    Article(id=33, context='所谓关联分析，其实就是事物集合之间的某种意义上的关联、联系。从大数据层面来理解的话，'
                           '就是在大量数据中挖掘项集的集合之间有所关联的事务以及其相关的联系').save()
    Article(id=34, context='假设一个数据项的全集为I=(I1 , I2 , … , Im )，数据集为D，设A和B为两个数据项集，并且为I的非空子集，'
                           '则形如A→B的式子就表示为一条关联规则。由多条关联规则组成的表格如下表所示：').save()
    Article(id=35, context='规则先导项(antecedents)：即关联规则A→B中的数据项集A，其可以包含一个或多个数据项').save()
    Article(id=36, context='规则后继项(consequences)：即关联规则A→B中的数据项集B，其可以包含一个或多个数据项').save()
    Article(id=37, context='规则先导项支持度(antecedent support)：即数据集D的事务中，出现数据项集A的概率P(A)').save()
    Article(id=38, context='规则后继项支持度(antecedent support)：即数据集D的事务中，出现数据项集B的概率P(B)').save()
    Article(id=39, context='支持度(support)：支持度即为数据集D的事务中，同时出现数据项集A和数据项集B的概率，'
                           '如A→B的支持度就是D中事务包含A∪B的概率').save()
    Article(id=40, context='置信度(confidence)：置信度即为数据集D的事务中，在包含了数据项集A的情况下包含了数据项集B的比例P(B | A)').save()
    Article(id=41, context='规则提升度(lift)：即表示含有规则先导项的条件下同时含有规则后继项的概率与后继项总体发生的概率之比，'
                           '即P(B | A) / P(B)。规则提升率通常可以用来揭示规则后继项对规则先导项所带来的变化程度').save()
    Article(id=42, context='规则杠杆率(leverage)：即表示当规则先导项与规则后继项独立分布时，规则先导项与规则后继项一起出现的次数比预期多多少的程度').save()
    Article(id=43, context='规则确信度(conviction)：若规则置信度为100%，则规则确信度为无限大。否则的话，则可以用来表示该规则在多大程度上是可信的').save()
    Article(id=44, context='强关联规则：对于一个关联规则A →B，我们预先设定好一个最小支持度min_sup和一个最小置信度min_conf，'
                           '如果该关联规则的支持度大于阈值min_sup且置信度大于阈值min_conf，则我们可以称其为强关联规则').save()
    Article(id=45, context='频繁项集(frequent itemset)：在一个项目集合中，若其包含k个项目，则我们称其为k-项集，通常记作Lk。'
                           '对于满足最小支持度的项集，就称之为频繁项集。若一个频繁项集的内部只包含有k-项集，则该频繁项集也被称为频繁k-项集').save()
    Article(id=46, context='候选项集：候选k-项集通常记作Ck，是通过Lk-1连接而形成的。在Ck中，还需要进行剪枝操作，就能够获取到Lk').save()
    Article(id=47, context='Apriori算法属于一种深层逐层搜索算法，是关联规则挖掘中最为著名且使用量最大的一个算法').save()
    Article(id=48, context='Apriori算法的基本思路为，通过多次扫描数据库，生成频繁k-项集，通过自连接生成候选k+1-项集，'
                           '再通过剪枝获取到频繁k+1-项集…最终生成最大频繁项集的过程。详细步骤如下：').save()
    Article(id=49, context='首先对数据库D进行一次扫描，对于I中的每一个项集I1 , I2 , … , In，统计每项在数据库中出现的次数。'
                           '将项目中小于最小支持度阈值的项给丢弃掉，剩余的项目组成L1').save()
    Article(id=50, context='继续迭代，通过Lk-1来计算Lk。其策略为建立k-候选集：通过Lk-1与包括自身在内的项进行连接以生成Ck').save()
    Article(id=51, context='进行Ck的剪枝操作，若c∈Ck且c不在Lk-1中，则将项目c给删除掉').save()
    Article(id=52, context='扫描数据库，统计Ck中各项集中项的出现次数，丢弃掉不满足支持度阈值的项集，得到Lk').save()
    Article(id=53, context='重复以上2-4步骤，直到Lk为空集').save()
    Article(id=54, context='对L1到Lk取并集，以获取所有的频繁项集的集合L').save()
    Article(id=55, context='FP-growth算法设计了一种被称之为频繁模式树(FP-tree)的数据结构，通过树的特点，将原始数据进行压缩存储').save()
    Article(id=56, context='由于Apriori算法在产生频繁项集的过程中，需要对数据库进行多次扫描，同时产生大量的中间项集，'
                           '这就使得Apriori算法的时间复杂度和空间复杂度较大。由此而产生了一种新的优化过的算法，即FP-growth算法。').save()
    Article(id=57, context='FP-tree的根节点为“null”，其余节点代表一个特征项及其支持度信息，每一个项集对应树上的一条路径。'
                           '为了能够更加快速地挖掘频繁项集，FP-tree还包含了一个含有两列的频繁项表，第一列为特征项名称，'
                           '按照特征项支持度降序排序；第二列存储为一个链表，将FP-tree中相同特征项的结点连接起来。'
                           'FP-growth算法主要分为构建FP-tree和基于FP-tree进行递归的挖掘频繁项两个步骤，其具体步骤如下：').save()
    Article(id=58, context='首先扫描数据库D，计算每一个特征值的支持度并降序排序，与min_sup阈值相对比过滤掉不满足要求的项，得到L1').save()
    Article(id=59, context='创建FP-tree的根节点记作T，内容为 “null” ，创建频繁项表并将各个链表设置为空').save()
    Article(id=60, context='按照L1将事务中的频繁项筛选出来，并按照L1中的特征项的顺序进行排序，记作P').save()
    Article(id=61, context='将P插入到T中，如果T中存在P的前缀，则每个前缀结点的计数值加1，仅为跟随在前缀之后的项创建新结点并计数为1').save()
    Article(id=62, context='更新频繁项表中的连接').save()
    Article(id=63, context='重复以上3-5步骤，直到所有结点都排列完毕').save()
    Article(id=64, context='在FP-tree构建完成后，便可用它来进行频繁项集的挖掘操作，分别以频繁项表中的项目作为后缀，构造它的条件模式基。'
                           '条件模式基是FP-tree中与该后缀一起出现的前缀路径的集合。通过条件模式基构造该项的条件FP-tree，'
                           '并递归性地在该树上进行挖掘操作。').save()
    return HttpResponse("刷新文本成功!<a href='index'>点击返回主页面</a>")
