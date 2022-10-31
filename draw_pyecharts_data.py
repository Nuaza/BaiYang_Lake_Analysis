#!/usr/bin/env python3.8
# @Time:2022/4/29
# @Author:CarryLee
# @File:draw_pyecharts_data.py
from numpy import array
from header import get_dataset, get_extra_dataset
from pyecharts.charts import Parallel, Graph, Bar, Line
import pyecharts.options as opts
from associationAnalysis_data import get_itemsets_without_frozenset, get_association_rule

path = './webView/templates/resources/'


# 仅限draw_pyecharts_data.py文件使用，外部文件引用可能会报错
def get_original_data():
    return get_dataset('./data/example.xlsx')


# 根据频繁项集绘制柱状图
def draw_bars_of_frequent_itemsets(file_path, output_path, min_support=0.05):
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
            title_opts=opts.TitleOpts(title="频繁项集柱状图", subtitle="min_support="+str(min_support))
        )
            .render(output_path + "bar_of_data_frequent_itemsets.html")
    )


# 根据关联规则绘制关系图
def draw_graph_of_data_rules(file_path, output_path, min_support=0.05):
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
                 layout="circular",
                 repulsion=4000,
                 linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
                 edge_symbol=["", "arrow"]
                 )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="关联规则关系图", subtitle="min_support="+str(min_support)),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
        )
            .render(output_path + "graph_of_data_rules.html")
    )


# 根据频繁项集绘制关系图
def draw_graph_of_data_itemsets(file_path, output_path, min_support=0.05):
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
            opts.GraphNode(name=itemsets[i], symbol_size=support[i]*50, value=support[i],
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
            title_opts=opts.TitleOpts(title="关联规则关系图", subtitle="min_support="+str(min_support)),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
        )
            .render(output_path + "graph_of_data_itemsets.html")
    )


def draw_parallel_of_data_rules(file_path, output_path, min_support):
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
        .render(output_path + "parallel_of_data_rules.html")
    )


# 根据extra数据的pH值绘制折线图
def draw_line_of_pH_from_extra(path):
    cpt_data = get_extra_dataset("data/extra", option=1)
    gdzz_data = get_extra_dataset("data/extra", option=2)
    nlz_data = get_extra_dataset("data/extra", option=3)
    qt_data = get_extra_dataset("data/extra", option=4)
    scd_data = get_extra_dataset("data/extra", option=5)
    x_data = cpt_data.iloc[:, 0].tolist()
    c = (
        Line(init_opts=opts.InitOpts(width="1000px"))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="监测数据pH值变化图", subtitle="自动数据(未审核)"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="pH",
                name_location="middle",
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
            datazoom_opts=[
                opts.DataZoomOpts(xaxis_index=0),
                opts.DataZoomOpts(type_="inside", xaxis_index=0),
            ],
        )
            .add_xaxis(x_data)
            .add_yaxis("采蒲台", cpt_data.iloc[:, 2].tolist())
            .add_yaxis("光淀张庄", gdzz_data.iloc[:, 2].tolist(), is_selected=False)
            .add_yaxis("南刘庄", nlz_data.iloc[:, 2].tolist(), is_selected=False)
            .add_yaxis("圈头", qt_data.iloc[:, 2].tolist(), is_selected=False)
            .add_yaxis("烧车淀", scd_data.iloc[:, 2].tolist(), is_selected=False)
            .render(path)
    )


