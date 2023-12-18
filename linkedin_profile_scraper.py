from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

class LinkedinProfileScrapper:
  def __init__(self, email = "shaunchackoofficial@gmail.com", password = "Chacko1234#", url="https://www.linkedin.com/in/sanjana-athreya/"):
    self.email = email
    self.password = password
    self.chrome_options = webdriver.ChromeOptions()
    self.url = url
    self.driver = webdriver.Chrome()

  def scraper_trigger(self):
    self.chrome_options.add_argument("--start-maximized")
    self.chrome_options.add_argument("--disable-gpu")
    self.chrome_options.add_argument("--no-sandbox")
    self.chrome_options.add_argument("--disable-notifications")
    self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    self.chrome_options.add_experimental_option('useAutomationExtension', False)
    self.driver = webdriver.Chrome(options=self.chrome_options)
    self.login()

  def login(self):
    self.driver.maximize_window()
    self.driver.get('https://www.linkedin.com/login')
    time.sleep(10)
    self.driver.find_element(By.ID, 'username').send_keys(self.email)
    self.driver.find_element(By.ID, 'password').send_keys(self.password)
    self.driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
    time.sleep(10)
    self.driver.get(self.url)
    time.sleep(40)
    self.scroll_down()

  def scroll_down(self):
    SCROLL_PAUSE_TIME = 2
    last_height = self.driver.execute_script("return document.body.scrollHeight")
    scroll_limit = 10
    count = 0
    while True and count < scroll_limit:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        count += 1
    self.get_data()

  def get_data(self):
    src = self.driver.page_source
    soup = BeautifulSoup(src, 'html.parser')  
    img_tag = soup.find('img', {'class': 'global-nav__me-photo'})
    name = img_tag['alt'] if img_tag else 'Name not found'
    location_body = soup.find("div", {'class': 'wrksnmhvklIDWaLBcdIePlLksyeass mt2'})
    location = location_body.find("span", {"class": 'text-body-small inline t-black--light break-words'})
    titles_divs = soup.find_all("div", {'class': 'display-flex align-items-center mr1 t-bold'})
    titles_divs_with_promo = soup.find_all("div", {'class': 'display-flex align-items-center mr1 hoverable-link-text t-bold'})
    job_description = soup.find_all("div", {'class': 'pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center'})
    titles = []
    for div in titles_divs:
        span = div.find('span', {'aria-hidden': 'true'})
        if span:
            titles.append(span.text.strip())
    for div in titles_divs_with_promo:
        span = div.find('span', {'aria-hidden': 'true'})
        if span:
            titles.append(span.text.strip())
    descriptions = []
    for div in job_description:
        span = div.find('span', {'aria-hidden': 'true'})
        if span:
            descriptions.append(span.text.strip())
    output = {}
    output['Descriptions'] = descriptions
    output['Titles'] = titles
    output['Name'] = name
    output['Location'] = location
    
    with open("profile_data.json", "w") as json_file:
        json_file.write(json.dumps(output))
    self.driver.quit()

LinkedinProfileScrapper(url = "https://www.linkedin.com/in/loren-hudspeth-01575178/").scraper_trigger()
