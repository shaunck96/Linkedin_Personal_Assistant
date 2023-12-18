from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

class ActivityScraper():
    def __init__(self, email = "shaunchackoofficial@gmail.com", password = "Chacko1234#", url="https://www.linkedin.com/in/sanjana-athreya/recent-activity/all/"):
        self.email = email
        self.password = password
        self.url = url
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome()

    def scraper_trigger(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=self.chrome_options)#,executable_path="chromedriver.exe")
        self.linkedin_login()

    def linkedin_login(self):
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
        self.activity_scraper()

    def activity_scraper(self):
        src = self.driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        posts = soup.find_all("div", {'class': 'update-components-text relative update-components-update-v2__commentary'})
        a_tags = soup.find_all('a', class_='app-aware-link update-components-actor__sub-description-link')
        date_of_post = [tag.get('aria-label') for tag in a_tags]

        like_counts = []
        reactions_elements = soup.find_all('li', class_='social-details-social-counts__reactions')
        for reactions_element in reactions_elements:
            like_count = reactions_element.find('button').text.strip()
            like_counts.append(like_count)

        post_info_df = pd.DataFrame(columns=['post_info', 'date_of_post', 'like_count'])

        index = 0
        for post in posts:
            post_info_df.at[index, 'post_info'] = post.text
            index+=1

        index=0    
        for date in date_of_post:    
            post_info_df.at[index, 'date_of_post'] = date
            
        index=0     
        for like_count in like_counts: 
            post_info_df.at[index, 'like_count'] = like_count
            index += 1

        post_info_df.to_csv(r'post_details.csv')
        self.driver.quit()

ActivityScraper(url="https://www.linkedin.com/in/sanjana-athreya/recent-activity/all/").scraper_trigger()