# 根据extra数据的温度的值绘制折线图
def draw_line_of_temperature_from_extra(path):
    cpt_data = get_extra_dataset("data/extra", option=1)
    gdzz_data = get_extra_dataset("data/extra", option=2)
    nlz_data = get_extra_dataset("data/extra", option=3)
    qt_data = get_extra_dataset("data/extra", option=4)
    scd_data = get_extra_dataset("data/extra", option=5)
    x_data = cpt_data.iloc[:, 0].tolist()
    c = (
        Line(init_opts=opts.InitOpts(width="1000px"))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="监测数据温度变化图", subtitle="自动数据(未审核)"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="水温℃",
                name_location="middle",
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
            datazoom_opts=[
                opts.DataZoomOpts(xaxis_index=0),
                opts.DataZoomOpts(type_="inside", xaxis_index=0),
            ],
        )
            .add_xaxis(x_data)
            .add_yaxis("采蒲台", cpt_data.iloc[:, 1].tolist())
            .add_yaxis("光淀张庄", gdzz_data.iloc[:, 1].tolist(), is_selected=False)
            .add_yaxis("南刘庄", nlz_data.iloc[:, 1].tolist(), is_selected=False)
            .add_yaxis("圈头", qt_data.iloc[:, 1].tolist(), is_selected=False)
            .add_yaxis("烧车淀", scd_data.iloc[:, 1].tolist(), is_selected=False)
            .render(path)
    )


# 根据extra数据的溶解氧的值绘制折线图
def draw_line_of_O2_from_extra(path):
    cpt_data = get_extra_dataset("data/extra", option=1)
    gdzz_data = get_extra_dataset("data/extra", option=2)
    nlz_data = get_extra_dataset("data/extra", option=3)
    qt_data = get_extra_dataset("data/extra", option=4)
    scd_data = get_extra_dataset("data/extra", option=5)
    x_data = cpt_data.iloc[:, 0].tolist()
    c = (
        Line(init_opts=opts.InitOpts(width="1000px"))
            .add_xaxis(x_data)
            .add_yaxis("采蒲台", cpt_data.iloc[:, 3].tolist())
            .add_yaxis("光淀张庄", gdzz_data.iloc[:, 3].tolist(), is_selected=False)
            .add_yaxis("南刘庄", nlz_data.iloc[:, 3].tolist(), is_selected=False)
            .add_yaxis("圈头", qt_data.iloc[:, 3].tolist(), is_selected=False)
            .add_yaxis("烧车淀", scd_data.iloc[:, 3].tolist(), is_selected=False)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="监测数据溶解氧变化图", subtitle="自动数据(未审核)"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="溶解氧mg/L",
                type_="value",
                name_location="middle",
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
            datazoom_opts=[
                opts.DataZoomOpts(xaxis_index=0),
                opts.DataZoomOpts(type_="inside", xaxis_index=0),
            ],
            visualmap_opts=opts.VisualMapOpts(
                pos_top="10",
                pos_right="10",
                is_piecewise=True,
                pieces=[
                    {"gt": 7.5, "color": "#096"},
                    {"gt": 6, "lte": 7.5, "color": "#ffde33"},
                    {"gt": 5, "lte": 6, "color": "#ff9933"},
                    {"gt": 3, "lte": 5, "color": "#cc0033"},
                    {"gt": 2, "lte": 3, "color": "#660099"},
                    {"gt": 0, "lte": 2, "color": "#7e0023"},
                ],
                out_of_range={"color": "#999"},
            )
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": 2},
                    {"yAxis": 3},
                    {"yAxis": 5},
                    {"yAxis": 6},
                    {"yAxis": 7.5},
                ],
                label_opts=opts.LabelOpts(position="end"),
            )
        )

            .render(path)
    )


