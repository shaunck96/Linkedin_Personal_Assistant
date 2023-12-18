import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
import json
import time

final_list = {}

for j in range(25,200,25):
    url_body = "https://www.linkedin.com/jobs/search/?currentJobId=3774112607&geoId=103644278&keywords=data%20scientist&location=United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
    url_final = url_body+"&start={}".format(j)
    
    print(url_final)
    
    time.sleep(50)
    
    resp = requests.get(url_final)
    print(resp)
    
    soup = BeautifulSoup(resp.text,'html.parser')

    divs = soup.find_all('div', class_='base-search-card__info')
    
    joblist = []
    
    try:
        divs = soup.find_all('div', class_='base-search-card__info')
    except:
        print("Empty page, no jobs found")
    
    for item in divs:
        title = item.find('h3').text.strip()
        company = item.find('a', class_='hidden-nested-link')
        location = item.find('span', class_='job-search-card__location')
        parent_div = item.parent
        entity_urn = parent_div['data-entity-urn']
        job_posting_id = entity_urn.split(':')[-1]
        job_url = 'https://www.linkedin.com/jobs/view/'+job_posting_id+'/'

        date_tag_new = item.find('time', class_ = 'job-search-card__listdate--new')
        date_tag = item.find('time', class_='job-search-card__listdate')
        date = date_tag['datetime'] if date_tag else date_tag_new['datetime'] if date_tag_new else ''
        job_description = ''
        job = {
            'title': title,
            'company': company.text.strip().replace('\n', ' ') if company else '',
            'location': location.text.strip() if location else '',
            'date': date,
            'job_url': job_url,
            'job_description': job_description,
            'applied': 0,
            'hidden': 0,
            'interview': 0,
            'rejected': 0
        }
        joblist.append(job)

    print(joblist)
    
    final_list['Pagenum'+str(j)] = joblist

with open('job_dict.txt', 'w') as fp:
    json.dump(final_list, fp)
