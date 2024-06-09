from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import pandas as pd

import time

def choose_option(xpath_prefix,driver):
    numbers = [1, 2, 3, 4, 5]
    weights = [1, 1, 4, 5, 3]
    selected_number = random.choices(numbers, weights=weights, k=1)[0]
    choice = driver.find_element(By.XPATH, f"{xpath_prefix}/div[{selected_number + 1}]/div/div")
    choice.click()



def generateEmail():
    df = pd.read_excel('Data.xlsx')
    row  = df.shape[0]
    numberRandom = random.randint(0,row-1)
    name = df.iloc[numberRandom,2]
    numberRandom = random.randint(0,row-1)
    middleName = df.iloc[numberRandom,3]
    domain = "@gmail.com"
    number = random.randint(100,10**5)
    email = str(name) + str(middleName) + str(number) + str(domain)
    return email

def autoFillForm():
    for _ in range(100):
        #khởi tạo trình duyệt chrome
        driver  = webdriver.Chrome()

        #mở url của google Form 
        driver.get('https://docs.google.com/forms/d/e/1FAIpQLSfXRFzrbWhPI3LCatQ_g8C4QI8Sjpw8EK7KHptqpNvqJchseA/viewform')


        # Đợi một lát để trang tải hoàn toàn
        time.sleep(2)
        email = generateEmail()
        input1 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/input')
        input1.send_keys(email)
        print(email)

        options_xpath = {
        "gender": ['//*[@id="i9"]', '//*[@id="i12"]'],
        "old": ['//*[@id="i19"]', '//*[@id="i22"]', '//*[@id="i25"]', '//*[@id="i28"]'],
        "branch": ['//*[@id="i35"]', '//*[@id="i38"]', '//*[@id="i41"]', '//*[@id="i44"]'],
        "earn": ['//*[@id="i51"]', '//*[@id="i54"]', '//*[@id="i57"]', '//*[@id="i60"]']
        }

        for key, xpath_list in options_xpath.items():
            random_index = random.randint(0, len(xpath_list) - 1)
            chosen_xpath = xpath_list[random_index]
            option_button = driver.find_element(By.XPATH, chosen_xpath)
            option_button.click()

        serviceExperience = driver.find_element(By.XPATH,'//*[@id="i67"]')
        serviceExperience.click()

        nextButton = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div')
        nextButton.click()


        time.sleep(5)

        for i in range(3, 9):
            for j in range(2, 11, 2):
                path = f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[{i}]/div/div/div[2]/div/div[1]/div/div[{j}]/span'
                choose_option(path, driver)

        submitButton = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div[2]')
        submitButton.click()
        driver.quit()


if __name__ == "__main__":
    autoFillForm()