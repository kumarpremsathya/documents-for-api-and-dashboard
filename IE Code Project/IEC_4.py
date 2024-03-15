import sys
import os
import cv2
import easyocr
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request

# Function to handle captcha processing
def process_captcha(browser):
    # Get the captcha image element
    captcha_image = browser.find_element(By.XPATH, '//*[@id="captcha"]')


    # Save the captcha image locally
    with open('captcha.png', 'wb') as file:
        file.write(captcha_image.screenshot_as_png)

    # Redirect stdout to a file for progress output
    with open('output.log', 'w', encoding='utf-8') as f:
        sys.stdout = f
        
        # Preprocess the captcha image
        captcha_image = cv2.imread('captcha.png')
        gray_image = cv2.cvtColor(captcha_image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        blurred_image = cv2.GaussianBlur(binary_image, (3, 3), 0)
        cv2.imwrite('preprocessed_captcha.png', blurred_image)
        
        # Load the reader
        reader = easyocr.Reader(['en'])
        result = reader.readtext('captcha.png', detail=0)
        captcha_text = ''.join(result)
        print("captcha_text", captcha_text)

    return captcha_text

# Disable printing progress information during download
def no_progress(blocknum, bs, size):
    pass

# Redirect stdout to a file
sys.stdout = open(os.devnull, 'w')

chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=chrome_options)
browser.get('https://www.dgft.gov.in/CP/?opt=view-any-ice')

try:
    next_xpath = browser.find_element(By.XPATH, '//*[@id="mainSectionWrap"]/div[3]/div/div[2]/div[1]')
    next_xpath.click()
    time.sleep(2)

    iec_input = browser.find_element(By.XPATH, '//*[@id="iecNo"]')
    entity_input = browser.find_element(By.XPATH, '//*[@id="entity"]')
    iec_input.send_keys("0388031964")
    time.sleep(3)
    entity_input.send_keys("TATA CONSULTANCY SERVICES LIMITED")
    time.sleep(3)

    while True:
        # Process the captcha
        captcha_text = process_captcha(browser)

        # Input the recognized captcha text
        captcha_input = browser.find_element(By.XPATH, '//*[@id="txt_Captcha"]')
        captcha_input.send_keys(captcha_text)

        time.sleep(3)

        # Click on the element with XPath '//*[@id="viewIEC1"]'
        view_button = browser.find_element(By.XPATH, '//*[@id="viewIEC1"]')
        view_button.click()
        time.sleep(5)

        # Check if the "Please enter valid captcha code" message is displayed
        error_message = browser.find_elements(By.XPATH, '//*[@id="incCaptcha"]')
        if not error_message:
            # Find the elements matching the XPath
            ice_details = browser.find_elements(By.XPATH, '//*[@id="iecdetails"]')

            # Iterate over the elements and print their outer HTML
            for element in ice_details:
                print(element.get_attribute('outerHTML'))
            
            break  # Break the loop if no error message is found             

except Exception as e:
    traceback.print_exc()
    print("wrong xpath", e)

finally:
    browser.quit()

    # Restore stdout
    sys.stdout = sys.__stdout__
