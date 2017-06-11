from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random

driver = webdriver.Chrome()

driver.get("http://localhost:8000/login/")
e = driver.find_element_by_id('id_username')
e.send_keys('selenek')
e = driver.find_element_by_id('id_password')
e.send_keys('selenium')
driver.find_element_by_css_selector("button[type=submit]").click()

driver.get("http://localhost:8000/quiz/Brain%20Type")

def answer(driver, dist, idx):
    r = random.random()
    i = 0
    while r > dist[i]:
        i += 1
    id = idx[i]
    elem = driver.find_element_by_id(str(id))
    elem.click()

for i in range(32):
    answer(driver, [0.07, 0.12, 0.38, 1.], [23, 24, 25, 26])
    answer(driver, [0.05, 0.08, 0.89, 1.], [27, 28, 29, 30])
    answer(driver, [0.08, 0.68, 0.78, 1.], [31, 32, 33, 34])
    answer(driver, [0.22, 0.25, 0.92, 1.], [35, 36, 37, 38])
    answer(driver, [0.82, 0.83, 0.93, 1.], [39, 40, 41, 42])
    answer(driver, [0.74, 0.8, 0.98, 1.], [43, 44, 45, 46])
    answer(driver, [0.1, 0.12, 0.45, 1.], [47, 48, 49, 50])
    answer(driver, [0.05, 0.23, 0.27, 1.], [51, 52, 53, 54])
    answer(driver, [0.1, 0.25, 0.26, 1.], [55, 56, 57, 58])
    answer(driver, [0.1, 0.32, 0.96, 1.], [59, 60, 61, 62])
    answer(driver, [0.02, 0.1, 0.24, 1.], [63, 64, 65, 66])
    answer(driver, [0.87, 0.98, 0.99, 1.], [67, 68, 69, 70])
    answer(driver, [0.21, 0.25, 0.3, 1.], [71, 72, 73, 74])
    answer(driver, [0.08, 0.76, 0.96, 1.], [75, 76, 77, 78])
    answer(driver, [0.1, 0.79, 0.97, 1.], [79, 80, 81, 82])
    elem = driver.find_element_by_css_selector("input[type=submit]")
    elem.click()

# driver.close()