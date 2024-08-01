from dotenv import load_dotenv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Adding the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import config

# Load environment variables from .env file
load_dotenv()

# Get email and password from environment variables
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

def set_options():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login(email, password, driver):
    login_url = config.LINK_LOGIN_FACEBOOK
    try:
        driver.get(login_url)
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'pass')

        # Input the email and password
        email_field.send_keys(email)
        password_field.send_keys(password)

        # Submit the form (e.g., clicking the login button)
        login_button = driver.find_element(By.ID, 'loginbutton')
        login_button.click()

        # Wait for a while to let the page load
        time.sleep(5)
        print('Logged in successfully')
    except Exception as e:
        print(f"An error occurred during login: {e}")
        raise

def findPage(page, driver):
    if page:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'x1ba4aug')))
            label_element = driver.find_element(By.CLASS_NAME,'x1ba4aug')
            label_element.click()
            time.sleep(5)
            find_element = label_element.find_element(By.XPATH,'./input')
            find_element.send_keys(page)
            find_element.send_keys(Keys.RETURN)  # Simulate pressing Enter key
            time.sleep(10)
            print(f"Searching for page: {page}")
            
        except Exception as e:
            print(f"An error occurred during search: {e}")
    else:
        raise ValueError("The page string is empty")

if __name__ == '__main__':
    namePage = input('Nhập tên page mà bạn muốn tìm kiếm: ')
    driver = set_options()
    try:
        login(email, password, driver)
        find(namePage, driver)
        # Keep the browser open for an additional minute before closing
        time.sleep(60)
    finally:
        driver.quit()
