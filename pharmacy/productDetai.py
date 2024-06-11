from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def convertThousands(input):
    if input[-1].lower() == 'k':
        number = float(input[:-1])
        return int(number * 1000)
    else:
        return int(input)

def getProductDetail(url):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--incognito") # Chạy chorme ở chế độ ẩn danh
    chrome_options.add_argument("--window-size=1920x1080") # Đặt kích thước cửa sổ trình duyệt 
    chrome_options.add_argument("--headless") # Chạy ở chế độ không có giao diện người dùng
    chrome_options.add_argument("--no-sandbox") # Vô hiệu hóa sandbox của chorme
    # ! Tìm hiểu về sandbox của chorme
    chrome_options.add_argument("--disable-dev-shm-usage") # Vô hiệu hóa sử dụng /dev/shm (share memory).Tùy chọn này chuyển bộ nhớ dùng chung sang bộ nhớ đĩa để tránh vấn đề đó 
    # ! Cũng nên tìm hiểu về share memory

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)
    try:
        # ? Giờ tạo các đối tượng để chứa dữ liệu
        productDetail = {}
        listImg = []
        productDetail['nameProduct'] = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[1]/h1').text
        imgProduct = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/img');
        productDetail['srcImg'] = imgProduct.get_attribute('src')
        containerImg = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[3]/div/div/div[1]')
        listImgs = containerImg.find_elements(By.CSS_SELECTOR,'.swiper-slide')
        for Img in listImgs:
            listImg.append(Img.find_element(By.TAG_NAME, 'img').get_attribute('src'))
        productDetail['listImg'] = listImg
        productDetail['unknow']  = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/p').text
        rawBrand = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/a').text
        # ! Thương hiệu: Vidipha Tôi sẽ lấy được nội dung như thế này từ rawBrand và tôi cần phải tinh chỉnh lại để đưa vào csdl
        productDetail['brand'] = rawBrand.split(':')[1].strip()

        rawPrice = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[3]/h3').text
        price = rawPrice.split(':')[0]
        productDetail['price'] = price


        rawLike = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[5]/div/div/div[2]/p').text
        like = convertThousands(rawLike)
        productDetail['like'] = like
        

        rawSold = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[5]/div/p').text
        rawSold = rawSold.split(' ')[2]
        sold = convertThousands(rawSold)
        productDetail['sold'] = sold

        productDetail['category'] = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[7]/div[2]/div[1]/div').text

        productDetail['activeIngredient'] = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[7]/div[2]/div[2]/div').text

        productDetail['indication'] = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[7]/div[2]/div[3]/div').text

        productDetail['dosageForm'] = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[7]/div[2]/div[4]/div').text

        productDetail['productionPlace'] = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[7]/div[2]/div[5]/div').text

        productDetail['specifications'] = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[7]/div[2]/div[6]/div').text   

        listAttribute = ['ingredient','indication','contraindication', 'dosageInstructions','sideEffect','caution','drugInteraction']
        for i in range(len(listAttribute)):
            # print(driver.find_element(By.XPATH,f'//*[@id="radix-:R6pqdctdcalda:"]/div/div/p[{i+1}]').get_attribute('textContent'))
            productDetail[listAttribute[i]]= driver.find_element(By.XPATH,f'//*[@id="radix-:R6pqdctdcalda:"]/div/div/p[{i+1}]').get_attribute('textContent')
        lastElement = driver.find_element(By.XPATH,'//*[@id="radix-:R6pqdctdcalda:"]/div/div/p[8]').get_attribute('innerText')
        listElement = lastElement.split('\n')
        print(listElement)
        for e in listElement:
            if e != '\xa0' and ':' in e:
                print(e.split(':')[1])
                # ! Thiếu thêm thuộc tính vào trong product detail

        
                
        # print(productDetail)

    finally:
        # Close the browser
        driver.quit()

if __name__== "__main__":
    # ! Sau khi lấy được thông tin rồi ra sẽ đọc file excel đã cào được từ bên trang chủ để for lấy detail ở trong này
    stringUrl = 'https://www.pharmacity.vn/gynapax-hop-30-goi-x-5g.html'
    getProductDetail(stringUrl)