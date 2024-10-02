import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import json

def extractNumber(count_commnet):
    return int(count_commnet.replace("(","").replace(")",""))

def getListComment(url):
    chrome_option = Options()
    chrome_option.add_argument("--incognito")
    chrome_option.add_argument("--window-size=1920x1080")
    # chrome_option.add_argument("--headless")
    # chrome_option.add_argument("--no-sandbox")
    # chrome_option.add_argument("--disable-dev-shm-usage")

    driver =webdriver.Chrome(options=chrome_option)
    driver.get(url)
    time.sleep(5)

    try:
        comment_count = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span')
        number_comment = extractNumber(comment_count.get_attribute('innerText'))
        comment_button = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]')
        comment_button.click()
        time.sleep(5)
        mainListElement = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
        parentElment = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[12]')
        def scroll_down():
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", mainListElement)
            time.sleep(3)  # Chờ một chút để phần tử mới được tải
        previous_div_count = 0
        comments = []
        while True:
            scroll_down()
            current_divs = parentElment.find_elements(By.XPATH, './div')
            current_div_count  = len(current_divs)
            if current_div_count == number_comment:
                break
            previous_div_count == current_div_count
            print(current_div_count)
            print(number_comment)
            for div in current_divs[len(comments):]:
                try:
                    comment = {}
                    userNameElement = div.find_element(By.XPATH,'./div/div/div[1]/div[1]/div[0]/button/div[0]')
                    comment['username'] = userNameElement.get_attribute('innerText')
                    containerContent = div.find_element(By.XPATH,'./div/div/div[3]')
                    startElement = containerContent.find_element(By.XPATH,'./div[0]/span[0]')
                    timeElement = containerContent.find_element(By.XPATH,'./div[0]/span[1]')
                    comment['star'] = startElement.get_attribute('aria-label')
                    comment['time'] = timeElement.get_attribute('innerText')
                    contentElement = containerContent.find_element(By.XPATH,'./div[1]/div')
                    spanMoreElement = contentElement.find_element(By.XPATH,'./span[1]/button')
                    if spanMoreElement :
                        spanMoreElement.click()
                        time.sleep(3)
                        extractConent = contentElement.find_element(By.XPATH,'./span[0]')
                    else:
                        extractConent = contentElement.find_element(By.XPATH, './span')
                    comment['content'] = extractConent.get_attribute('innerText')
                    containerImgElement = containerContent.find_element(By.XPATH,'./div[2]')
                    listImgElement = containerImgElement.find_elements(By.XPATH,'./button')
                    if listImgElement:
                        listImg = []
                        for button in listImgElement:
                            listImg.append(button.get_attribute('style'))
                    comment['listImg'] = listImg
                    print(comment)
                    print("")
                    comments.append(comment)
                except Exception as e:
                    print("An error occurred : ",e)

    except Exception as e:
        print("An error occurred: ",e)
    finally:
        driver.quit()

if __name__== "__main__":
    url = 'https://www.google.com/maps/place/Nh%C3%A0+H%C3%A0ng+Nh%C3%A0+%C4%90%E1%BB%8F/data=!4m7!3m6!1s0x31421d34928496a3:0x40fb32a2b9ccc332!8m2!3d16.0624172!4d108.2038722!16s%2Fg%2F11hnwy8_62!19sChIJo5aEkjQdQjERMsPMuaIy-0A?authuser=0&hl=vi&rclk=1'
    getListComment(url)