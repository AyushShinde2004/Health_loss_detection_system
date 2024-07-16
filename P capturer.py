import cv2
import easyocr
import time
import pyautogui
import numpy as np

def capture_health_area(region):# is current health/ current frame 
    screenshot=pyautogui.screenshot(region=region)
    screenshot_np=np.array(screenshot)
    screenshot_np=cv2.cvtColor(screenshot_np,cv2.COLOR_RGB2BGR)
    return screenshot_np #This whole fun retuning ss with numpy arry and in BGR

def read_health_value(image,reader):# this fun recevies image from capture_health_region and read the text and print
    result = reader.readtext(image)
    print(f"OCR Result: {result}")
    if result:
        try:
            health_value_text= result[0][1]
            print(f"Detected Text: {health_value_text}")
            health_value=int(health_value_text)
            return health_value
        except (ValueError,IndexError):
            pass
        return None
    
reader=easyocr.Reader(['en'],gpu=True)

health_bar_region=(1993,414,200,220)

previous_health= None

try:
    while True:
        health_image = capture_health_area(health_bar_region) #health_image is frame from capture_health_region
        cv2.imshow('Health Bar Region', health_image)
        current_health = read_health_value(health_image,reader) #the health image as text is stored in current_health
        if current_health is None:
            if previous_health is not None and current_health < previous_health:
             print(f"Health loss detected{previous_health}{current_health}")
             previous_health=current_health
        time.sleep(1)

        if cv2.waitKey(1)&0xFF ==ord('q'):
            break
except KeyboardInterrupt:
    print("user interruption")     

cv2.destroyAllWindows 

