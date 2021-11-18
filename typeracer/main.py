import time
import pyautogui
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://play.typeracer.com/')
driver.maximize_window()

time.sleep(2)


def login():

    f = open("creds.txt", "r")
    lines = f.readlines()
    username = lines[0]
    password = lines[1]
    f.close()

    loginbtn = driver.find_element_by_xpath('//*[@id="userInfo"]/div/div[2]/div[1]/div[2]/a[2]')
    loginbtn.click()
    time.sleep(1)
    # replaces new line to prevent hitting enter after entering username
    pyautogui.write(username.replace("\n", ""), interval=0.01)
    pyautogui.press('tab')
    pyautogui.write(password, interval=0.01)
    pyautogui.press('enter')

    time.sleep(2)

    response()


def main():
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
        letters = driver.find_element_by_xpath('//*[@id="gwt-uid-21"]/table/tbody/tr[2]/td/table/tbody/tr['
                                               '1]/td/table/tbody/tr[1]/td/div/div')

        pyautogui.write(letters.text, interval=0.05)
        print(letters.text)

        response()


def test():
    begintest = driver.find_element_by_xpath('/html/body/div[16]/div/div/div[2]/div/div/table/tbody/tr[4]/td/button')
    begintest.click()

    image = driver.find_element_by_xpath('/html/body/div[16]/div/div/div[2]/div/div/table/tbody/tr[3]/td/img')

    pyautogui.write(captcha, interval=0.07)


def response():
    choice = int(input("Are you starting a race (1) or a test (2)?"))

    if choice == 1:
        main()
    elif choice == 2:
        test()
    elif choice != 1 or 2:
        print("Invalid argument, please try again.")
        time.sleep(3)
        response()


login()
