#!/usr/bin/env python3.8
# @Time:2022/4/29
# @Author:CarryLee
# @File:draw_pyecharts_standard.py
from numpy import array
from header import get_dataset
from pyecharts.charts import Graph, Pie, Bar, Bar3D, Parallel
import pyecharts.options as opts
from associationAnalysis_standard import get_itemsets_without_frozenset, get_association_rule

path = './webView/templates/resources/'


def get_original_data():
    return get_dataset('./data/手工合并.xlsx')


# 根据频繁项集绘制柱状图
def draw_bars_of_frequent_itemsets(file_path, output_path, min_support=0.02):
    data = get_itemsets_without_frozenset(file_path, min_support, 'support')
    c = (
        Bar(init_opts=opts.InitOpts(width="1200px", height="600px"))
            .add_xaxis(
            data.iloc[:, 1].tolist()
        )
            .add_yaxis("频繁项集", [round(i, 2) for i in data.iloc[:, 0].tolist()])
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=13, rotate=30), name='频繁项集'),
            yaxis_opts=opts.AxisOpts(name='支持度', name_location="center"),
            title_opts=opts.TitleOpts(title="频繁项集柱状图", subtitle="min_support=" + str(min_support))
        )
            .render(output_path + "bar_of_standard_frequent_itemsets.html")
    )


# 根据白洋淀水质类别占比绘制饼图
def draw_pie_of_standard(file_path, output_path):
    data = get_dataset(file_path).iloc[:, 32].tolist()
    c = (
        Pie()
        .add(
            series_name="水质类别",
            data_pair=[('Ⅲ类', data.count('Ⅲ类')),
                       ('Ⅳ类', data.count('Ⅳ类')),
                       ('Ⅴ类', data.count('Ⅴ类')),
                       ('劣Ⅴ类', data.count('劣Ⅴ类'))],
            radius=200
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="白洋淀监测数据水质类别饼图",
                pos_left="left",
                pos_top="20",
            ),
            legend_opts=opts.LegendOpts(is_show=True),
        )
        .render(output_path + "pie_of_standard.html")
    )


def draw_parallel_of_standard_rules(file_path, output_path, min_support):
    data = get_association_rule(file_path, min_support)
    rules = []
    number = 10
    if data.shape[0] < 10:
        number = data.shape[0]
    for i in range(number):
        temp = [data.loc[i][0] + " → " + data.loc[i][1], round(data.loc[i][4], 2), round(data.loc[i][5], 2),
                round(data.loc[i][6], 2), round(data.loc[i][7], 2)]
        rules.append(temp)
    c = (
        Parallel()
        .add_schema(
            [
                opts.ParallelAxisOpts(dim=0, name="关联规则", type_="category", data=array(rules)[:, 0].tolist()),
                opts.ParallelAxisOpts(dim=1, name="支持度", is_scale=True),
                opts.ParallelAxisOpts(dim=2, name="置信度", is_scale=True),
                opts.ParallelAxisOpts(dim=3, name="提升度", is_scale=True),
                opts.ParallelAxisOpts(dim=4, name="杠杆率", is_scale=True),
            ]
        )
        .add("关联规则", rules)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="关联规则平行图", subtitle="前"+str(number)+"项，min_support="+str(min_support)),
        )
        .render(output_path + "parallel_of_standard_rules.html")
    )