# 根据手工数据的高锰酸盐的值绘制折线图
def draw_line_of_MnO2(path):
    nlz_data = get_dataset('./data/example.xlsx').iloc[0:18, :]
    gdzz_data = get_dataset('./data/example.xlsx').iloc[18:36, :]
    scd_data = get_dataset('./data/example.xlsx').iloc[36:54, :]
    qt_data = get_dataset('./data/example.xlsx').iloc[54:72, :]
    cpt_data = get_dataset('./data/example.xlsx').iloc[72:90, :]
    x_data = nlz_data.iloc[:, 3].tolist()
    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("采蒲台", cpt_data.iloc[:, 7].tolist())
            .add_yaxis("光淀张庄", gdzz_data.iloc[:, 7].tolist())
            .add_yaxis("南刘庄", nlz_data.iloc[:, 7].tolist())
            .add_yaxis("圈头", qt_data.iloc[:, 7].tolist(), is_selected=False)
            .add_yaxis("烧车淀", scd_data.iloc[:, 7].tolist(), is_selected=False)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="监测数据高锰酸盐变化图", subtitle="手工数据"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="高锰酸盐指数mg/L",
                type_="value",
                name_location="middle",
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": 6},
                ],
                label_opts=opts.LabelOpts(position="end"),
                linestyle_opts=opts.LineStyleOpts(type_="dotted", color="#CC0033")
            )
        )
            .render(path)
    )


# 根据手工数据的COD的值绘制折线图
def draw_line_of_COD(path):
    nlz_data = get_dataset('./data/example.xlsx').iloc[0:18, :]
    gdzz_data = get_dataset('./data/example.xlsx').iloc[18:36, :]
    scd_data = get_dataset('./data/example.xlsx').iloc[36:54, :]
    qt_data = get_dataset('./data/example.xlsx').iloc[54:72, :]
    cpt_data = get_dataset('./data/example.xlsx').iloc[72:90, :]
    x_data = nlz_data.iloc[:, 3].tolist()
    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("采蒲台", cpt_data.iloc[:, 8].tolist())
            .add_yaxis("光淀张庄", gdzz_data.iloc[:, 8].tolist())
            .add_yaxis("南刘庄", nlz_data.iloc[:, 8].tolist())
            .add_yaxis("圈头", qt_data.iloc[:, 8].tolist(), is_selected=False)
            .add_yaxis("烧车淀", scd_data.iloc[:, 8].tolist(), is_selected=False)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="监测数据化学需氧量变化图", subtitle="手工数据"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="化学需氧量mg/L",
                type_="value",
                name_location="middle",
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": 20},
                ],
                label_opts=opts.LabelOpts(position="end"),
                linestyle_opts=opts.LineStyleOpts(type_="dotted", color="#CC0033")
            )
        )
            .render(path)
    )


# 根据手工数据的BOD₅的值绘制折线图
def draw_line_of_BOD(path):
    nlz_data = get_dataset('./data/example.xlsx').iloc[0:18, :]
    gdzz_data = get_dataset('./data/example.xlsx').iloc[18:36, :]
    scd_data = get_dataset('./data/example.xlsx').iloc[36:54, :]
    qt_data = get_dataset('./data/example.xlsx').iloc[54:72, :]
    cpt_data = get_dataset('./data/example.xlsx').iloc[72:90, :]
    x_data = nlz_data.iloc[:, 3].tolist()
    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("采蒲台", cpt_data.iloc[:, 9].tolist())
            .add_yaxis("光淀张庄", gdzz_data.iloc[:, 9].tolist())
            .add_yaxis("南刘庄", nlz_data.iloc[:, 9].tolist())
            .add_yaxis("圈头", qt_data.iloc[:, 9].tolist(), is_selected=False)
            .add_yaxis("烧车淀", scd_data.iloc[:, 9].tolist(), is_selected=False)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="监测数据生化需氧量变化图", subtitle="手工数据"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="五日生化需氧量mg/L",
                type_="value",
                name_location="middle",
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": 4},
                ],
                label_opts=opts.LabelOpts(position="end"),
                linestyle_opts=opts.LineStyleOpts(type_="dotted", color="#CC0033")
            )
        )
            .render(path)
    )


