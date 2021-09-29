import time
import pyautogui
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://play.typeracer.com/')
driver.maximize_window()

time.sleep(1)

race = driver.find_element_by_xpath('//*[@id="gwt-uid-1"]/a')
race.click()

# gives time for xpath to load and be found while running the loop statement(s)
time.sleep(4)

go = driver.find_element_by_class_name('lightLabel')
compare = "Go!"

while go.text != compare:
    time.sleep(0.1)
    print(go.text)

while go.text == compare:
    letters = driver.find_element_by_xpath('//*[@id="gwt-uid-20"]/table/tbody/tr[2]/td/table/tbody/tr['
                                           '1]/td/table/tbody/tr[1]/td/div/div')

    pyautogui.write(letters.text, interval=0.05)
    print(letters.text)
