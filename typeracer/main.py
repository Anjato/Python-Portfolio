import time
import pyautogui
import cv2
import pytesseract
from pathlib import Path
import os
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.get('https://play.typeracer.com/')

# give page time to load the sign in javascript in top right
time.sleep(2)


# function to login the user with credentials found in creds.txt (same folder as main.py), going to add encryption
# support to not store password in plaintext
def login():
    file = "creds.txt"

    if not os.path.exists(file):
        user = str(input("Please enter username:"))
        passwd = str(input("Please enter password:"))
        f = open(file, "w")
        f.writelines([user, "\n", passwd])
        f.close()
    elif os.stat(file).st_size == 0:
        user = str(input("Please enter username:"))
        passwd = str(input("Please enter password:"))
        f = open(file, "w")
        f.writelines([user, "\n", passwd])
        f.close()
    else:
        f = open(file, "r")
        read = f.readlines()
        user = read[0]
        passwd = read[1]
        f.close()

############# ADD FOCUS WINDOW HERE #######################

    # sign in button in top right
    loginbtn = driver.find_element(By.XPATH, "//a[@class='promptBtn signIn']")
    loginbtn.click()
    # give time for form to pop up
    time.sleep(1)
    # replaces new line to prevent hitting enter after entering username
    pyautogui.write(user.replace("\n", ""), interval=0.01)
    # hits tab to goto password field
    pyautogui.press('tab')
    pyautogui.write(passwd, interval=0.01)
    pyautogui.press('enter')

    # give time for sign in form to disappear
    time.sleep(1)

    response()


# main function that complete races. must be on the main page for the function to find the begin race button
def main():
    race = driver.find_element(By.XPATH, "//a[@class='gwt-Anchor prompt-button bkgnd-green']")
    race.click()

    # gives time for xpath to load and be found while running the loop statement(s)
    time.sleep(4)

    go = driver.find_element(By.XPATH, "//div[@class='gameStatusLabel']")
    compare = "Go!"

    changeDisplayFormat = driver.find_element(By.XPATH, "//a[@class='gwt-Anchor display-format-trigger']")

    changeDisplayFormat.click()
    time.sleep(0.5)
    oldStyleOneRadio = driver.find_element(By.XPATH, "//span[@class='gwt-RadioButton OLD_FULLTEXT']/input")
    oldStyleOneRadio.click()
    time.sleep(0.5)
    changeDisplayFormatX = driver.find_element(By.XPATH, "//div[@class='xButton']")
    changeDisplayFormatX.click()
    time.sleep(1)

    words = driver.find_element(By.XPATH, "//div[@class='nonHideableWords unselectable']/span[2]")
    comma = driver.find_element(By.XPATH, "//div[@class='nonHideableWords unselectable']/span[3]")

    print(go.text)
    while go.text != compare:
        time.sleep(0.1)

    while go.text == compare:
        comma = driver.find_element(By.XPATH, "//div[@class='nonHideableWords unselectable']/span[3]")
        if comma.text == ',':
            print(words.text + comma.text)
            pyautogui.write(words.text + ',' + ' ', interval=0.05)
        else:
            print(words.text + comma.text)
            pyautogui.write(words.text + ' ', interval=0.05)

    # if go.text == compare:
    #     pyautogui.write(firstWord.text + ' ', interval=0.05)
    #     print(firstWord.text)
    #     while go.text == compare:
    #         pyautogui.write(otherWords.text, interval=0.05)
    #         print(otherWords.text)

    response()


# function to complete the typing speed verification. not currently done due to tesseract not reading images well
def test():
    begintest = driver.find_element_by_xpath('/html/body/div[16]/div/div/div[2]/div/div/table/tbody/tr[4]/td/button' or
                                             '/html/body/div[10]/div/div/div[2]/div/div/table/tbody/tr[4]/td/button')
    begintest.click()

    image = driver.find_element_by_xpath('/html/body/div[16]/div/div/div[2]/div/div/table/tbody/tr[3]/td/img')

    pyautogui.write(captcha, interval=0.07)


# function to take user input to either start a race (must be on main page) or complete a test to verify typing speed
def response():

    choice = int(input("Are you starting a race (1) or a test (2)?"))

    if choice == 1:
        main()
    elif choice == 2:
        test()
        # just in case :)
    elif choice != 1 or 2:
        print("Invalid argument, please try again.")
        time.sleep(3)
        response()


# function needs some more looking into, tesseract works but struggles to identify the letters due to them being warped
# and having lines strikethrough. only here for testing tesseract and once complete, will be put into test function
def tesseracttest():
    img = cv2.imread('challenge.jpg')

    text = pytesseract.image_to_string(img)
    print(text)


def getRes():
    width, height = pyautogui.size()
    global modW
    global modH
    modW = width / 1.2
    modH = height / 1.2
    driver.set_window_size(modW, modH)

    login()


getRes()
