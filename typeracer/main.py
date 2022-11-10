import pyautogui
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import subprocess as sp
import requests

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get('https://play.typeracer.com/')

wait = WebDriverWait(driver, 10)


# function to log in the user with credentials found in creds.txt (same folder as main.py), going to add encryption
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

    loginbtn = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.promptBtn.signIn')))
    # loginbtn = driver.find_element(By.XPATH, "//a[@class='promptBtn signIn']")

    loginbtn.click()

    usernameTextBox = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".gwt-TextBox[name='username'")))
    passwordTextBox = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "tr:nth-child(2) > td:nth-child(2) "
                                                                              "> table > tbody > tr:nth-child(1) "
                                                                              "> td > input")))
    signInButton = driver.find_element(By.CSS_SELECTOR, ".gwt-Button[type=button]")

    usernameTextBox.send_keys(user)
    passwordTextBox.send_keys(passwd)

    signInButton.click()

    response()


# main function that complete races. must be on the main page for the function to find the begin race button
def main():
    race = wait.until(ec.presence_of_element_located((By.XPATH, "//a[@class='gwt-Anchor prompt-button bkgnd-green']")))
    race.click()

    go = wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class='gameStatusLabel']")))
    compareList = ["Go!", "The race is on! Type the text below:"]

    changeDisplayFormat = wait.until(
        ec.presence_of_element_located((By.XPATH, "//a[@class='gwt-Anchor display-format-trigger']")))

    changeDisplayFormat.click()
    oldStyleOneRadio = wait.until(
        ec.presence_of_element_located((By.XPATH, "//span[@class='gwt-RadioButton OLD_FULLTEXT']/input")))
    oldStyleOneRadio.click()
    changeDisplayFormatX = wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class='xButton']")))
    changeDisplayFormatX.click()

    words = wait.until(
        ec.presence_of_element_located((By.XPATH, "//div[@class='nonHideableWords unselectable']/span[2]")))

    print(go.text)
    while go.text != compareList[1] and go.text != compareList[0]:
        print(go.text)
        sleep(0.1)

    while go.text == compareList[1] or go.text == compareList[0]:
        try:
            textInput = driver.find_element(By.XPATH, "//input[@class='txtInput']")
            punctuation = driver.find_element(By.XPATH, "//div[@class='nonHideableWords unselectable']/span[3]")
            if punctuation.text != '':
                print(words.text + punctuation.text)
                # pyautogui.write(words.text + ',' + ' ', interval=0.01)
                textInput.send_keys(words.text + punctuation.text + ' ')
                sleep(0.15)
            else:
                print(words.text + punctuation.text)
                # pyautogui.write(words.text + ' ', interval=0.01)
                textInput.send_keys(words.text + ' ')
                sleep(0.15)
        except NoSuchElementException:
            print('Unable to find text field for race. Race finished!')
            response()
            pass

    response()


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
def test():

    # vpn()

    begintest = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".gwt-Button.gwt-Button")))
    begintest.click()

    captchaWait = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".challengeImg")))
    challengeTextBox = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".challengeTextArea")))
    submitButton = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".gwt-Button.gwt-Button")))

    captcha = driver.find_element(By.CSS_SELECTOR, ".challengeImg")
    captcha.screenshot("challenge.png")

    challenge = "challenge.png"

    challengeOCRText = ocr_space_file(filename=challenge)
    challengeText = challengeOCRText['ParsedResults'][0]['ParsedText']

    challengeTextBox.send_keys(challengeText)
    submitButton.click()

    response()


def checkvpn():
    os.chdir('C:/Program Files/Private Internet Access/')
    piactl = 'piactl.exe'
    connectionState = sp.Popen([piactl, 'get', 'connectionstate'], stdout=sp.PIPE).communicate()[0]
    return connectionState.decode().strip()


def vpn():
    originaldir = os.getcwd()
    os.chdir('C:/Program Files/Private Internet Access/')
    piactl = 'piactl.exe'
    sp.run([piactl, 'disconnect'])
    sp.run([piactl, 'connect'])

    while True:
        connectionState = checkvpn()
        if connectionState != "Connected":
            checkvpn()
            print(connectionState)
            sleep(1)
        else:
            print("VPN Connected! Continuing test...")
            break

    os.chdir(originaldir)


def ocr_space_file(filename, overlay=False, api_key='K8561183428895', language='eng', OCREngine=5, scale=True):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :param OCREngine: Optional between 1, 2, 3, or 5
                    1 = fastest, 2 = better with single numbers/characters
                    3 = expands on language support but slower, 5 = seems most accurate
                    Defaults to 1.
    :param scale: API does minor internal upscaling which can significantly improve accuracy
                    Defaults to False.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine': OCREngine,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.json()


def getres():
    width, height = pyautogui.size()
    modW = width / 1.2
    modH = height / 1.2
    driver.set_window_size(modW, modH)

    login()


getres()
