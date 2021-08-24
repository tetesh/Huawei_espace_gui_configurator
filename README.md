# Huawei_Espace7910_gui_configurator

![alt text](https://github.com/tetesh/Huawei_espace_gui_configurator/blob/master/screeenshot.png)

USAGE:

1. Take the config file from the configured espace 7910 at your company, and rename it Config-eSpace7910_old.xml
2. Replace the lines <Account1>, <Auth> and <UIEMUser> with:
  
  <Account1 Enable="1" Account="" LogOut="0" LabelName="" UCAccount="" PGMNumber="" CorpID="" PhysicalLocation="" JointUserNum="">
  <Auth UserName="" Passwd=""/>
  <UIEMUser UserNO="" UserName="" PassWord="******" UnLoadTime="" isLogOut="0" isStorePasswd="0"/>
    
3. Put in the folder with the script
4. For the re-registration function to work in Huawei_espace_configurator.py, change the variables:
    
   web_user_my_company = 'you_user'
   web_passwd_my_company = 'you_password'
6. Change variable  chrome_options.binary_location = '~/chrome_win/GoogleChromePortable/App/Chrome-bin/chrome.exe' ( I using chrome portable)
   Important: The chromedriver presented here is only suitable for browser version 92, if you want to use a different version of the driver, replace chromedriver 
5. install package selenium, webdriver, pyinstaller using pip    
6. RUN: pyinstaller.exe ./Huawei_espace_configurator.py --add-binary "./driver/chromedriver.exe;./driver" --add-data "./Config
-eSpace7910_old.xml;./"
    
