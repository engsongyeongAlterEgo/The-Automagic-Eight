
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
from storage import writeData

def automate_hour_entry(userId, userPwd, proCode, activity):
    # Initialize the WebDriver for Chrome
    writeData([userId, userPwd, "", "", "", ""])
    driver = webdriver.Chrome()

    # Initialize ActionChains
    actions = ActionChains(driver)

    # Open the website
    driver.get("https://start.exactonline.nl/?ReturnUrl=%2fdocs%2fMenuPortal.aspx")

    # Find the LoginForm$UserName element by its ID and fill it in
    username_field = driver.find_element(By.ID, "LoginForm$UserName")
    username_field.send_keys(userId)# put ID

    # Find the button by its ID and click it
    submit_button = driver.find_element(By.ID, "submit_btn")
    submit_button.click()

    # Wait for the password field to be present on the new page
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    
    # Enter password securely using execute_script
    driver.execute_script(f'arguments[0].value = "{userPwd}";', password_field)

    # Find the button by its ID and click it
    submit_button = driver.find_element(By.ID, "next")
    driver.execute_script("arguments[0].click();", submit_button)
    
    # Wait for the "Entries" menu item to be clickable and then click it
    entries_menu_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Entries"))
    )
    driver.execute_script("arguments[0].click();", entries_menu_item)

    # Wait for the "Weekly" link to be clickable and then click it
    weekly_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Entries_Entries_Entries_Weekly"))
    )
    driver.execute_script("arguments[0].click();", weekly_link)

    driver.switch_to.frame("MainWindow")

    driver.execute_script("arguments[0].value = '54';", driver.find_element(By.ID, "mtx_r0_c1_Quantity"))
    driver.execute_script("arguments[0].value = '54';", driver.find_element(By.ID, "mtx_r0_c2_Quantity"))
    driver.execute_script("arguments[0].value = '54';", driver.find_element(By.ID, "mtx_r0_c3_Quantity"))
    driver.execute_script("arguments[0].value = '54';", driver.find_element(By.ID, "mtx_r0_c4_Quantity"))
    driver.execute_script("arguments[0].value = '54';", driver.find_element(By.ID, "mtx_r0_c5_Quantity"))

    actions = ActionChains(driver)

    actions.send_keys(Keys.TAB).perform()

    for char in proCode:
        actions.send_keys(char)

    actions.send_keys(Keys.TAB).perform()

    for char in activity:
        actions.send_keys(char)

    actions.send_keys(Keys.TAB).perform()

    # Assuming driver is your WebDriver instance and project_field_name is the name of your hidden field
    project_field_id = "mtx_r0_c1_Quantity"
    value_to_input = "8"  # The value you want to set

    driver.execute_script(f'document.getElementById("{project_field_id}").value="{value_to_input}";')

    # Assuming driver is your WebDriver instance and project_field_name is the name of your hidden field
    project_field_id = "mtx_r0_c2_Quantity"
    value_to_input = "8"  # The value you want to set

    driver.execute_script(f'document.getElementById("{project_field_id}").value="{value_to_input}";')

    # Assuming driver is your WebDriver instance and project_field_name is the name of your hidden field
    project_field_id = "mtx_r0_c3_Quantity"
    value_to_input = "8"  # The value you want to set

    driver.execute_script(f'document.getElementById("{project_field_id}").value="{value_to_input}";')

    # Assuming driver is your WebDriver instance and project_field_name is the name of your hidden field
    project_field_id = "mtx_r0_c4_Quantity"
    value_to_input = "8"  # The value you want to set

    driver.execute_script(f'document.getElementById("{project_field_id}").value="{value_to_input}";')

    # Assuming driver is your WebDriver instance and project_field_name is the name of your hidden field
    project_field_id = "mtx_r0_c5_Quantity"
    value_to_input = "8"  # The value you want to set

    driver.execute_script(f'document.getElementById("{project_field_id}").value="{value_to_input}";')

    # driver.execute_script('document.getElementById("btnSaveAsSubmitted").click();')
    
    
    input("Press Enter to close the browser...")