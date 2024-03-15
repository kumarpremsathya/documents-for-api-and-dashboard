# import sys
# import os
# import cv2
# import easyocr
# import traceback
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import urllib.request

# # Disable printing progress information during download
# def no_progress(blocknum, bs, size):
#     pass

# # Redirect stdout to a file
# sys.stdout = open(os.devnull, 'w')

# chrome_options = webdriver.ChromeOptions()
# browser = webdriver.Chrome(options=chrome_options)
# browser.get('https://old.icegate.gov.in/EnqMod/')

# try:
#     # next_xpath = browser.find_element(By.XPATH, '//*[@id="mainSectionWrap"]/div[3]/div/div[2]/div[1]')
#     # next_xpath.click()
#     # time.sleep(2)

#     iec_input = browser.find_element(By.XPATH, '//*[@id="searchIECode"]')
    
#     iec_input.send_keys("0388066415")
#     time.sleep(3)
    

#     # Get the captcha image element
#     captcha_image = browser.find_element(By.XPATH, '//*[@id="capimg"]')

#     # Save the captcha image locally
#     with open('captcha.png', 'wb') as file:
#         file.write(captcha_image.screenshot_as_png)

#     # Redirect stdout to a file for progress output
#     with open('output.log', 'w', encoding='utf-8') as f:
#         sys.stdout = f
#         reader = easyocr.Reader(['en'])
#         sys.stdout = sys.__stdout__
   
#     # Load the reader
#     reader = easyocr.Reader(['en'])
#     result = reader.readtext('captcha.png', detail=0)
#     captcha_text = ''.join(result)
#     print("captcha_text", captcha_text)

#     time.sleep(5)

#     # Input the recognized captcha text
#     captcha_input = browser.find_element(By.XPATH, '//*[@id="captchaResp"]')
#     captcha_input.send_keys(captcha_text)

#     time.sleep(3)
    

#     # Click on the element with XPath '//*[@id="viewIEC1"]'
#     view_button = browser.find_element(By.XPATH, '//*[@id="pagetable"]/tbody/tr[4]/td[3]/dl/dd/a')
#     view_button.click()
#     time.sleep(15)

# except Exception as e:
#     traceback.print_exc()
#     print("wrong xpath", e)

# finally:
#     browser.quit()

#     # Restore stdout
#     sys.stdout = sys.__stdout__


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
    captcha_image = browser.find_element(By.XPATH, '//*[@id="capimg"]')

    # Save the captcha image locally
    with open('captcha.png', 'wb') as file:
        file.write(captcha_image.screenshot_as_png)

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
browser.get('https://old.icegate.gov.in/EnqMod/')

try:
    
    while True:
        
        iec_input = browser.find_element(By.XPATH, '//*[@id="searchIECode"]')    
        iec_input.send_keys("0388066415")
        time.sleep(3)
         
        # Process the captcha
        captcha_text = process_captcha(browser)

        # Input the recognized captcha text
        captcha_input = browser.find_element(By.XPATH, '//*[@id="captchaResp"]')
        captcha_input.send_keys(captcha_text)

        time.sleep(3)

        # Click on the element with XPath '//*[@id="pagetable"]/tbody/tr[4]/td[3]/dl/dd/a'
        view_button = browser.find_element(By.XPATH, '//*[@id="pagetable"]/tbody/tr[4]/td[3]/dl/dd/a')
        view_button.click()
        time.sleep(3)

        # Check if the "Invalid Code! Please try again!" message is displayed
        error_message = browser.find_elements(By.XPATH, '//*[@id="pagetable"]/tbody/tr[4]/td[3]/dl/dt[5]/ul/li/span')
        if not error_message:
            break  # Break the loop if no error message is found

except Exception as e:
    traceback.print_exc()
    print("wrong xpath", e)

finally:
    browser.quit()

    # Restore stdout
    sys.stdout = sys.__stdout__
