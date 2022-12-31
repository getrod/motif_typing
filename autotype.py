import pyautogui
import time

words = 'Hello world!'
time.sleep(10)

for c in words:
    pyautogui.write(c)