#!/usr/bin/env python3

# -*- encoding=utf-8 -*-

import requests

import pymysql.cursors


def get_position_info(pageNo,keyWords):
#   """返回当前页面的信息列表"""
    url = "https://www.lagou.com/jobs/positionAjax.json"

    headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7",
        "Connection":"keep-alive",
        "Content-Length":"63",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie":"JSESSIONID=ABAAAECABGFABFF2355DDD810AA4B7200888D1AD6748FCE; user_trace_token=20200114140751-a42b5275-8421-48d3-b9e7-68dfd54a7268; WEBTJ-ID=20200114140806-16fa2aa95b2747-088a3c550e67ef-1136685a-1764000-16fa2aa95b37cb; _ga=GA1.2.1962027842.1578982086; _gid=GA1.2.552871320.1578982086; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1578982086; LGUID=20200114140752-33060498-3694-11ea-b2bf-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_MIDDLE_TOKEN=52a24466865c3ceb89c3746da8f4044e; lagou_utm_source=A; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216fa2aa96bf214-0b00a41712c003-1136685a-1764000-16fa2aa96c0e6c%22%2C%22%24device_id%22%3A%2216fa2aa96bf214-0b00a41712c003-1136685a-1764000-16fa2aa96c0e6c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; X_HTTP_TOKEN=c2100305a94fa1bd24375097511424ef3d7cabe162; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1579057355; LGSID=20200115110222-735d7e62-3743-11ea-b2de-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Futrack%2FtrackMid.html%3Ff%3Dhttps%253A%252F%252Fwww.lagou.com%252Fjobs%252Flist%255Fpython%253FlabelWords%253D%2526fromSearch%253Dtrue%2526suginput%253D%26t%3D1579057335%26_ti%3D1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20200115110222-735d8073-3743-11ea-b2de-525400f775ce; SEARCH_ID=72019fd8d0824c75bf82cd2e145a7d13",
        "Host":"www.lagou.com",
        "Origin":"https://www.lagou.com",
        "Referer":"https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Mobile Safari/537.36",
        "X-Anit-Forge-Code":"0",
        "X-Anit-Forge-Token":"None",
        "X-Requested-With":"XMLHttpRequest"
    }
    postData = {"needAddtionalResult":"false","pn":pageNo,"kd":keyWords,"sid":"098c18fdd37945f7a5781f7d465e0bd8"}
    
    response = requests.post(url, data=postData, headers=headers)
    return response.json()




def get_positions_list(positions_dic):
    list_positions =  positions_dic['content']['positionResult']['result']

    result = []
    for position in list_positions:
      info = []
      info.append(position["positionName"])
      info.append(position["companyFullName"])
      info.append(position["companySize"])
      info.append(position["financeStage"])
      info.append(position["industryField"])
      info.append(position["city"])
      info.append(position["salary"])
      info.append(position["workYear"])
      result.append(info)

    return result
    


def get_conn():
   '''建立数据库连接'''
   conn = pymysql.connect(host='localhost',
                               user='root',
                               password='jj1234567',
                               db='pythondb',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
   return conn


def insert(conn, info):
    '''数据写入数据库'''
#    print(info)
    with conn.cursor() as cursor:
        sql = "INSERT INTO `position_info_detail` (`positionName`, `companyFullName`, `companySize`, `financeStage`, `industryField`, `city`, `salary`, `workYear`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, info)
    conn.commit()



def main():
    try:
        conn = get_conn()  # 建立数据库连接  不存数据库 注释此行
        for i in [2,3,4,5,6,7,8,9,10,11]:
            positions_dic = get_position_info(i,"python")
            print(positions_dic)
            array = get_positions_list(positions_dic)
            for position in array:
                insert(conn, tuple(position))

        conn.close()  # 关闭数据库连接，不存数据库 注释此行
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
