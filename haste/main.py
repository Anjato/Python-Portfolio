import pyautogui
import time

time.sleep(5)

f = open("lol.txt", 'r')

for word in f:
    pyautogui.typewrite(word, 0.0)