# 根据手工数据的氨氮的值绘制折线图
def draw_line_of_NH3(path):
    nlz_data = get_dataset('./data/example.xlsx').iloc[0:18, :]
    gdzz_data = get_dataset('./data/example.xlsx').iloc[18:36, :]
    scd_data = get_dataset('./data/example.xlsx').iloc[36:54, :]
    qt_data = get_dataset('./data/example.xlsx').iloc[54:72, :]
    cpt_data = get_dataset('./data/example.xlsx').iloc[72:90, :]
    x_data = nlz_data.iloc[:, 3].tolist()
    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("采蒲台", cpt_data.iloc[:, 10].tolist())
            .add_yaxis("光淀张庄", gdzz_data.iloc[:, 10].tolist())
            .add_yaxis("南刘庄", nlz_data.iloc[:, 10].tolist())
            .add_yaxis("圈头", qt_data.iloc[:, 10].tolist(), is_selected=False)
            .add_yaxis("烧车淀", scd_data.iloc[:, 10].tolist(), is_selected=False)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="监测数据氨氮含量变化图", subtitle="手工数据"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="氨氮mg/L",
                type_="value",
                name_location="middle",
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": 1.0},
                ],
                label_opts=opts.LabelOpts(position="end"),
                linestyle_opts=opts.LineStyleOpts(type_="dotted", color="#CC0033")
            )
        )
            .render(path)
    )


# 根据手工数据的总磷的值绘制折线图
def draw_line_of_P(path):
    nlz_data = get_dataset('./data/example.xlsx').iloc[0:18, :]
    gdzz_data = get_dataset('./data/example.xlsx').iloc[18:36, :]
    scd_data = get_dataset('./data/example.xlsx').iloc[36:54, :]
    qt_data = get_dataset('./data/example.xlsx').iloc[54:72, :]
    cpt_data = get_dataset('./data/example.xlsx').iloc[72:90, :]
    x_data = nlz_data.iloc[:, 3].tolist()
    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("采蒲台", cpt_data.iloc[:, 11].tolist())
            .add_yaxis("光淀张庄", gdzz_data.iloc[:, 11].tolist())
            .add_yaxis("南刘庄", nlz_data.iloc[:, 11].tolist())
            .add_yaxis("圈头", qt_data.iloc[:, 11].tolist(), is_selected=False)
            .add_yaxis("烧车淀", scd_data.iloc[:, 11].tolist(), is_selected=False)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="监测数据总磷含量变化图", subtitle="手工数据"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="总磷mg/L",
                type_="value",
                name_location="middle",
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": 0.05},
                ],
                label_opts=opts.LabelOpts(position="end"),
                linestyle_opts=opts.LineStyleOpts(type_="dotted", color="#CC0033")
            )
        )
            .render(path)
    )


# 根据手工数据的总氮的值绘制折线图
def draw_line_of_N(path):
    nlz_data = get_dataset('./data/example.xlsx').iloc[0:18, :]
    gdzz_data = get_dataset('./data/example.xlsx').iloc[18:36, :]
    scd_data = get_dataset('./data/example.xlsx').iloc[36:54, :]
    qt_data = get_dataset('./data/example.xlsx').iloc[54:72, :]
    cpt_data = get_dataset('./data/example.xlsx').iloc[72:90, :]
    x_data = nlz_data.iloc[:, 3].tolist()
    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("采蒲台", cpt_data.iloc[:, 12].tolist())
            .add_yaxis("光淀张庄", gdzz_data.iloc[:, 12].tolist())
            .add_yaxis("南刘庄", nlz_data.iloc[:, 12].tolist())
            .add_yaxis("圈头", qt_data.iloc[:, 12].tolist(), is_selected=False)
            .add_yaxis("烧车淀", scd_data.iloc[:, 12].tolist(), is_selected=False)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="监测数据总氮含量变化图", subtitle="手工数据"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="总氮mg/L",
                type_="value",
                name_location="middle",
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": 1.0},
                ],
                label_opts=opts.LabelOpts(position="end"),
                linestyle_opts=opts.LineStyleOpts(type_="dotted", color="#CC0033")
            )
        )
            .render(path)
    )
