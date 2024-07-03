from bs4 import BeautifulSoup
import requests
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup

def get_website_html(url):
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8')
            return html_content
    except urllib.error.URLError as e:
        print(f"An error occurred: {e}")

# Example usage
driver = webdriver.Chrome()
url = "https://employees.exact.com/docs/WflRequest.aspx?BCAction=1&ID=%7b03922a77-7f03-4a09-9d49-c826e5807b80%7d"
#html = get_website_html(website_url)
driver.get(url)

# Create a BeautifulSoup object with JavaScript support using 'lxml' parser
# soup = BeautifulSoup(html, 'lxml')
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Find all div elements
heading = soup.find(id ='_Header')
title = soup.find(id ='Description')
