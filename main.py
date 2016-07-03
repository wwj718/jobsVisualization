from os.path import dirname, join
import numpy as np
import pandas as pd

from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBoxForm
from bokeh.models.widgets import Slider, Select, TextInput  #,DatePicker # http://bokeh.pydata.org/en/0.11.1/docs/reference/models/widgets.inputs.html
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, OpenURL, TapTool  # open url
import codecs

'''
编码问题：保证所有进入python程序的数据被解码为unicode，关于编码问题可以看我的这篇文章：http://blog.just4fun.site/decode-and-encode-note.html

关于注释: 由于bokeh采用了ast来处理代码，所以中文注释会有问题，尽量采用文档字符串的注释风格而不是#

可以采用jupyter来探索jobs_df
'''

jobs_df = pd.read_csv(
    join(
        dirname(__file__),
        #"lagouSpider-20160625-141631.csv"),parse_dates=["createTime"])
        "lagouSpider-newest.csv"),# 5000 rows × 11 columns
    encoding="utf8")


'''
点的颜色，根据可视化理论的建议，你可以使用颜色反映一种属性，诸如将工资设为高亮，主语把颜色关联到哪种属性由你决定
'''
jobs_df["color"] = np.where(jobs_df["salaryMin"] > 5, "orange", "grey")
jobs_df["alpha"] = np.where(jobs_df["salaryMax"] > 10, 0.9, 0.25)
jobs_df.fillna(0, inplace=True)  # just replace missing values with zero
'''
DateRangeSlider
'''
axis_map = {
    u"该职位平均薪资": "salaryAvg",
    u"该职位最高薪资": "salaryMax",
    u"该职位最低薪资": "salaryMin",
    u"简历提交次数": "deliverCount",
    u"被查看次数": "showCount",
    #"createTime":"createTime",
}
# axis_map ,columns is value,such as Meter numericRating

# Create Input controls
#min_year = Slider(title=u"开始年份",
#                  start=1940,
#                  end=2014,
#                  value=1970,
#                  step=1)
#max_year = Slider(title=u"结束年份",
#                  start=1940,
#                  end=2014,
#                  value=2014,
#                  step=1)
#oscars = Slider(title=u"至少获得奥斯卡奖项", start=0, end=4, value=0, step=1)
#boxoffice = Slider(title=u"票房 (millions)", start=0, end=800, value=0, step=1)
'''
options 能否来自pandas的分析
positionName
# complaints['Complaint Type'].value_counts(),get  value type
# df.name.unique() : List Unique Values In A Pandas Column
# 采用jupyter探索
'''
salaryAvg = Slider(title=u"该职位平均薪资", value=0, start=0, end=50, step=5)
salaryMax = Slider(title=u"该职位最高薪资", value=0, start=0, end=50, step=5)
salaryMin = Slider(title=u"该职位最低薪资", value=0, start=0, end=50, step=5)

#createTime = DatePicker(title="create date", min_date=datetime(2015,01,01),
#                       max_date=datetime.now(),
#                       value=datetime.now()
#                       )
# jobs_df["positionType"].unique() dump to options
with codecs.open(join(dirname(__file__), "positionType.csv"), 'r') as f:
    positionType_csv = f.read().splitlines()
with codecs.open(join(dirname(__file__), "city.csv"), 'r') as f:
    city_csv = f.read().splitlines()
with codecs.open(join(dirname(__file__), "workYear.csv"), 'r') as f:
    workYear_csv = f.read().splitlines()
positionType = Select(title=u"职位类型", value=u"All", options=positionType_csv)

city = Select(title=u"城市", value=u"All", options=city_csv)
companyLabelList = TextInput(title=u"公司福利搜索(诸如五险一金，股票期权，带薪年假)")
positionAdvantage = TextInput(title=u"职位优势搜索（诸如双休，期权，季度调薪）")
companyName = TextInput(title=u"公司名称搜索")
workYear = Select(title=u"工作经验", value=u"All", options=workYear_csv)
x_axis = Select(title=u"X 轴",
                options=sorted(axis_map.keys()),
                value=u"该职位平均薪资")  # use create_time
y_axis = Select(title=u"Y 轴",
                options=sorted(axis_map.keys()),
                value=u"该职位最高薪资")

# Create Column Data Source that will be used by the plot
'''
ColumnDataSource
'''
source = ColumnDataSource(data=dict(x=[],
                                    y=[],
                                    salaryAvg=[],
                                    salaryMax=[],
                                    salaryMin=[],
                                    positionType=[],
                                    companyLabelList=[],
                                    positionAdvantage=[],
                                    companyName=[],
                                    color=[],
                                    city=[],
                                    companyLogo=[],
                                    positionId=[],
                                    workYear=[],
                                    createTime=[],
                                    alpha=[]))
'''
点的悬停提示框,logo http://www.lagou.com/+logourl 应该在显示时候改变字段，而不是存储时

todo:信息过于丰富，重叠度高，需要在旁边列出来，用表格，或者换轴（时间）

todo:出于效率考虑应该只显示2000条
'''

hover = HoverTool(tooltips=[
    (u"公司logo",
     "<img width='60' src='http://www.lagou.com/@companyLogo'></img>"), (
         u"公司名称", "@companyName"), (u"所在城市", "@city"), (
             u"工资上限", "@salaryMax k"), (u"职位类型", "@positionType"), (
                 u"职位优势", "@positionAdvantage"), (u"发布时间", "@createTime")
])

