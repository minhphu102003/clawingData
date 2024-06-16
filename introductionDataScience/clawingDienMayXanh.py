import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os

def getLinkCategory(url):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)
    linkCategory = []
    try:
        menuElement = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/section/div[2]/div[1]')
        hrefElements = menuElement.find_elements(By.TAG_NAME, 'a')
        for item in hrefElements:
            linkCategory.append(item.get_attribute('href'))
        return linkCategory
    except Exception as e:
        print(e)
        return []
    finally:
        driver.quit()


def getLinkProduct(url):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)
    linkProduct = []
    try:
        while True:
            try:
                moreElement = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="categoryPage"]/div[3]/div[2]'))
                )
                if 'none' in moreElement.get_attribute('style'):
                    break
                moreElement.click()
                time.sleep(2)
            except Exception:
                break

        menuProduct = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="categoryPage"]/div[3]/ul'))
        )
        itemsProduct = menuProduct.find_elements(By.XPATH, './li')

        for item in itemsProduct:
            try:
                link = item.find_element(By.TAG_NAME, 'a')
                linkProduct.append(link.get_attribute('href'))
            except Exception as e:
                print(f"Could not find link in item: {item.get_attribute('outerHTML')}, error: {e}")
        return linkProduct
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        driver.quit()


def getComment(driver):
    commentList = []
    listComment = driver.find_element(By.CSS_SELECTOR, '.comment-list')
    itemsComment = listComment.find_elements(By.XPATH, './li')
    for item in itemsComment:
        comment = {}
        start = item.find_element(By.CSS_SELECTOR, '.cmt-top-star')
        numberStart = len(start.find_elements(By.CSS_SELECTOR, '.iconcmt-starbuy'))
        comment['star'] = numberStart
        try:
            content = item.find_element(By.CSS_SELECTOR, '.cmt-content ')
            commentValue = content.find_element(By.TAG_NAME, 'p').get_attribute('innerText')
            comment['content'] = commentValue
        except:
            comment['content'] = ''
        commentList.append(comment)
    return commentList


def getCommentProduct(url):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    # ? sẽ có vài sản phẩm comment rất nhiều nên thời gian cào dữ liệu rất lâu nên ta cần cofigure để có thể cào hết tất cả dữ liệu
    driver.set_page_load_timeout(300) 
    driver.get(url)
    time.sleep(3)

    # ? Tạo đối tượng product để chứa giá trị của từng tên và comment của sản phẩm đó 
    product = {
        "nameProduct": "",
        "url": url,
        "comments": []
    }

    try:
        # ! Lấy tên của sản phẩm
        # Sẽ có vài sản phẩm theo format khác nhưng nó thiểu số và không có comment nên ở except cũng không làm gì 
        containerName = driver.find_element(By.CSS_SELECTOR, '.detail.detail_42')
        nameProduct = containerName.find_element(By.XPATH, './h1')
        product["nameProduct"] = nameProduct.get_attribute('innerText')
        try:
            # ! Sẽ có vài sản phẩm comment ít (<5 comment) sẽ không có nút xem thêm đánh giá nên 
            # Ở except ta sẽ xử lý đẻ lấy những comment đó 
            parentElement = driver.find_element(By.CSS_SELECTOR, '.box-flex')
            seeMore = parentElement.find_element(By.XPATH, './a')
            seeMore.click()
            comment = getComment(driver)
            product["comments"].extend(comment)
            pageCurrent = 1
            try:
                check = True
                # ! Nhiều page nên phải for từng page và reaload trang liên tục nên DOM sẽ bị biến đổi, thay vì for list DOM selector 
                # Thì ta while true và waitDriver cho bớt lỗi và dễ làm hơn
                while check:
                    try:
                        if pageCurrent == 1:
                            pageElement = driver.find_element(By.CSS_SELECTOR, '.pagcomment')
                            listLinks = pageElement.find_elements(By.TAG_NAME, 'a')
                            maxPage = int(listLinks[-2].text)
                        else:
                            pageElement = driver.find_element(By.CSS_SELECTOR, '.pagcomment')
                        listLinks = pageElement.find_elements(By.TAG_NAME, 'a')

                        if pageCurrent != 1:
                            listLinks = listLinks[1:]
                        for link in listLinks:
                            if int(link.text) > pageCurrent:
                                pageCurrent = int(link.text)
                                link.click()
                                WebDriverWait(driver, 10).until(
                                EC.staleness_of(link)
                                )
                                WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.comment-list'))
                                )
                                comment = getComment(driver)
                                product["comments"].extend(comment)
                                break
                            #? Xác định trang cuối để thoát while
                            elif pageCurrent == maxPage:
                                check = False
                            elif int(link.text) <= pageCurrent:
                                pass
                    except Exception as e:
                        print(e)
                        check = False    
            except Exception as e:
                print(e)
        except Exception as e:
            comment = getComment(driver)
            product["comments"].extend(comment)   
    except Exception as e:
        print(e)
    finally:
        driver.quit()

    return product

if __name__ == "__main__":
    url = 'https://www.dienmayxanh.com/dien-thoai'
    # linkCategory = getLinkCategory(url)
    # linktotal = []
    # for link in linkCategory:
    #     linkProduct = getLinkProduct(link)
    #     linktotal.extend(linkProduct)

    # with open('product_links.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['product_link'])
    #     for link in linktotal: 
    #         writer.writerow([link])

    with open('product_links.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader) 
        links = [row[0] for row in reader]

    products = []
    output_file = 'products.json'
    
    if not os.path.isfile(output_file):
        with open(output_file, mode='w', encoding='utf-8-sig') as file:
            json.dump([], file, ensure_ascii=False, indent=4)
    
    with open(output_file, mode='r', encoding='utf-8-sig') as file:
        products = json.load(file)

    for link in links:
        product = getCommentProduct(link)
        products.append(product)
        with open(output_file, mode='w', encoding='utf-8-sig') as file:
            json.dump(products, file, ensure_ascii=False, indent=4)
