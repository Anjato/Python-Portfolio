from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get("https://www.thatquiz.org/tq-1/?-j1gh8f-l34-mpnv600-n35-p0")

while True:

    # grabs cell value in table where the equation is found
    # originally had as a global but it would throw a stale element reference error, idk why
    table_equation = browser.find_element_by_xpath("//table[@class='g6cd']/tbody/tr/td[2]/table/tbody/tr/td[1]")

    # replaces unicode letters with operators that python understands
    t = table_equation.text.replace(u"\u00D7", "*").replace(u"\u00F7", "/").replace(u"\u2013", "-")

    print(t)
    answer = str(int(eval(t)))
    print(answer, "\n")

    pyautogui.write(answer, _pause=False)
    pyautogui.press("enter")
