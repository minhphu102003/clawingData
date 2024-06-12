import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import traceback

def getCourses(url):
    chrome_options = Options()
    chrome_options.add_argument("--incognito") # Chạy chorme ở chế độ ẩn danh
    chrome_options.add_argument("--window-size=1920x1080") # Đặt kích thước cửa sổ trình duyệt 
    chrome_options.add_argument("--headless") # Chạy ở chế độ không có giao diện người dùng
    chrome_options.add_argument("--no-sandbox") # Vô hiệu hóa sandbox của chorme
    # ! Tìm hiểu về sandbox của chorme
    chrome_options.add_argument("--disable-dev-shm-usage") # Vô hiệu hóa sử dụng /dev/shm (share memory).Tùy chọn này chuyển bộ nhớ dùng chung sang bộ nhớ đĩa để tránh vấn đề đó 

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)

    try:
        linkElement = driver.find_element(By.XPATH,'/html/body/div/table/tbody/tr/td[2]/a')
        linkElement.click()
        time.sleep(3)

        table = driver.find_element(By.CLASS_NAME,'tb-calendar')
        # print(table.get_attribute('outerHTML'))
        # ! Mình sẽ lấy số liệu về để thống kê
        course = {
            'code': 'POS 351',
            'semester': 83,
            'calender':'' 
        }
        calender = []
        classElements = table.find_elements(By.CLASS_NAME,'lop')
        for classElement in classElements:
            # print(classElement.get_attribute('outerHTML'))
            td_elements = classElement.find_elements(By.TAG_NAME, 'td')
            classDetail = {}
            classDetail['className'] = td_elements[0].text
            classDetail['classCode'] = td_elements[1].text
            classDetail['remainingSeats'] = td_elements[3].text
            classDetail['registrationDeadline'] = td_elements[4].text
            classDetail['schoolWeek'] = td_elements[5].text
            classDetail['courseSchedule'] = td_elements[6].text
            classDetail['place'] = td_elements[8].text
            classDetail['teacher'] = td_elements[9].text
            calender.append(classDetail)
        course['calender'] = calender
        print(course)    
            # ?  Tại sao lại không cần phòng vì lịch trong kì có thể được đổi và phòng học thường xuyên được sinh viên check theo ngày nên không cần thống kê làm gì 
    except Exception as e:
    # Xử lý ngoại lệ và in ra thông báo lỗi
        print("An error occurred:", e)
        traceback.print_exc()
    finally: 
        driver.quit()




if __name__ == "__main__":
    # ! Mục đích của mình là thống kê 
    url = ''
    # ! Cập nhật lên truyền vào getCourse sẽ có mã môn và học kỳ
    getCourses(url)
