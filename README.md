# Boss直聘爬虫

## Boss直聘岗位全国薪资水平分析程序

![](https://img.shields.io/badge/Python-3.11-green.svg)

#### Boss直聘官网 - www.zhipin.com

---

## 需求

### 原始需求

设计一个**图形界面**，可以**输入一个岗位名称**，从boss直聘网抓取招聘岗位的数据（**至少包括岗位名称、工作区域、招聘单位、薪酬、工作经验年限、学历、岗位关键字**），并**保存**到MongoDB数据库或redis数据库中，能通过**图形展示该岗位在不同城市的薪酬水平**。

### 需求分析

1. 设计图形界面，使用 **tkinter** 进行图形化界面设计
2. 用户可以输入岗位名称，点击运行按钮运行爬虫程序
3. 需要获得数据（**至少包括岗位名称、工作区域、招聘单位、薪酬、工作经验年限、学历、岗位关键字**）
4. 保存数据到**MongoDB或者Redis**，在 Scarpy框架的 **pipelines** 中进行数据库操作，使用pymongo模块或者redis模块
5. 图形展示该岗位在不同城市的薪资水平，使用条形图进行展示，使用 **matplotlib** 模块中的 **figure** 函数生成条形图

## 数据结构设计

### 爬取字段数据结构

| 字段名 | 数据类型 | 字段描述 |
| ----- | ----- | ----- |
| jobkwd | String | 搜索岗位名 |
| jobName | String | 岗位名称 |
| cityName | String | 工作区域 |
| companyName | String | 招聘单位 |
| salaryDesc | String | 薪酬 |
| jobExperience | String | 工作经验年限 |
| jobDegree | String | 学历 |

### 程序数据结构

| 字段名 | 数据类型 | 字段描述 |
| ----- | ----- | ----- |
| f | Object | 条形图对象 |
| host | String | MongoDB IP |
| port | Numbers | MongoDB 端口 |
| db_name | String | 数据库名 |
| client | Object | MongoDB 连接对象 |
| collection | Object | MongoDB 集合对象 |
| data_df | Object | pandas 数据对象 |
| data_df_meigong_keyword | list | 对应搜索岗位数据列表 |
| data_df_meigong_keyword_salary | list | 对应搜索岗位工资列表 |
| process | Object | 线程对象 |
| root | Object | tkinter对象 |
| lable_value | Object | tkinter状态 |
| entry | Object | tkinter输入框 |

## 模块设计

### 爬虫模块

1. 配置Scrapy框架运行环境，配置变量
2. 岗位搜索页反爬下载中间件
3. 运行爬虫程序
4. 根据爬取岗位名称爬取岗位信息
5. 根据网站反爬机制设置对应的反反爬策略
6. 构建Item 传递pipelines
7. pipelines存入MongoDB

### 图形界面模块

1. 使用tkinter模块生成GUI界面
2. 构建tkinter输入框获得爬取岗位名，按钮点击运行爬虫程序
3. 爬虫模块运行结束后，运行条形图模块
4. 将条形图模块生成的条形图展示在GUI界面

### 条形图模块

1. 连接MongoDB数据库
2. 获取条形图所需要的数据（城市|薪酬）
3. 构建条形图需要的数据对象（x轴：城市|y轴：薪酬平均水平）
4. 将数据对象传入条形图对象
5. 绘制条形图
6. 保存绘制的条形图
