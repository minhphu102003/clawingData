import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import sys

# ! Đầu tiên là đọc file từ bên kia 
# Sau đó nhờ vào link để tiếp tục lấy dữ liệu 

def getProductDetailData(url):
    stringUrl = url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(stringUrl, headers=headers)

    if response.status_code == 200 :
        soup = BeautifulSoup(response.text, 'html.parser')
        productElement = soup.find_all(class_='md:gap-6')
        if(productElement):
            productDetail = {}
            listImg = []
            imgs = productElement[0].find_all(class_='swiper-slide-active')
            print(imgs)
            for img in imgs:
                print(img)
        else:
            print('None')

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    url = 'https://www.pharmacity.vn/ladophar-nuoc-uong-lado-care-mars-giup-bo-than-trang-duong-hop-10-goi.html'
    getProductDetailData(url)