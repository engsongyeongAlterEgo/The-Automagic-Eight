
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver for Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
driver.get("https://start.exactonline.nl/?ReturnUrl=%2fdocs%2fMenuPortal.aspx")

# Find the LoginForm$UserName element by its ID and fill it in
username_field = driver.find_element(By.ID, "LoginForm$UserName")
username_field.send_keys("")# put ID

# Find the button by its ID and click it
submit_button = driver.find_element(By.ID, "submit_btn")
submit_button.click()


# Wait for the password field to be present on the new page
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "LoginForm_Password"))
)

password_field.send_keys("")# put password

# Find the button by its ID and click it
submit_button = driver.find_element(By.ID, "LoginForm_btnSave")
submit_button.click()
input("Press Enter to close the browser...")