"""
tooltips=
        <div>
            <div>
                <img
                    src="http://www.lagou.com/@companyLogo"  alt="@companyLogo" width="60"
                    style="float: left;"
                    border="2"
                ></img>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">公司名称：</span>
                <span style="font-size: 15px; color: #966;">@companyName</span>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">所在城市：</span>
                <span style="font-size: 15px; color: #966;">@city</span>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">工资上限：</span>
                <span style="font-size: 15px; color: #966;">@salaryMax</span>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">职位类型：</span>
                <span style="font-size: 15px; color: #966;">@positionType</span>
            </div>
        </div>


"""
# from source.data

p = Figure(plot_height=600,
           plot_width=800,
           title="",
           #toolbar_location=None,
           tools=[hover,"tap","pan,wheel_zoom,box_zoom,reset,resize,save"],
           toolbar_location="below",  #http://bokeh.pydata.org/en/latest/docs/user_guide/tools.html
           )
p.circle(x="x",
         y="y",
         source=source,
         size=7,
         color="color",
         line_color=None,
         fill_alpha="alpha")

url = "http://www.lagou.com/jobs/@positionId.html"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

# TapSelectTool  click link
# what is  fill_alpha,why  is it string? try in jupyter
# open url http://bokeh.pydata.org/en/0.11.1/docs/user_guide/interaction.html#customjs-for-widgets


def select_movies():
    '''
    这是核心所在，使用用户的输入来筛选匹配的电影
    这里是起步的地方，最先应当构建这部分
    '''
    salaryAvg_val = salaryAvg.value
    city_val = city.value
    positionType_val = positionType.value
    workYear_val = workYear.value
    companyLabelList_val = companyLabelList.value.strip()
    positionAdvantage_val = positionAdvantage.value.strip()
    assert isinstance(city_val, unicode)
    selected = jobs_df
    selected = jobs_df[
        (jobs_df.salaryAvg >= salaryAvg.value) & (jobs_df.salaryMax >= (
            salaryMax.value)) & (jobs_df.salaryMin >= salaryMin.value)]
    if (city_val != u"All"):
        #print type(city_val) #str   | print type(u"北京") <type 'unicode'> | print type("北京") <type 'str'>
        #selected = selected[selected.city.str.contains("北京") == True] # ok
        # encode/decode
        selected = selected[selected.city.str.contains(city_val) == True]
    if (positionType_val != "All"):
        selected = selected[selected.positionType.str.contains(
            positionType_val) == True]
    if (workYear_val != "All"):
        selected = selected[selected.workYear.str.contains(workYear_val) ==
                            True]
    '''
    companyLabelList_val such as
    节日礼物,绩效奖金,五险一金,弹性工作
    股票期权,带薪年假,专项奖金,岗位晋升
    技能培训,专项奖金,带薪年假,创意团队
    节日礼物,年底双薪,带薪年假,绩效奖金
    '''
    if (companyLabelList_val != "All"):
        selected = selected[selected.companyLabelList.str.contains(
            companyLabelList_val) == True]
    if (positionAdvantage_val != "All"):
        selected = selected[selected.positionAdvantage.str.contains(
            positionAdvantage_val) == True]
    # make selected < 2000
    return selected


def update(attrname, old, new):
    df = select_movies()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title = u"%d 个职位 符合要求" % len(df)
    # use to update plot, not all data
    source.data = dict(x=df[x_name],
                       y=df[y_name],
                       salaryAvg=df["salaryAvg"],
                       salaryMax=df["salaryMax"],
                       salaryMin=df["salaryMin"],
                       positionType=df["positionType"],
                       companyLabelList=df["companyLabelList"],
                       positionAdvantage=df["positionAdvantage"],
                       companyName=df["companyName"],
                       alpha=df["alpha"],
                       city=df["city"],
                       companyLogo=df["companyLogo"],
                       positionId=df["positionId"],
                       workYear=df["workYear"],
                       createTime=df["createTime"],
                       color=df["color"], )


'''
这是所有的ui控件，这样一来pandas就可以可视化了，与用户交互
control.on_change 事件驱动
'''

controls = [salaryAvg, positionType, city, workYear, companyLabelList,
            positionAdvantage, companyName, x_axis, y_axis]
for control in controls:
    control.on_change('value', update)

inputs = HBox(VBoxForm(*controls), width=300)

update(None, None, None)  # initial load of the data
'''
curdoc -> http://bokeh.pydata.org/en/0.11.0/docs/reference/io.html
http://bokeh.pydata.org/en/0.11.0/docs/reference/io.html
HBox可能影响布局，Lay out child widgets in a single horizontal row.
 ->http://bokeh.pydata.org/en/0.10.0/docs/reference/models/widgets.layouts.html
 -> http://bokeh.pydata.org/en/0.11.1/docs/user_guide/layout.html : Laying Out Multiple Plots
p部分，应该关注p,p = Figure ->http://bokeh.pydata.org/en/0.11.0/docs/reference/plotting.html

参考server app
http://bokeh.pydata.org/en/latest/docs/gallery.html#gallery
    *  https://github.com/bokeh/bokeh/blob/0.11.1/examples/app/selection_histogram.py 只有一个文件
    *  https://github.com/bokeh/bokeh-demos/blob/master/weather/main.py  一个建议的后端模型

部署
http://bokeh.pydata.org/en/latest/docs/user_guide/server.html
demo：https://github.com/bokeh/demo.bokehplots.com/tree/master/bokeh
'''
curdoc().add_root(HBox(inputs, p, width=1100))
