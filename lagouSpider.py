#!/usr/bin/env python3

# -*-encoding:utf-8-*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import re
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from openpyxl import Workbook

import pymysql.cursors


def get_conn():
    """建立数据库连接"""
    conn = pymysql.connect(host='localhost',
                            user='root',
                            password='jj1234567',
                            db='pythondb',
                            charset='utf8',
                            cursorclass=pymysql.cursors.DictCursor)
    return conn;

def insert(conn,info):
    print(info)
    with conn.cursor() as cursor:
        sql = "INSERT INTO `position_info` (`company_name`,`salary`,`position_name`) VALUES (%s, %s, %s)"
        cursor.execute(sql,info)
    conn.commit()


def get_page_content():
    driver = webdriver.Chrome()
    driver.get("https://www.lagou.com/")
    htmls = []

    try:
        chooseLocationBox = driver.find_element_by_id("cboxWrapper")

        cboxCloseBtn = driver.find_element_by_id("cboxClose")
        cboxCloseBtn.click()
        time.sleep(2)
        input = driver.find_element_by_id("search_input")
        input.clear()
        input.send_keys("python")
        searchBtn = driver.find_element_by_id("search_button")
        searchBtn.click()
        time.sleep(2)

        closeADBtn = driver.find_element_by_class_name("body-btn")
        closeADBtn.click()
        
        htmls.append(driver.page_source)
        try:
#            nextPageBtn = driver.find_element_by_class_name("pager_next")
            i = 1
            while i<31:
                nextPageBtn = driver.find_element_by_class_name("pager_next")
                ActionChains(driver).move_to_element(nextPageBtn).perform()
                nextPageBtn.click()
                time.sleep(2)
                htmls.append(driver.page_source)
                i +=1


        except Exception as e:
            print(e)
            print("当前已经是最后一页了，下一页按钮不可点击")

#        print("html Content:",driver.page_source)
        
        return htmls
        
        
    except Exception as e:
        print("----------error-----------")
        print(e)
        print("--------error end---------")
        return htmls

    driver.close()
    
def get_position_info(htmlContents):
    res = []
    for html in htmlContents:
        soup = BeautifulSoup(html, 'html.parser')
        positions = soup.find_all("li",class_=("con_list_item default_list"))
        for position in positions:
            posi = []
            posi.append(position.get("data-company"))
            posi.append(position.get("data-salary"))
            posi.append(position.get("data-positionname"))
            res.append(posi)
            
    return res



def main():

    info = get_position_info(get_page_content())
    lang_name = 'python'
    wb = Workbook()  # 打开 excel 工作簿

    ws1 = wb.active
    ws1.title = lang_name
    
    conn = get_conn()
    
    
    for row in info:
        ws1.append(row)
        insert(conn,tuple(row))
    conn.close()
    wb.save('{}职位信息.xlsx'.format(lang_name))

if __name__ == '__main__':
   main()
