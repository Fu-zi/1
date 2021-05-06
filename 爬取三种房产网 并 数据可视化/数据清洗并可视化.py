import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate #导入interpolate模块
from pyecharts import Bar, Pie         # 用于图形数据的添加以及展现   Bar Line Pie 分别是柱状图 折线图 饼图
from pyecharts import Line,EffectScatter, Overlap

def data():

    # 读取表格数据
    lianjia = pd.read_csv("lianjia_data.csv", encoding="gbk")
    anjuke = pd.read_csv("anjuke.csv", encoding="gbk")
    fangyoujia = pd.read_csv("fangyoujia.csv", encoding="gbk")

    # #合并数据
    frames = [lianjia, fangyoujia]
    connect_data = pd.concat(frames)
    # 保存合并后的数据子本地
    connect_data.to_csv('data_zufang.csv', index=False, encoding='utf-8-sig')

    # 根据列值筛选处city为gz（广州）的行数据
    df_gz = connect_data.loc[connect_data['city'] == 'gz']

    # 广州市不同区租金平均单价,并至少保留两位小数
    list_gz = df_gz['price'].groupby(df_gz['orientation']).mean().round(decimals=2).tolist()

    # 粤港澳大湾区各市租房平均单价,并至少保留两位小数
    list_yga = connect_data['price'].groupby(connect_data['city']).mean().round(decimals=2)
    # 广州市各地区出租户型数量

    return list_price_gz, list_price_yga, pie_num_gz, pie_num_yga

def drop():
    plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
    plt.rcParams['font.serif'] = ['KaiTi']
    plt.rcParams['axes.unicode_minus'] = False

# #广州市各区租房平均单价柱状图def drop(list_gz, e):
#     x = ['从化', '南沙', '增城', '天河', '海珠', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
#     y = list_price_gz
#     plt.bar(x, y)
#     plt.title('广州市各区租房平均单价柱状图')
#     plt.show()

# #广州市各地区总出租户型比例
#     attr = ['中小户型', '中大户型','大户型', '小户型','中户型']
#     v1 = pie_num_yga[1:]
#     pie = Pie('广州市各地区总出租户型比例环形图', title_pos='center')
#     pie.add(
#             '', attr, v1,  # ''：图例名（不使用图例）
#             radius=[40, 75],  # 环形内外圆的半径
#             is_label_show=True,  # 是否显示标签
#             label_text_color=None,  # 标签颜色
#             legend_orient='vertical',  # 图例垂直
#             legend_pos='left'
#         )
#     pie.show_config()
#     pie.render('pie_num_gz.html')

# #粤港澳大湾区各城市总出租户型比例
#     # 生成数据
#     labels = ['中小户型', '中大户型','大户型', '小户型','中户型']
#     share =  pie_num_yga[1:]
#
#     # 设置分裂属性
#     explode = [0, 0, 0, 0, 0.1]
#     # 分裂饼图
#     plt.pie(share, explode=explode,
#             labels=labels, autopct='%3.1f%%',
#             startangle=180, shadow=True,
#             colors=['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'red'])
#     # 标题
#     plt.title('粤港澳大湾区各城市总出租户型饼图')
#
#     plt.show()


# #粤港澳大湾区各城市出租房屋发布时间线性_闪烁图
#     line = Line('粤港澳大湾区各城市出租房屋发布时间线性_闪烁图')
#     x_data = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
#     y_data = [2805, 1708, 1170, 1140, 1230, 1492, 2104, 2366, 3335, 1103, 614, 477]
#     line.add('', x_data, y_data, is_random=True, xaxis_name='时间变化',
#              yaxis_name='房屋数量', yaxis_name_gap=60)
#
#     es = EffectScatter()
#     es.add('', x_data, y_data, effect_scale=8, area_color='red')  # 闪烁
#     overlop = Overlap()
#     overlop.add(line)  # 必须先添加line,在添加es
#     overlop.add(es)
#     overlop.render('yga_line.html')


#粤港澳大湾区各市租房平均单价柱状图

    # bar = Bar('粤港澳大湾区各市租房平均单价柱状图')
    # bar.add('各市租房平均单价',
    #         ['东莞', '佛山', '广州', '惠州', '江门', '深圳', '珠海', '肇庆', '中山'],
    #         list_price_yga,
    #         is_more_utils=True  # 设置最右侧工具栏
    #         ,label_color = ['#99ccff']
    #         )
    # bar.show_config()  # 调试输出pyecharts的js配置信息
    # bar.render('yga_bar.html')


#粤港澳大湾区各城市租房配套资源数量

    plt.figure(figsize=(9,6))
    X = ['广州', '深圳', '珠海', '佛山', '惠州', '东莞', '中山', '江门']
    Y1 = [340, 530, 2130, 1660, 2270, 2110, 1810, 1630]
    plt.bar(X, Y1, alpha=0.9, width=0.35, edgecolor='white', label='配套资源数量', lw=1)
    plt.legend(loc="upper left")
    plt.title('粤港澳大湾区各城市租房配套资源数量')
    plt.show()





if __name__ == '__main__':
    # data()
    drop()



