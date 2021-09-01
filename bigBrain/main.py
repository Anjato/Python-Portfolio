from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get("https://www.thatquiz.org/tq-1/?-j1gh8f-l34-mpnv600-n35-p0")

# grabs cell value in table where the equation is found
table_equation = browser.find_element_by_xpath("//table[@class='g6cd']/tbody/tr/td[2]/table/tbody/tr/td[1]")


while True:
    # fixes stale element reference error (somehow, no clue why tbh)
    table_equation = browser.find_element_by_xpath("//table[@class='g6cd']/tbody/tr/td[2]/table/tbody/tr/td[1]")

    t = table_equation.text.replace(u"\u00D7", "*").replace(u"\u00F7", "/").replace(u"\u2013", "-")

    print(t)
    answer = str(int(eval(t)))
    print(answer)

    pyautogui.write(answer, _pause=False)
    pyautogui.press("enter")
