from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver (you need to specify the path to your webdriver executable)
driver = webdriver.Chrome()

# Open LinkedIn website
driver.get("https://www.linkedin.com/")

# Log in to your LinkedIn account (Replace 'your_email' and 'your_password' with your credentials)
email_input = driver.find_element(By.ID, "session_key")
password_input = driver.find_element(By.ID, "session_password")

time.sleep(10)

email_input.send_keys("shaunchackoofficial@gmail.com")
time.sleep(10)
password_input.send_keys("Chacko1234#")
password_input.send_keys(Keys.RETURN)

time.sleep(10)

search_field = driver.find_element(By.XPATH, '//*[@id="ember16"]/input')

# Task 2.2: Input the search query to the search bar
search_query = "data scientist microsoft"
search_field.send_keys(search_query)

# Task 2.3: Search
search_field.send_keys(Keys.RETURN)

# Click on the "People" filter
people_filter = driver.find_element(By.XPATH, "//button[@aria-label='People']")
people_filter.click()

# Click on the "Current company" filter
current_company_filter = driver.find_element(By.XPATH, "//button[@aria-label='Current company']")
current_company_filter.click()

# Close the browser when done
driver.quit()
