import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Đọc file đùng link để đi cào comment
# Và lưu thêm đường dẫn img vào 
def readFile(path):
    with open(path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        for type in data:
            print(len(type))
            for place in type:
                print(place['img'])
                print(place['link'])

def clawingComment(url):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5) 

    try:
        containerElement = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]')
        time.sleep(3)
        while True:
            try:
                # Kiểm tra xem phần tử có xuất hiện không
                expandMoreElement = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[50]/div/button/div')
                print("expandMoreElement đã được tìm thấy!")
                break  # Thoát khỏi vòng lặp nếu phần tử xuất hiện
            except NoSuchElementException:
                # Nếu chưa thấy phần tử, cuộn xuống và đợi một chút
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", containerElement)
                time.sleep(2)  # Thời gian chờ để nội dung tải thêm
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    

if __name__ == '__main__':
    url = 'https://www.google.com/maps/place/Nh%C3%A0+H%C3%A0ng+Nh%C3%A0+%C4%90%E1%BB%8F/@16.0624172,108.2038722,17z/data=!3m1!4b1!4m6!3m5!1s0x31421d34928496a3:0x40fb32a2b9ccc332!8m2!3d16.0624172!4d108.2038722!16s%2Fg%2F11hnwy8_62?authuser=0&hl=vi&entry=ttu&g_ep=EgoyMDI1MDEwMS4wIKXMDSoASAFQAw%3D%3D'
    clawingComment(url)