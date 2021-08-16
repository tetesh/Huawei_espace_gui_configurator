from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time, os, sys, threading
from tkinter import *
import tkinter.ttk as ttk

def all_func(ip_addr, number, password):
    pb.start()
    pb_status['text'] = 'В процессе!'
    #открываем шаблон конфига и исправляем в нем учетные данные. Важно: учетные данные от веб морды уже исправлены в шаблоне на: admin:Huawei79, а также уже указан мой server asterisk, и мой ntp server. Вам же будет проще подменит Config_old на свой!
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

    #Добавляем аргумет заставляющий работать Chrome в скрытном режиме
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    #Отключаем проверку сертификатов
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    # Получаем в переменную browser указатель на webdriver
    browser = webdriver.Chrome('./driver/chromedriver.exe', chrome_options=chrome_options, desired_capabilities=capabilities)
    # Переходим на страницу
    browser.get('https://' + ip_addr)
    time.sleep(8)
    # Ищем элемент ввода и отправляем стандартные учетные данные
    login = browser.find_element_by_id('user_name_txt')
    login.send_keys('admin')
    # Ищем элемент ввода и отправляем стандартные учетные данные
    passwd = browser.find_element_by_id('password_txt')
    passwd.send_keys('admin123')
    # Нажимаем кнопку авторизации
    login_btn = browser.find_element_by_id('login_btn')
    login_btn.click()
    time.sleep(12)

    try:  # Проверка авторизации (если пароль не стандартный - скрипт не зайдет в и нтерфейс и не найдет нужный элемент)
        close_def_passwd = browser.find_element_by_id('ontBtn_yes_a')
        close_def_passwd.click()
    except NoSuchElementException:
        print('Телефон уже был настроен, для настройки через эту программу сбростье его до заводских настроек!')
        browser.close()
        sys.exit()

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
    time.sleep(60)
    pb.stop()
    pb_status['text'] = 'Готово, проверяйте работу!'

root = Tk()
root.geometry('420x250+1000+300')
# root.maxsize(420, 250)
# root.minsize(420, 250)
f = Frame(root, bg='#FBCEB1')
f.pack()


l_ip = Label(f, text='Введите Ip адрес:', fg='black', bg='#FBCEB1', font=('Courier New', 12, 'bold'), padx=10)
l_ip.grid(row=0, column=0, pady=10, sticky=W)
e_ip = Entry(f)
e_ip.grid(row=0, column=2, sticky=W+E, padx=10, pady=20)
l_user = Label(f, text='Введите sip user:', fg='black', bg='#FBCEB1', font=('Courier New', 12, 'bold'), padx=10)
l_user.grid(row=1, column=0, pady=10, sticky=W)
l_password = Label(f, text='Введите sip password:', padx=10, pady=10, fg='black', bg='#FBCEB1', font=('Courier New', 12, 'bold'))
l_password.grid(row=2, column=0, pady=10, sticky=W)
e_user = Entry(f)
e_user.grid(row=1, column=2, sticky=W+E, padx=10, pady=10)
e_password = Entry(f)
e_password.grid(row=2, column=2, sticky=W+E, padx=10, pady=10)
pb = ttk.Progressbar(f, orient='horizontal', mode='indeterminate', length=280)
# pb.start()
# pb.stop()
pb.grid(row=4, column=0, columnspan=3, pady=10, padx=30, sticky=W+E)
pb_status = Label(f, fg='black', bg='#FBCEB1', font=('Courier New', 15, 'bold'), padx=10)
pb_status.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky=W)

# def progress():
#     pb_status['text'] = 'В процессе!'
#     time.sleep(60)
#     pb_status['text'] = 'Готово!'

# def functions(ip_addr, number, password):
#     global pb_status
#     pb_status['text'] = 'В процессе!'
#     all_func(ip_addr, number, password)
#     time.sleep(60)
#     pb_status['text'] = 'Готово!'


btn_configure = Button(f, text='Настроить', pady=5, fg='#008080', bg='lightgray', command=lambda: all_func(e_ip.get(), e_user.get(), e_password.get())).grid(row=3, column=0, sticky=W, padx=30)

root.mainloop()
