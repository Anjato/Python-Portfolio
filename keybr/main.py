import time
import pyautogui
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.keybr.com/login/tvP9PDi0p4")


# Clicks on Multiplayer Tab
'''
multiplayer = driver.find_element_by_xpath('//*[@id="Nav"]/div/div[7]/a/span')
multiplayer.click()
'''


# Clicks on Practice Tab
practice = driver.find_element_by_xpath('//*[@id="Nav"]/div/div[3]/a/span')
practice.click()


''' Originally needed when not using the direct account sign in link as being used above and instead
    only opening https://www.keybr.com/. This would then close the popup message and click on the
    "click to activate" text in order for it to start typing
# popup = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/a')
# popup.click()
# activate = driver.find_element_by_xpath('//*[@id="App"]/div/div[3]/div/div[3]')
# activate.click()
'''


# gives time for xpath to load and be found while running the loop statement(s)
time.sleep(3)

# Practice
while True:
    letters_uni = driver.find_element_by_xpath('//*[@id="App"]/div/div[3]/div/div[2]')
    unicode = letters_uni.text.replace(u"\u2423", " ")

    print(unicode)
    letters_fixed = str(unicode)

    # fastest time I could come up with without hitting 150 WPM limit (BS anti-cheat tbh)
    pyautogui.write(letters_fixed, interval=0.0763)
    print(letters_fixed)

# Multiplayer
'''
# finding string value of element to see when it can start typing
go = driver.find_element_by_xpath('//*[@id="App"]/div/div[1]/div[1]')
# variable to compare it to
compare = "GO!"

# if the statement is not true, loops this until it is
while go.text != compare:
    time.sleep(0.1)

# if the statement is true, loops this until the race finishes
while go.text == compare:
    letters_uni = driver.find_element_by_xpath('//*[@id="App"]/div/div[2]/div/div[2]')
    unicode = letters_uni.text.replace(u"\u2423", " ")

    print(unicode)
    letters_fixed = str(unicode)
    
    # fastest time I could come up with without hitting 150 WPM limit (BS anti-cheat tbh)
    pyautogui.write(letters_fixed, interval=0.0763)
    print(letters_fixed)
'''
