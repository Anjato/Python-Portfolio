import pyautogui
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get("https://www.keybr.com")

while True:
    text = browser.find_element_by_xpath('//*[@id="App"]/div/div[3]/div/div[2]/div/span[1]')

    print(text)
