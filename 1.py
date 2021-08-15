# Подключаем selenium (сперва установить через pip install selenium)
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
browser.get('https://nnmclub.to/')

# Получаем указатель на поле ввода текста в форме постинга
# textarea=browser.find_element_by_css_selector('#index_email')
# Печатаем в поле ввода какой-либо текст
# textarea.send_keys('email@mail.ru')

# Получаем указатель на поле ввода пароля
# textarea=browser.find_element_by_css_selector('#index_pass')
# Печатаем в поле ввода пароль
# textarea.send_keys('password')

#Получаем указатель на кнопку "Войти"
# submit=browser.find_element_by_css_selector('#index_login_button')
#Нажимаем эту кнопку
# submit.click()

time.sleep(10)




