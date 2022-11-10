import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


options = webdriver.FirefoxOptions()

# If Firefox is not in default path, it is necessary to define binary location
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

driver_path = os.path.join(os.path.dirname(__file__), "geckodriver.exe")
driver = webdriver.Firefox(executable_path=driver_path, options=options)

url = "https://ru.wikipedia.org"

try:
    # Find first H2 and print its color
    driver.get(url=url)
    header2 = driver.find_element(by=By.TAG_NAME, value='h2')
    color = header2.value_of_css_property('color')
    print(color)

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()



