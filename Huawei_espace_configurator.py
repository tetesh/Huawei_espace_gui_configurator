from selenium import webdriver
#from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time, os
from tkinter import *

web_user_my_company = 'admin'
web_passwd_my_company = 'Huawei79!'

def all_func(ip_addr, number, password, web_login, web_password, flag):

    pb_status['text'] = 'В процессе!'
    pb_status.update()
    # открываем шаблон конфига и исправляем в нем учетные данные. Важно: учетные данные от веб морды уже исправлены в шаблоне на: admin:Huawei79, а также уже указан мой server asterisk, и мой ntp server. Вам же будет проще подменит Config_old на свой и изменить данные строки!
    with open('Config-eSpace7910_old.xml', 'r') as f:
        old_data = f.read()
    new_data_1 = old_data.replace(
        '<Account1 Enable="1" Account="" LogOut="0" LabelName="" UCAccount="" PGMNumber="" CorpID="" PhysicalLocation="" JointUserNum="">\n<Auth UserName="" Passwd=""',
        f'<Account1 Enable="1" Account="{number}" LogOut="0" LabelName="{number}" UCAccount="" PGMNumber="" CorpID="" PhysicalLocation="" JointUserNum="">\n<Auth UserName="{number}" Passwd="{password}"')
    new_data_2 = new_data_1.replace(
        '<UIEMUser UserNO="" UserName="" PassWord="" UnLoadTime="" isLogOut="0" isStorePasswd="0" timeTag="0" ContactSyncTime="0" Roaming="0" RoamingTime="0"',
        f'<UIEMUser UserNO="{number}" UserName="{number}" PassWord="{password}" UnLoadTime="" isLogOut="0" isStorePasswd="0" timeTag="0" ContactSyncTime="0" Roaming="0" RoamingTime="0"')
    with open('Config-eSpace7910.xml', 'w') as f:
        f.write(new_data_2)

    chrome_options = Options()
    chrome_options.binary_location = './GoogleChromePortable/App/Chrome-bin/chrome.exe' #можно использовать системный chrome, тогда убрать данную строку, Важно chromedriver должен быть такой же версии, что и браузер
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-features=NetworkService")  ##this did it for me
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")

    # Получаем в переменную browser указатель на webdriver и передаем опции
    browser = webdriver.Chrome('./driver/chromedriver.exe', chrome_options=chrome_options)

    # Переходим на страницу
    try:
        browser.get('https://' + ip_addr)
        time.sleep(8)
    except WebDriverException:
        print('ip адрес не доступен!')
        browser.close()
        pb_status['text'] = 'ERROR: Узел недоступен!'
        return

    # Ищем элемент ввода и отправляем стандартные учетные данные #TODO способ нормальной проверки
    try:
        login = browser.find_element_by_id('user_name_txt')
        login.send_keys(web_login)
    except NoSuchElementException:
        print('Это не ip телефон Huawei 7910')
        browser.close()
        pb_status['text'] = 'ERROR: Это не ip телефон!'
        return

    # Ищем элемент ввода и отправляем стандартные учетные данные
    passwd = browser.find_element_by_id('password_txt')
    passwd.send_keys(web_password)
    # Нажимаем кнопку авторизации
    login_btn = browser.find_element_by_id('login_btn')
    login_btn.click()
    time.sleep(12)
    if flag == 1: # если телефон был уже настроен и реквизиты не стандартные, то не будет элемента 'ontBtn_yes_a'
        try:
            close_def_passwd = browser.find_element_by_id('ontBtn_yes_a')
            close_def_passwd.click()
        except NoSuchElementException:
            print('Телефон уже был настроен, для настройки через эту программу сбростье его до заводских настроек!')
            browser.close()
            # pb.stop()
            pb_status['text'] = 'ERROR: Телефон не на заводских настройках!'
    else:
        print('reconfigure')
    time.sleep(1)
    go_status = browser.find_element_by_id('label_status')
    go_status.click()
    time.sleep(1)
    go_information = browser.find_element_by_id('version_btn')
    go_information.click()
    time.sleep(1)
    version = browser.find_element_by_id('soft_version_td').text
    if 'eSpace7910' in version:
        print('phone eSpace7910')
    else:
        print('no')
        pb_status['text'] = 'ERROR: Это не 7910!'
        return
    time.sleep(1)
    go_advanced = browser.find_element_by_id('label_advanced')
    go_advanced.click()
    go_cfg_button = browser.find_element_by_id('config_btn')
    go_cfg_button.click()
    time.sleep(1)
    #передаем путь к нашему готовому файлу конфигурации
    input_files = browser.find_element_by_class_name('input_file')
    input_files.send_keys(os.path.abspath('Config-eSpace7910.xml'))
    #Импортием конфигурацию
    btn_import = browser.find_element_by_id('label_import_config_btn')
    btn_import.click()
    time.sleep(2)
    browser.close()
    print('Готово! После перезагрузки телефон будет готов!')
    pb_status['text'] = 'Готово! Телефон будет перезагружен!'


root = Tk() #создаем окно
root.geometry('380x220+1000+300') #размеры и положение на экране
root.maxsize(380, 220)
root.minsize(380, 220)
f = Frame(root, bg='#FBCEB1') #создаем фрейм
f.pack()


l_ip = Label(f, text='Введите ip адрес:', fg='black', bg='#FBCEB1', font=('Courier New', 10, 'bold'), padx=10)
l_ip.grid(row=0, column=0, columnspan=2, pady=10, sticky=W)

e_ip = Entry(f)
e_ip.grid(row=0, column=2, sticky=W+E, padx=10, pady=10)

l_user = Label(f, text='Введите sip user:', fg='black', bg='#FBCEB1', font=('Courier New', 10, 'bold'), padx=10)
l_user.grid(row=1, column=0, columnspan=2, pady=10, sticky=W)

l_password = Label(f, text='Введите sip password:', fg='black', bg='#FBCEB1', font=('Courier New', 10, 'bold'), padx=10)
l_password.grid(row=2, column=0, columnspan=2, pady=10, sticky=W)

e_user = Entry(f)
e_user.grid(row=1, column=2, sticky=W+E, padx=10, pady=10)

e_password = Entry(f)
e_password.grid(row=2, column=2, sticky=W+E, padx=10, pady=10)

pb_status = Label(f, fg='black', bg='#FBCEB1', font=('Courier New', 10, 'bold'))
pb_status.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky=W)

btn_configure = Button(f, text='Настроить', pady=5, fg='#008080', bg='lightgray', command=lambda: all_func(e_ip.get(), e_user.get(), e_password.get(), 'admin', 'admin123', 1)).grid(row=3, column=0, sticky=W, padx=10, pady=10)
#Кнопка перерегистрации. Реквизиты user, password, которые успользуются в моей компании, они же прописываются при настройке выше
btn_reconfigure = Button(f, text='Перерегистрация', pady=5, fg='#008080', bg='lightgray', command=lambda: all_func(e_ip.get(), e_user.get(), e_password.get(), web_user_my_company, web_passwd_my_company, 0)).grid(row=3, column=1, columnspan=2, sticky=W, padx=10, pady=10)
root.mainloop()