def draw_bar3D_of_standard_rules(file_path, output_path, min_support=0.02):
    rules = get_association_rule(file_path, min_support)
    y_axis = ['支持度', '置信度', '提升度', '杠杆率']
    x_axis, datas = [], []
    for i in range(rules.shape[0]):
        x_axis.append(rules.loc[i][0]+" → " + rules.loc[i][1])
    for i in range(4, rules.shape[1] - 1):
        for j in range(rules.shape[0]):
            temp_list = [i - 4, j, round(rules.loc[j][i], 2)]
            datas.append(temp_list)
    data = [[d[1], d[0], d[2]] for d in datas]
    c = (
        Bar3D(init_opts=opts.InitOpts(width="1200px", height="600px"))
        .add(
            series_name="",
            data=data,
            xaxis3d_opts=opts.Axis3DOpts(name="关联规则", type_="category", data=x_axis),
            yaxis3d_opts=opts.Axis3DOpts(name="规则项目", type_="category", data=y_axis),
            zaxis3d_opts=opts.Axis3DOpts(type_="value", min_=0, max_=3),
            grid3d_opts=opts.Grid3DOpts(
                width=100, depth=100, rotate_speed=20, is_rotate=True
            ),
            shading="realistic"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="关联规则3D柱状图", subtitle="min_support="+str(min_support)),
            visualmap_opts=opts.VisualMapOpts(
                max_=20,
                range_color=[
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ],
            )
        )
        .render(output_path + "bar3D_of_standard.html")
    )


# 根据关联规则绘制关系图
def draw_graph_of_standard_rules(file_path, output_path, min_support=0.02):
    data = get_association_rule(file_path, min_support)
    antecedents, consequents, temp, nodes, nodes_data, links_data = [], [], [], [], [], []
    categories = [
        opts.GraphCategory(name="频繁1-项集"), opts.GraphCategory(name="频繁2-项集"), opts.GraphCategory(name="频繁3-项集"),
        opts.GraphCategory(name="频繁4-项集")
    ]
    for i in range(data.shape[0]):
        antecedents.append(data.loc[i][0])
        consequents.append(data.loc[i][1])
    temp = antecedents + consequents
    for i in range(len(temp)):
        if temp[i] not in nodes:
            nodes.append(temp[i])

    for i in range(len(nodes)):
        nodes_data.append(opts.GraphNode(name=nodes[i], symbol_size=(nodes[i].count(",")+1)*15, category=nodes[i].count(",")))
    for i in range(len(antecedents)):
        links_data.append(opts.GraphLink(source=antecedents[i], target=consequents[i], value=i+1))
    c = (
        Graph(init_opts=opts.InitOpts(height="600px"))
            .add("",
                 nodes_data,
                 links_data,
                 categories,
                 repulsion=4000,
                 linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
                 edge_symbol=["", "arrow"]
                 )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="关联规则关系图", subtitle="min_support="+str(min_support)),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
        )
            .render(output_path + "graph_of_standard_rules.html")
    )


# 根据频繁项集绘制关系图
def draw_graph_of_standard_itemsets(file_path, output_path, min_support=0.02):
    data = get_itemsets_without_frozenset(file_path, min_support, 'support')
    pre, after, nodes_data, links_data = [], [], [], []
    categories = [
        opts.GraphCategory(name="频繁1-项集"), opts.GraphCategory(name="频繁2-项集"), opts.GraphCategory(name="频繁3-项集"),
        opts.GraphCategory(name="频繁4-项集")
    ]
    itemsets = data.iloc[:, 1].tolist()
    support = [round(i, 2) for i in data.iloc[:, 0]]
    for i in range(data.shape[0]):
        for j in range(i+1, data.shape[0]):
            if len(itemsets[j].split(',')) > 1:
                if set(itemsets[i]) < set(itemsets[j]):
                    pre.append(itemsets[i])
                    after.append(itemsets[j])
    for i in range(len(itemsets)):
        nodes_data.append(
            opts.GraphNode(name=itemsets[i], symbol_size=support[i]*200, value=support[i],
                           category=itemsets[i].count(",")))
    for i in range(len(pre)):
        links_data.append(opts.GraphLink(source=pre[i], target=after[i], value=i + 1))
    c = (
        Graph(init_opts=opts.InitOpts(width="1000px", height="600px"))
            .add("",
                 nodes_data,
                 links_data,
                 categories,
                 layout="circular",
                 repulsion=4000,
                 linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
                 edge_symbol=["", "arrow"]
                 )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="频繁项集关系图", subtitle="min_support="+str(min_support)),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
        )
            .render(output_path + "graph_of_standard_itemsets.html")
    )
