import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import traceback

def getCourses(url,code ,semeter):
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
        calender = []
        classElements = table.find_elements(By.CLASS_NAME,'lop')
        for classElement in classElements:
            # print(classElement.get_attribute('outerHTML'))
            td_elements = classElement.find_elements(By.TAG_NAME, 'td')
            classDetail = {
                'code': code,
                'semester':semeter,
            }
            classDetail['className'] = td_elements[0].text
            classDetail['classCode'] = td_elements[1].text
            classDetail['remainingSeats'] = td_elements[3].text
            classDetail['registrationDeadline'] = td_elements[4].text
            classDetail['schoolWeek'] = td_elements[5].text
            # ! Cần phải xử lý chuỗi ở chỗ này để tính được ngày giờ và số ngày hủy 
            classDetail['courseSchedule'] = td_elements[6].text
            print(classDetail['courseSchedule'])
            classDetail['place'] = td_elements[8].text
            classDetail['teacher'] = td_elements[9].text

            calender.append(classDetail)
        return calender    
            # ?  Tại sao lại không cần phòng vì lịch trong kì có thể được đổi và phòng học thường xuyên được sinh viên check theo ngày nên không cần thống kê làm gì 
    except Exception as e:
    # Xử lý ngoại lệ và in ra thông báo lỗi
        print("An error occurred:", e)
        return []
    finally: 
        driver.quit()


def readCSV(start=70, end=85):
    data  = pd.read_csv('./mydtu/subjectTile.csv')
    branch  = data.iloc[:,0]
    code = data.iloc[:,1]
    classCode = data.iloc[:,2]
    total = []
    for b, c, cc in zip(branch, code, classCode):
        URL = f'https://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx?keyword2={b}%24{c}&scope=1&hocky=83&t=1718353281436'
        course = getCourses(URL, cc,85)
        total.extend(course)
    df = pd.DataFrame(total)
    df.to_excel('courses.xlsx', index=False)




if __name__ == "__main__":
    # readCSV()
    URL = 'https://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx?keyword2=POS%24351&scope=1&hocky=83&t=1718353281436'
    course = getCourses(URL,'POS 351',83)
    print(course)
