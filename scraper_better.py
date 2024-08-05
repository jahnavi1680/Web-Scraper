# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 20:38:21 2023

@author: jp042
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
chrome_driver_path = "C:/webdrivers/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Replace 'url_of_webpage' with the actual URL of the webpage you want to scrape
url = 'https://topai.tools/browse'
driver.get(url)

# Wait for a specific element to be present before proceeding
try:
    element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
    WebDriverWait(driver, 10).until(element_present)
except Exception as e:
    print("Error:", e)
    driver.quit()

# Replace 5 with the number of times you want to scroll down the page
scroll_times = 250

for _ in range(scroll_times):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(10)

# Now the page should have loaded more content, and you can proceed with scraping.

# Initialize an empty list to store all the tool information
all_tool_info = []

def extract_tool_info(tool_url):
    req = requests.get(tool_url)
    soup = BeautifulSoup(req.content, "html.parser")

    # Find the title
    title_element = soup.find('h1', class_='text-capitalize')
    title = title_element.text.strip() if title_element else None

    # Extract the pricing link 
    small_tag = soup.find('small', class_='text-app pl-5 mx-5 text-app')

# If the small tag is found, proceed to find the link element within it
    if small_tag:
        link_element = small_tag.find('a')
        pricing_page = link_element['href'] if link_element else None
    else:
        pricing_page = None

    # Find the tags
    tags_elements = soup.find_all('span', class_='badge bg-black')
    tags = [tag.text.strip() for tag in tags_elements]

    # Extract the use cases of the tool
    use_cases_elements = soup.find('div', class_='my-4').find_all('li')
    use_cases = [use_case.text.strip() for use_case in use_cases_elements]

    # Find the pricing information
    pricing_element = soup.find('span', class_='badge rounded bg-black text-light')
    pricing = pricing_element.text.strip() if pricing_element else None

    # Find the link to the website
    a_tag = soup.find('div', class_='bg-dark').find('a')
    website= a_tag['href'] if a_tag else None

    tool_info = {
        'title': title,
        'pricing_page': pricing_page,
        'pricing': pricing,
        'website': website,
        'tags': tags,
        'use_cases': use_cases
    }

    return tool_info

tool_boxes = driver.find_elements(By.CSS_SELECTOR, 'div.tool_box')
for tool_box in tool_boxes:
    inner_html = tool_box.get_attribute('innerHTML')
    soup = BeautifulSoup(inner_html, "html.parser")
    anchor_element = soup.select_one('h5 a[href^="/t/"]')
    href_value = anchor_element.get('href')
    tool_url='https://topai.tools'+href_value
    print(href_value)
    tool_info = extract_tool_info(tool_url)
    all_tool_info.append(tool_info)