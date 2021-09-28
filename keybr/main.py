import pyautogui
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.keybr.com")

while True:
    popup = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/a')
    popup.click()

    text = driver.find_element_by_class_name('TextInput-item TextInput-item')


    print(text)
