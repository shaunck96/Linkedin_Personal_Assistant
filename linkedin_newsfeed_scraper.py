from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

class NewsFeedScraper():
    def __init__(self, email="shaunchackoofficial@gmail.com", password="Chacko1234#"):
        self.email = email
        self.password = password
        self.url = "https://www.linkedin.com/feed/"
        self.chrome_options = webdriver.ChromeOptions()
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
        self.linkedin_login()
        
    def linkedin_login(self):    
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(10)

        self.driver.find_element(By.ID, 'username').send_keys(self.email)
        self.driver.find_element(By.ID, 'password').send_keys(self.password)
        self.driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
        time.sleep(10)
        
        self.newsfeed_scraper()


    def newsfeed_scraper(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        SCROLL_PAUSE_TIME = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_limit = 4
        count = 0

        while True and count < scroll_limit:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            count += 1

        src = self.driver.page_source
        soup = BeautifulSoup(src, 'html.parser')  
        posts = soup.find_all("div", {'class': 'update-components-text relative update-components-update-v2__commentary'})
        post_list = []
        for post in posts:
            print(post.text)
            post_list.append(post.text)
        output = {}
        output['Newsfeed_posts'] = post_list

        with open("newsfeed.json", "w") as json_file:
            json.dump(output, json_file)

        self.driver.quit()

NewsFeedScraper(email="shaunchackoofficial@gmail.com", password="#").scraper_trigger()
