import pyautogui
import random
import pyscreenshot
from PIL import Image
import pytesseract
import time
from pynput import mouse
import cv2
import numpy as np

def detect_click():
    def on_click(x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            print(f"Left button clicked at ({x}, {y})")
            # Stop listener
            return False

    # Collect events until released
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def defeat_them():

    user_again = 'y'

    while user_again == 'y':
        print('click now')
        if not detect_click():
            x_and_y_start = pyautogui.position()

        if not detect_click():
            x_and_y_end = pyautogui.position()
        
        screenshot = pyscreenshot.grab(bbox=[x_and_y_start[0], x_and_y_start[1], x_and_y_end[0], x_and_y_end[1]])
        screenshot_path = 'screenshot.png'
        screenshot.save(screenshot_path)
        
        img = cv2.imread(screenshot_path)
        (h, w) = img.shape[:2]
        img = cv2.resize(img, (w*3, h*3))

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding
        binary_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))

        # Detect horizontal lines in the binary image
        detected_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

        # Subtract the detected lines from the binary image
        binary_image_no_lines = cv2.bitwise_and(binary_image, cv2.bitwise_not(detected_lines))

        text = pytesseract.image_to_string(binary_image_no_lines, config='--psm 6 --oem 3 -c tessedit_char_blacklist=|')

        modified_string = text[0].upper() + text[1:]
        modified_string = ' '.join(modified_string.splitlines())
        print(modified_string)
        
        time.sleep(1.5)

        pyautogui.keyDown('shift')
        pyautogui.write(modified_string[0])
        pyautogui.keyUp('shift')

        pyautogui.write(modified_string[1:], interval=random.uniform(0.025, 0.09))

        '''
        count = 0
        for texty in modified_string:
            if count == 0:
                pyautogui.keyDown('shift')
                pyautogui.write(texty)
                pyautogui.keyUp('shift')
                count+=1
            else: 
                pyautogui.write(texty)
        '''
    
        user_again = input('again? (y for yes): ')

if __name__ == "__main__":
    defeat_them()