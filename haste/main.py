import pyautogui
import time

file_name = input('File name:')
file_handle = open(file_name)

time.sleep(5)

for word in file_handle:
    pyautogui.typewrite(word, 0.0)
