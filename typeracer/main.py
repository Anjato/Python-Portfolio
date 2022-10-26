import pyautogui
import cv2
import pytesseract
from pathlib import Path
import os
from time import sleep
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.get('https://play.typeracer.com/')

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

    loginbtn = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//a[@class='promptBtn "
                                                                                         "signIn']")))
    # loginbtn = driver.find_element(By.XPATH, "//a[@class='promptBtn signIn']")

    loginbtn.click()

    usernameTextBox = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//input["
                                                                                                "@name='username']")))
    passwordTextBox = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//input["
                                                                                                "@name='password']")))
    usernameTextBox.send_keys(user)
    passwordTextBox.send_keys(passwd)

    signInButton = driver.find_element(By.XPATH, "//button[@class='gwt-Button']")
    signInButton.click()

    response()


# main function that complete races. must be on the main page for the function to find the begin race button
def main():
    race = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, "//a[@class='gwt-Anchor prompt-button bkgnd-green']")))
    race.click()

    go = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, "//div[@class='gameStatusLabel']")))
    compare = "Go!"

    changeDisplayFormat = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, "//a[@class='gwt-Anchor display-format-trigger']")))

    changeDisplayFormat.click()
    oldStyleOneRadio = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, "//span[@class='gwt-RadioButton OLD_FULLTEXT']/input")))
    oldStyleOneRadio.click()
    changeDisplayFormatX = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, "//div[@class='xButton']")))
    changeDisplayFormatX.click()

    words = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, "//div[@class='nonHideableWords unselectable']/span[2]")))

    print(go.text)
    while go.text != compare:
        sleep(0.1)

    while go.text == compare:
        try:
            textInput = driver.find_element(By.XPATH, "//input[@class='txtInput']")
            punctuation = driver.find_element(By.XPATH, "//div[@class='nonHideableWords unselectable']/span[3]")
            if punctuation.text != '':
                print(words.text + punctuation.text)
                # pyautogui.write(words.text + ',' + ' ', interval=0.01)
                textInput.send_keys(words.text + punctuation.text + ' ')
                sleep(0.16)
            else:
                print(words.text + punctuation.text)
                # pyautogui.write(words.text + ' ', interval=0.01)
                textInput.send_keys(words.text + ' ')
                sleep(0.16)
        except NoSuchElementException:
            print('Unable to find text field for race. Race finished!')
            response()
            pass

    response()


# function to complete the typing speed verification. not currently done due to tesseract not reading images well
def test():
    print('Blank')


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
        sleep(3)
        response()


# function needs some more looking into, tesseract works but struggles to identify the letters due to them being warped
# and having lines strikethrough. only here for testing tesseract and once complete, will be put into test function
def tesseracttest():
    img = cv2.imread('challenge.jpg')

    text = pytesseract.image_to_string(img)
    print(text)


def getres():
    width, height = pyautogui.size()
    modW = width / 1.2
    modH = height / 1.2
    driver.set_window_size(modW, modH)

    login()


getres()
