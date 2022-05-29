import requests


def get_indeed_job_posts(job_title, page=0):
    '''Get indeed job postings for a specefic job title
    ## Returns
    HTML structure of the job posts selected page 
    '''
    job_title = job_title.replace(' ', '+')
    start = page * 10  # posts pagination (0, 10, 20,...)
    url = f'https://eg.indeed.com/jobs?q={job_title}&start={start}'
    response = requests.get(url)
    return response.content
