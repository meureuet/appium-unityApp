import os, sys
import datetime
from time import sleep
import unittest
import cv2
import numpy as np

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


class CustomTests(unittest.TestCase):

    def setUp(self):
        caps = {}
        caps["platformName"] = "Android"
        caps["appium:platformVersion"] = "11"
        caps["appium:deviceName"] = "Pixel 3 API 30"
        caps["appium:app"] = "D:\\apks\\CalculatorTheGame_v1.5.apk"
        caps["appium:automationName"] = "Appium"
        caps["appium:newCommandTimeout"] = 300
        caps["appium:appPackage"] = "com.sm.calculateme"
        caps["appium:appActivity"] = "com.unity3d.player.UnityPlayerActivity"
        caps["appium:ensureWebviewsHavePages"] = True
        caps["appium:nativeWebScreenshot"] = True
        caps["appium:connectHardwareKeyboard"] = True

        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
        print("set up")

       
    def test_step(self):
        driver = self.driver
        sleep(20)
        
        image_x, image_y = self.detectImage(
            "D:\\Appium Project\\rule explain\\Button_Hi.png")
        
        # Hi 버튼 터치
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(image_x, image_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print("touch hi button")
        sleep(5)

    
    # 외곽선 표시
    def auto_canny(self, image, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(image)

        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)

        return edged
    
    # 이미지 좌표 반환
    def detectImage(self, templateImagePath):
        shotName = '{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())

        directory = 'D:\\Appium Project\\rule explain\\'
        screenshotImgPath = directory + shotName + '.png'
        self.driver.save_screenshot(screenshotImgPath)
        sleep(2)

        # 원본 이미지
        screenImage = cv2.imread(screenshotImgPath, 0)
        screenCann = self.auto_canny(screenImage)

        # 찾으려는 이미지
        templateImage = cv2.imread(templateImagePath, 0)
        templateCann = self.auto_canny(templateImage)
        w, h = templateCann.shape[::-1]

        # 원본에서 template 찾기
        res = cv2.matchTemplate(screenCann, templateCann, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = max_loc
        x = top_left[0] + int(w/2)
        y = top_left[1] + int(h/2)

        return x, y

    def tearDown(self):
        self.driver.quit()
        print("tear down")
        
if __name__ == "__main__":
    unittest.main()






