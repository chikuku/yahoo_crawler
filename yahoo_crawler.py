# -*- coding: utf-8 -*-
"""
Created on Sun May 24 18:39:00 2020

@author: Annie
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from itertools import product
os.chdir(r'D:\Users\edony\Desktop\樂天派\e-commerce\015_Alicia\015_Alicia')
# 填入要使用的瀏覽器安裝位置
options = Options()
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
webdriver_path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path = webdriver_path)

# yahoo_熟食前13頁的網址

url_1 = []
for i in range(12):
    url_1.append("https://tw.buy.yahoo.com/category/4436638?guce_referrer=aHR0cHM6Ly90dy5idXkueWFob28uY29tLw&guce_referrer_sig=AQAAAFu2UMMzegc5Jd4l4gqjEmdPGQd_GPseKw0cDgfh9xitlyAbMmePzfiFK0J-UUjjRbV-SBKhB5Im9q0S9D78qUKwmI_Et05S56JsSutE-SH_o_gDiTwDLFiZNeNOKXBpdpIWXQkuFfQxooX0T0IONBliqyNgk1uSOBP5uDzrwKXq&" +"pg="+str(i)+"&sort=p13n")


# YAHOO 要點進去抓規格   
# 主要爬蟲

def get_yahoo_name(url):
    _DELAY = 1
    food = []
    # 畫面捲7次1080剛好可以捲到底
    for num in range(1,7):
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0,"+ str(1080*num) +")")
        time.sleep(_DELAY) # 避免捲動太快 有時候還沒載入
    #先暫存一個商品網址list 接著一個一個跳轉,爬規格跟名字 然後回上一頁
    try:
        a_tag = driver.find_elements_by_tag_name('a')
        tag_li = []
        # 存每頁中每個商品的連結
        for item in a_tag:
            if 'BaseGridItem__content___3LORP BaseGridItem__hover___3UlCS' == \
            item.get_attribute('class'):
                tag_li.append(item.get_attribute('href')) 
        print('there are :'+ str(len(tag_li)) + ' links in this page') 
        #檢查用
        for prod_url in tag_li:
        ## 找是否有規格 不是每個商品都有規格
            driver.get(prod_url) # 跳轉進該商品頁面
            time.sleep(_DELAY)
            # 找商品標題
            try:
                pro_title = driver.find_elements_by_tag_name('h1')[0].text
            # 找是否有規格 
                elements = driver.find_elements_by_class_name("RadioButtons__radioBtn___qhOjt")
                if len(elements) > 0: # to aviod some error
                    for flavor in elements:
                        food.append(pro_title + "||"+ flavor.text)
                                
                else: # some items don't have flavor
                    food.append(pro_title)
                    #with('yahoo_cookedfood.txt', 'a') as w:
                    #    w.write(pro_title + '\n')
            except:
                pass # sometimes 抓到的商品網址內沒有商品 載入失敗的話
            
        # save
        for item in food:
            with open('yahoo_cookedfood2.txt', 'a') as w:
                #food_check  = sorted(set(food),key = food.index)
                w.write(item + '\n')
                
    
    except:
        pass
    
    
# 抓
page = 1 # 追蹤第幾頁有問題
n = 5 # 跳頁秒數 不能跳太快
for url in url_1[3:15]:
    driver.get(url)
    get_yahoo_name(url)
    print('This is page: '+ str(page))
    time.sleep(n)
    #n += 0.5
    page += 1