import requests
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
 
driver = webdriver.Chrome()
url = "https://employees.exact.com/docs/WflRequest.aspx?BCAction=1&ID=%7b03922a77-7f03-4a09-9d49-c826e5807b80%7d"
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

heading = soup.find(id ='_Header')
title = soup.find(id ='Description')
