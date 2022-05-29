import requests
from bs4 import BeautifulSoup
import pandas as pd



def get_indeed_job_posts(job_title, page=0):
    '''Get indeed job postings for a specefic job title
    ## Returns
    HTML structure of the job posts selected page 
    '''
    job_title = job_title.replace(' ', '+')
    start = page * 10  # posts pagination (0, 10, 20,...)
    url = f'https://www.indeed.com/jobs?q={job_title}&start={start}'
    response = requests.get(url)
    return response.content


def parse_job_posts(job_posts):
    '''Make a Python list from indeed job posts
    '''
    job_list = []
    jobs = job_posts.find_all('div', class_='cardOutline')
    
    for job in jobs:
        title = job.find('h2').find('a').get_text()

        keywords = ['data', 'bi', 'intelligence', 'analytics', 'etl', 'sql']
        if any(x in title.lower().split() for x in keywords):
            job = {
                'title': title,
                'company': job.find('span', class_='companyName').get_text(),
                'location': job.find('div', class_='companyLocation').get_text(),
                'link': 'https://www.indeed.com{}'.format(
                    job.find('h2').find('a').get('href')
                )
            }
            job_list.append(job)
    return job_list


def get_job_opportunities(job_title):
    page = 0
    last_page = False
    jobs_data = []

    while not(last_page):
        html = get_indeed_job_posts(job_title, page)
        soup = BeautifulSoup(html, 'html.parser')
        
        job_posts = soup.find('ul', class_="jobsearch-ResultsList")
        jobs_data += parse_job_posts(job_posts)

        # indicating last page at Indeed's pagination
        if soup.select('.dupetext'):  
            last_page = True
            
        page += 1

    jobs_df = pd.DataFrame(jobs_data)
    jobs_df.to_csv('dataEng_jobs.csv', index=False)


if __name__ == '__main__':
    get_job_opportunities('data engineer')
