from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get("https://www.thatquiz.org/tq-1/math/arithmetic/")
table_equation = browser.find_element_by_xpath("//table[@class='bZQ q9av']/tbody/tr/td[2]")


# table_settings = browser.find_element_by_xpath("//table[@class='bZQ q9av']/tbody/tr/td[1]")
# if True:
#     print(table_settings.text)
# maybe able to manipulate the settings automatically when opening the web page? doubtful though

while True:
    answer = str(int(eval(table_equation.text[-14:-7])))

    print(table_equation.text[-14:-7])
    print(answer)

    pyautogui.write(answer, _pause=False)
    pyautogui.press("enter")
