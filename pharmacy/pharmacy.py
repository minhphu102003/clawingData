from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import sys

def clawingDataPharmacy(stringUrl):
    options = Options()
    options.headless = True  # Chạy trình duyệt ẩn danh
    driver = webdriver.Chrome(options=options)

    url = stringUrl
    driver.get(url)
    time.sleep(5)  # Chờ 5 giây để trang web tải hoàn chỉnh
    
    listPharmacys = driver.find_elements(By.CLASS_NAME, 'store-list')
    for pharmacy in listPharmacys:
        pharmacyItems = pharmacy.find_elements(By.CLASS_NAME, 'cursor-pointer')
        if pharmacyItems:
            for pharmacyItem in pharmacyItems:
                listPharagraphs = pharmacyItem.find_elements(By.TAG_NAME, 'p')
                if listPharagraphs:
                    for listPharagraph in listPharagraphs:
                        print(listPharagraph.text)
                listLinkMap = pharmacyItem.find_elements(By.TAG_NAME, 'a')
                if listLinkMap:
                    for link in listLinkMap:
                        print(link.get_attribute('href'))



    driver.quit()  # Đóng trình duyệt sau khi hoàn thành

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    stringUrl = 'https://www.pharmacity.vn/he-thong-cua-hang'
    clawingDataPharmacy(stringUrl)
