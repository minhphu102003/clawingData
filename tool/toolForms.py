from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time

def set_aria_checked_true(element,driver):
    driver.execute_script("arguments[0].setAttribute('aria-checked', 'true');", element)

def choose_option(xpath_prefix,driver):
    numbers = [1, 2, 3, 4, 5]
    weights = [1, 2, 5, 6, 4]
    selected_number = random.choices(numbers, weights=weights, k=1)[0]
    choice = driver.find_element(By.XPATH, f"{xpath_prefix}/div[{selected_number + 1}]/div/div")
    choice.click()


def autoFill():
    for k in range(10):
        driver = webdriver.Chrome()
        driver.get('https://docs.google.com/forms/d/e/1FAIpQLScGszQxNfOMZjhEtR6NthO4PiakL0-0prYlzqVl11uvwGu-Eg/viewform')
        time.sleep(2)

        options_xpath = {
        "gender": ['//*[@id="i5"]', '//*[@id="i8"]'],
        "old": ['//*[@id="i15"]', '//*[@id="i18"]', '//*[@id="i21"]', '//*[@id="i24"]'],
        "branch": ['//*[@id="i31"]', '//*[@id="i34"]', '//*[@id="i3"]', '//*[@id="i40"]'],
        "earn": ['//*[@id="i47"]', '//*[@id="i50"]', '//*[@id="i53"]', '//*[@id="i56"]']
        }

        for key, xpath_list in options_xpath.items():
            if key == 'old':
        # Tạo một phân phối ngẫu nhiên với 60% tỉ lệ cho index 0 và 1
                random_index = random.choices(range(len(xpath_list)), weights=[6, 6, 2, 1])[0]
            elif key == 'earn':
                random_index = random.choices(range(len(xpath_list)), weights=[1, 5, 7, 3])[0]
            else:
                random_index = random.randint(0, len(xpath_list) - 1)
            chosen_xpath = xpath_list[random_index]
            option_button = driver.find_element(By.XPATH, chosen_xpath)
            option_button.click()
        serviceExperience = driver.find_element(By.XPATH,'//*[@id="i63"]')
        serviceExperience.click()
        nextButton = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div')
        nextButton.click()
        time.sleep(6)

        for i in range(2, 8):
            for j in range(2, 11, 2):
                path = f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[{i}]/div/div/div[2]/div/div[1]/div/div[{j}]/span/'
                choose_option(path, driver)


        submitButton = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div[2]')
        submitButton.click()
        driver.quit()
        print(k)
if __name__ =="__main__":
    autoFill()

