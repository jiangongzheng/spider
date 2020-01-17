#!/usr/bin/env python3

# -*- encoding:utf-8 -*-


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
import time

from bs4 import BeautifulSoup

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
        sql = "INSERT INTO `movie_info_detail` (`movie_name`,`movie_author`,`movie_img`,`star`,`quote`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql,info)
    conn.commit()




def get_page_content():
    driver = webdriver.Chrome()
    driver.get("https://movie.douban.com/top250")
    htmls = []
    htmls.append(driver.page_source)

    try:
        for i in range(2,11):
            nextPageBtn = driver.find_element_by_link_text(str(i))
            ActionChains(driver).move_to_element(nextPageBtn).perform()
            nextPageBtn.click()
            time.sleep(2)
            htmls.append(driver.page_source)
            i +=1
    except Exception as e:
        print(e)
        print("当前已经是最后一页了，下一页按钮不可点击")

    driver.close()
    return htmls;
    
#for html in htmls:
#    print(html)

def get_movie_infos(htmls):
    res = []
    for html in htmls:
        soup = BeautifulSoup(html,'html.parser')
        movie_infos = soup.find_all("div",class_=("item"))
        for movie in movie_infos:
            movie_info = []
            movie_img = movie.div.a.img.get("src")
            names = movie.find('div',class_=('hd'))
            movie_name = ''.join(names.stripped_strings)
            authorsEle = movie.find('div',class_=('bd'))
            movie_author = authorsEle.p.get_text()
            print(movie_author.strip())
            quote = authorsEle.find('p',class_=('quote')).get_text()
            star = authorsEle.find('span',class_=('rating_num')).get_text()
            
            movie_info.append(movie_name)
            movie_info.append(movie_author)
            movie_info.append(movie_img)
            movie_info.append(star)
            movie_info.append(quote)
            
            res.append(movie_info)
            
    return res




def main():
    try:
        htmls = get_page_content()
        infos = get_movie_infos(htmls)
        conn = get_conn()
        for movie in infos:
            print(movie)
            insert(conn,tuple(movie))
        conn.close()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()

#['\n', <div class="pic">
#<em class="">250</em>
#<a href="https://movie.douban.com/subject/2300586/">
#<img alt="这个男人来自地球" class="" src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p513303986.webp" width="100"/>
#</a>
#</div>, '\n', <div class="info">
#<div class="hd">
#<a class="" href="https://movie.douban.com/subject/2300586/">
#<span class="title">这个男人来自地球</span>
#<span class="title"> / The Man from Earth</span>
#<span class="other"> / 地球不死人(港)  /  这个人来自洞穴</span>
#</a>
#<span class="playable">[可播放]</span>
#</div>
#<div class="bd">
#<p class="">
#                            导演: 理查德·沙因克曼 Richard Schenkman   主演: 大卫·李·史密斯 David ...<br/>
#                            2007 / 美国 / 剧情 科幻
#                        </p>
#<div class="star">
#<span class="rating45-t"></span>
#<span class="rating_num" property="v:average">8.5</span>
#<span content="10.0" property="v:best"></span>
#<span>263701人评价</span>
#</div>
#<p class="quote">
#<span class="inq">科幻真正的魅力不是视觉效果能取代的。 </span>
#</p>
#</div>
#</div>, '\n']

#
#detail:     a.href











