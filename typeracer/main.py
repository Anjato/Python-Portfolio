import time
import pyautogui
import cv2
import pytesseract
import tkinter as tk
from cryptography.fernet import Fernet
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def getRes():
    width, height = pyautogui.size()
    global modW
    global modH
    modW = width / 1.2
    modH = height / 1.2


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://play.typeracer.com/')
# driver.maximize_window()
getRes()
driver.set_window_size(modW, modH)

# give page time to load the sign in javascript in top right
time.sleep(2)


# function to login the user with credentials found in creds.txt (same folder as main.py), going to add encryption
# support to not store password in plaintext
def login():
    # file with login details
    f = open("creds.txt", "r")
    lines = f.readlines()
    username = lines[0]
    password = lines[1]
    f.close()

    # sign in button in top right
    loginbtn = driver.find_element_by_xpath('//*[@id="userInfo"]/div/div[2]/div[1]/div[2]/a[2]')
    loginbtn.click()
    # give time for form to pop up
    time.sleep(1)
    # replaces new line to prevent hitting enter after entering username
    pyautogui.write(username.replace("\n", ""), interval=0.01)
    # hits tab to goto password field
    pyautogui.press('tab')
    pyautogui.write(password, interval=0.01)
    pyautogui.press('enter')

    # give time for sign in form to disappear
    time.sleep(1)

    response()


# main function that complete races. must be on the main page for the function to find the begin race button
def main():
    race = driver.find_element_by_xpath('//*[@id="gwt-uid-1"]/a')
    race.click()

    # gives time for xpath to load and be found while running the loop statement(s)
    time.sleep(4)

    go = driver.find_element_by_class_name('lightLabel')
    compare = "Go!"

    letters = driver.find_element_by_xpath('//*[@id="gwt-uid-21"]/table/tbody/tr[2]/td/table/tbody/tr['
                                           '1]/td/table/tbody/tr[1]/td/div/div' or
                                           '//*[@id="gwt-uid-25"]/table/tbody/tr[2]/td/table/tbody/tr['
                                           '1]/td/table/tbody/tr[1]/td/div/div' or
                                           '//*[@id="gwt-uid-29"]/table/tbody/tr[2]/td/table/tbody/tr['
                                           '1]/td/table/tbody/tr[1]/td')
    while go.text != compare:
        time.sleep(0.1)
        print(go.text)

    while go.text == compare:
        pyautogui.write(letters.text, interval=0.05)
        print(letters.text)

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
