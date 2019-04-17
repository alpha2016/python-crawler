# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests
import csv
import bs4
import pymysql
import math

def get_data(majorname):
    print(majorname)
    url = 'http://www.zjchina.org/mspMajorIndexAction.fo'
    d = {'year': 2019, 'province':'', 'schoolno':'', 'schoolname': '','majorno':'', 'majorname': majorname,'startcount': 0,'gopage':'', 'totalPages': 1,'page_size': 100}
    r = requests.post(url, data=d)
    soup = BeautifulSoup(r.content, 'html.parser')
    body = soup.body
    create(majorname, body)


    # 查询是不是多个页面
    page = body.find('div', {'id': 'page'})
    # print(page)
    pageNum = page.find_all('font')
    num = pageNum[0].text
    maxPage = math.ceil(float(num) / 100)
    print(maxPage)

    # 多个页面的情况下，循环处理新的页面
    if maxPage > 1:
        for p in range(2, maxPage + 1, 1):
            d = {'year': 2019, 'province':'', 'schoolno':'', 'schoolname': '','majorno':'', 'majorname': majorname,'startcount': 0,'gopage':'', 'totalPages': maxPage,'page_size': 100}
            # print(d)
            url = 'http://www.zjchina.org/mspMajorIndexAction.fo?&startcount=' + str((p - 1) * 100)
            r = requests.post(url, data=d)
            soup = BeautifulSoup(r.content, 'html.parser')
            body = soup.body
            create(majorname, body)

    
def create(keyword, body):
    div = body.find('div', {'id': 'A5'})
    data = div.find('table')
    trs = data.find_all('tr')
    tr = trs[1:len(trs)]

    for x in tr:
        td = x.find_all('td')
        province = td[0].text
        code = td[1].text
        name = td[2].text
        school_code = td[3].text
        school_name = td[4].text
        years_limit = td[5].text
        remark = td[6].text

        sql = """insert into majors(keyword,province,code,name,school_code,school_name,years_limit,remark) values ('{}','{}','{}','{}','{}','{}','{}','{}'); """.format(
            keyword,province, code, name, school_code, school_name, years_limit, remark)
        try:
            cur.execute(sql)
            connect.commit()
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    connect = pymysql.connect(
            host = "127.0.0.1",
            user = "root",
            password = "123456",
            db = "business",
            port = 3306,
            charset = "utf8"
        )
    cur = connect.cursor()
    # 爬取的专业信息数组
    majors = ['人物形象设计']
    for major in majors:
        get_data(major)
connect.close()

# 对应表结构
# CREATE TABLE `majors` (`id` int(11) NOT NULL AUTO_INCREMENT,
#     `keyword` varchar(50) DEFAULT NULL COMMENT '关键字',
#     `province` varchar(50) DEFAULT NULL COMMENT '省份信息',
#     `code` varchar(50) DEFAULT NULL COMMENT '专业代码',
#     `name` varchar(50) DEFAULT NULL COMMENT '专业名称',
#     `school_code` varchar(50) DEFAULT NULL COMMENT '学校代码',
#     `school_name` varchar(255) DEFAULT NULL COMMENT '学校名称',
#     `years_limit` tinyint(3) unsigned DEFAULT NULL COMMENT '年限',
#     `remark` varchar(255) DEFAULT NULL COMMENT '备注',
#     `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     PRIMARY KEY(`id`) USING BTREE
# ) ENGINE = InnoDB AUTO_INCREMENT = 237 DEFAULT CHARSET = utf8mb4 ROW_FORMAT = DYNAMIC
