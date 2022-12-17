import multiprocessing
import time
from tkinter import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pymongo
import pandas as pd
import numpy as np
import threading
import psutil

# 定义图标样式大小参数
f = Figure(figsize=(15, 8), dpi=100)

# 绘制条形图
def draw(kwd):
    # 连接MongoDB
    host = 'localhost'
    port = 27017
    db_name = 'boss'
    client = pymongo.MongoClient(host=host, port=port)
    db = client[db_name]
    collection = db['job']

    # 构建数据对象
    data_df = pd.DataFrame(list(collection.find()))
    data_df_meigong_keyword = data_df.loc[data_df['jobkwd'].str.contains(kwd)]
    data_df_meigong_keyword_salary = data_df_meigong_keyword['salaryDesc'].str.split('-', expand=True)[0]
    print(data_df_meigong_keyword_salary)

    # Dataframe新增一列  在第 列新增一列名为' ' 的一列 数据
    data_df_meigong_keyword.insert(8, '区间最小薪资(K)', data_df_meigong_keyword_salary)
    list_group_city1 = []
    list_group_city2 = []

    # 构建数据对象
    for df1, df2 in data_df_meigong_keyword.groupby(data_df_meigong_keyword['cityName']):
        list_group_city1.append(df1)
        salary_list_district = [int(i) for i in (df2['区间最小薪资(K)'].values.tolist())]
        district_salary_mean = round(np.mean(salary_list_district), 2)
        list_group_city2.append(district_salary_mean)
        list_group_city2, list_group_city1 = (list(t) for t in zip(*sorted(zip(list_group_city2, list_group_city1), reverse=True)))

    # 添加子图:1行1列第1个
    a = f.add_subplot(111)  

    # 生成用于绘sin图的数据
    x = list_group_city1[0:15]
    y = list_group_city2[0:15]
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 在前面得到的子图上绘图
    a.bar(x, y)
    a.set_title(f"{kwd}各个省份的平均工资")
    a.set_xlabel('省份')
    a.set_ylabel(f'{kwd}平均工资(K)')
    # 将绘制的图形显示到tkinter: 创建属于root的canvas画布,并将图f置于画布上
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()  # 注意show方法已经过时了,这里改用draw
    canvas.get_tk_widget().place(x=50, y=100)

# 运行爬虫函数
def start_crawl(kwd):
    # 获取爬虫设置
    process = CrawlerProcess(get_project_settings())
    # 指定爬虫程序
    process.crawl("jobspider", kwd)
    # 运行爬虫
    process.start()

# 运行搜索函数
def search():
    try:
        # 如果条形图存在，清空条形图
        if f:
            f.clf()
        # 修改运行状态
        lable_value.set("正在抓取数据中，请稍等.....")
        # 获得输入框数据
        kwd = entry.get()
        print(f'关键词{kwd}')
        # 线程
        the_scrapy = multiprocessing.Process(target=start_crawl, args=(kwd,))
        the_scrapy.start()
        print(the_scrapy.pid)
        while the_scrapy.pid in psutil.pids():
            time.sleep(0.5)

        # 改变运行状态
        lable_value.set("数据抓取成功，正在分析数据...")
        time.sleep(3)
        draw(kwd)

    except Exception as e:
        print("错误信息---" + str(e))
        lable_value.set("数据抓取失败....")

# 将函数打包进线程
def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护
    t.daemon = True
    # 启动
    t.start()

# 初始化GUI界面函数
def init_GUI():
    # 实例化GUI界面
    global root
    root = Tk()
    root.geometry("1500x1000")
    root.title("boss抓取")

    label = Label(root, text="岗位:", font=("宋体", 18), pady=20)
    label.place(x=50, y=15)

    # 岗位输入框
    global pos_var, entry
    pos_var = StringVar()
    entry = Entry(root, font=("宋体", 18), textvariable=pos_var)
    entry.place(x=120, y=35)
    
    # 查询按钮
    # lambda :thread_it(search, ) 打包线程，避免卡死
    button = Button(root, text="搜索", font=("宋体", 16), fg="blue", command=lambda: thread_it(search))
    button.place(x=380, y=30)

    # 运行状态
    global lable_value
    lable_value = StringVar()
    label = Label(root, textvariable=lable_value, font=("宋体", 18), pady=20)
    lable_value.set("")
    label.place(x=600, y=500)

    # 窗口常显
    root.mainloop()

# 主函数
if __name__ == "__main__":
    # 初始化GUI界面
    init_GUI()
