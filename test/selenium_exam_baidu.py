#!/usr/bin/env python3
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup

#driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")

assert "百度" in driver.title
query_text = "WebRTC"
input_box = driver.find_element(By.ID, "kw")
input_box.clear()
input_box.send_keys(query_text)

submit_btn = driver.find_element(By.ID, "su")
submit_btn.click()

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
try:
    WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions) \
                .until(expected_conditions.title_contains(query_text))
except:
    pass

# Using beautifulsop to parse search results
bsobj = BeautifulSoup(driver.page_source, features="html.parser")

# Get search results queue
search_results = bsobj.find_all('div', {'class': 'c-container'})
print("result count: {}".format(len(search_results)))
# For each search result
for search_item in search_results:
    if search_item.h3 and search_item.h3.a:
        # Get all text for the title of each search result
        text = search_item.h3.a.get_text(strip=True)
        print(text)

driver.close()
