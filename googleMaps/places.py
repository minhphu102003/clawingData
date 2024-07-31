import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import json

def extract_rating_and_comments(text):
    # Sử dụng regex để tách số sao và số bài đánh giá
    rating_match = re.search(r'(\d+,\d+|\d+\.\d+|\d+) sao', text)
    comments_match = re.search(r'(\d+) bài đánh giá', text)
    
    if rating_match and comments_match:
        rating = rating_match.group(1)
        comments = comments_match.group(1)
        return rating, comments
    else:
        return None, None

def extract_coordinates(url):
    # Sử dụng regex để trích xuất tọa độ từ URL
    pattern = r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)"
    match = re.search(pattern, url)
    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return latitude, longitude
    else:
        return None

def getPlaces(url,type):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)  # Tăng thời gian chờ

    try:
        buttonElements = driver.find_elements(By.CLASS_NAME,'e2moi')
        buttonElements[type].click()
        
        time.sleep(3)

        if type != 1:
            siblideElements = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
        else:
            siblideElements = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')
        

        places = []
        
        # Hàm cuộn xuống để load thêm các phần tử
        def scroll_down():
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", siblideElements)
            time.sleep(3)  # Chờ một chút để phần tử mới được tải

        # Lặp lại quá trình cuộn và load các phần tử mới
        previous_div_count = 0
        while True:
            scroll_down()
            preceding_divs = siblideElements.find_elements(By.XPATH, './div')
            current_div_count = len(preceding_divs)
            if current_div_count == previous_div_count:
                break  # Dừng lại nếu không còn phần tử mới được tải
            previous_div_count = current_div_count
            for div in preceding_divs[len(places):]:  # Chỉ xử lý các phần tử mới
                try:
                    place = {}
                    linkElement = div.find_element(By.CLASS_NAME, 'hfpxzc')
                    place['type'] = type+1
                    place['link'] = linkElement.get_attribute('href')
                    coordinates = extract_coordinates(place['link'])
                    place['latitude'] = coordinates[0]
                    place['longitude'] = coordinates[1]
                    nameElement = div.find_element(By.CLASS_NAME, 'fontHeadlineSmall')
                    place['name'] = nameElement.get_attribute('innerText')
                    contentElement = div.find_element(By.CLASS_NAME,'AJB7ye')
                    spanTarget = contentElement.find_element(By.XPATH,'./span[2]')
                    spanSpecify = spanTarget.find_element(By.XPATH,'./span')
                    rating, comments = extract_rating_and_comments(spanSpecify.get_attribute('aria-label'))
                    place['star'] = rating
                    place['comment'] = comments
                    containerImg = div.find_element(By.CLASS_NAME,'SpFAAb')
                    imgElement = containerImg.find_element(By.XPATH,'./div/div/img')
                    place['img'] = imgElement.get_attribute('src')
                    places.append(place)
                except Exception as e:
                    pass
        
        return places
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    placeTotal = []
    for i in range(4):
        URL = 'https://www.google.com/maps/@16.07587,108.1624807,15.25z?authuser=0&hl=vi&entry=ttu'
        place = getPlaces(URL,i)
        placeTotal.append(place)
        # Lưu kết quả vào file JSON
    with open('places1.json', 'w', encoding='utf-8') as json_file:
        json.dump(placeTotal, json_file, ensure_ascii=False, indent=4)