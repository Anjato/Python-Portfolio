import pyautogui
from time import sleep
import os

clear = lambda: os.system('cls')

file_name = input('File name:')
file_handle = open(file_name)

print("Starting in 5 seconds...")
sleep(1)
clear()
print("Starting in 4 seconds...")
sleep(1)
clear()
print("Starting in 3 seconds...")
sleep(1)
clear()
print("Starting in 2 seconds...")
sleep(1)
clear()
print("Starting in 1 seconds...")
sleep(1)
clear()
print("Starting! :)")


for word in file_handle:
    pyautogui.typewrite(word, 0.0)
