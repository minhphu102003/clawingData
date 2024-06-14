import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from config import EMAIL, PASSWORD

def clawingComment(url):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)

    try:
        commentNumber = int(driver.find_element(By.ID, 'total_comment').text)
        commentElement = driver.find_element(By.ID, 'box_comment')
        commentValue = []
        listComments = commentElement.find_elements(By.CLASS_NAME, 'content-comment')

        # Tiếp tục tải thêm bình luận
        while len(listComments) < commentNumber:
            try:
                showElement = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'show_more_coment'))
                )
                showElement.click()
                time.sleep(2)
                try:
                    # Chuyển sang iframe 
                    iframe = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="dark_theme"]/div[2]/div/div[1]/div/iframe')))
                    driver.switch_to.frame(iframe)

                    # Nhập thông tin đăng nhập
                    email_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'myvne_email_input')))
                    password_input = driver.find_element(By.ID, 'myvne_password_input')
                    email_input.send_keys(EMAIL)
                    password_input.send_keys(PASSWORD)
                    buttonLogin = driver.find_element(By.ID, 'myvne_button_login')
                    buttonLogin.click()

                    # Đợi trang đăng nhập hoàn tất và tải lại
                    time.sleep(5)
                    driver.switch_to.default_content()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'box_comment'))
                    )

                    print('Đăng nhập thành công')

                    listComments = driver.find_elements(By.CLASS_NAME, 'content-comment')
                    print(len(listComments))
                except Exception as e:
                    print('login error', e)
                    driver.switch_to.default_content()
            except Exception as e:
                print("An error occurred while loading more comments:", e)
                break

        for comment in listComments:
            people = {}
            try:
                fullContent = comment.find_element(By.CLASS_NAME, 'full_content')
                listSpan = fullContent.find_elements(By.TAG_NAME, 'span')
                people['name'] = listSpan[0].text
                comment_text = fullContent.text.replace(people['name'], '')
                people['comment'] = comment_text
                commentValue.append(people)
            except:
                try:
                    contentMore = comment.find_element(By.CLASS_NAME, 'content_more')
                    listSpan = contentMore.find_elements(By.TAG_NAME, 'span')
                    people['name'] = listSpan[0].get_attribute('textContent')
                    comment_text = contentMore.get_attribute('textContent').replace(people['name'], '')
                    people['comment'] = comment_text
                    commentValue.append(people)
                except Exception as inner_e:
                    print(f"No content found for a comment: {inner_e}")

        print(commentValue)

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    # ! Vẫn đang bị lỗi ở đăng nhập vì trang web xác định được bot từ selenium và ngăn chặn không cho đăng nhập 
    url = 'https://vnexpress.net/dua-tre-khong-duoc-an-dui-ga-4751249.html'
    clawingComment(url)
