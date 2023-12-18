from linkedin_activity_scraper import ActivityScraper
from linkedin_job_scraper import JobScraper
from linkedin_newsfeed_scraper import NewsFeedScraper
from linkedin_profile_scraper import LinkedinProfileScrapper

email = input("Enter Linkedin Login email: ")
password = input("Enter Linkedin Login password: ")

NewsFeedScraper(email=email, password=password).scraper_trigger()

profile_to_be_scraped = input("Enter Profile Information to be scraped")
LinkedinProfileScrapper(url = profile_to_be_scraped).scraper_trigger()

ActivityScraper(url="https://www.linkedin.com/in/sanjana-athreya/recent-activity/all/").scraper_trigger()
JobScraper(url = "https://www.linkedin.com/jobs/search/?currentJobId=3774112607&geoId=103644278&keywords=data%20scientist&location=United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true").scraper_trigger()
