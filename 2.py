from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")

capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptSslCerts'] = True
capabilities['acceptInsecureCerts'] = True

# Получаем в переменную browser указатель на браузер
browser = webdriver.Chrome(chrome_options=chrome_options,desired_capabilities=capabilities)

# Переходим на страницу, на которой нужно что-то сделать
browser.get('http://demo.mt.lv/webfig')
browser.get('http://demo.mt.lv/webfig/#Bridge')
time.sleep(12)
add_bridge = browser.find_element_by_class_name('button')
add_bridge.click()
rw_value = browser.find_element_by_xpath('//*[@id="content"]/table[3]/tbody[3]/tr/td[3]/input')
test = 'bridgetest'
rw_value.clear()
rw_value.send_keys('test')