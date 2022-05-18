import requests
import pandas as pd

from bs4 import BeautifulSoup

#get content website page
def extract(page):
   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
   url = f'https://ca.indeed.com/jobs?q=Front%20End%20Developer&l=Vancouver%2C%20BC&radius=25&start={page}'
   req = requests.get(url, headers)
   soup = BeautifulSoup(req.text, "html.parser")
   return soup

#extract all the div = job_seen_beacon
def transform(soup):
  divs = soup.find_all('div', class_ = 'job_seen_beacon')
  for item in divs:
    jobTitle = item.find('a').text.strip()
    company = item.find('span', class_ = 'companyName').text.strip()
    location = item.find('div', class_ = 'companyLocation').text.strip()
    try:
      salary = item.find('div', class_ = 'attribute_snippet').text.strip()
    except:
      salary = ''
    summary = item.find('div', class_ = 'job-snippet').text.strip().replace('\n','')
    
    try:
      urgentHire = item.find('div', class_ = 'urgentlyHiring').text.strip()
    except:
      urgentHire = ''
    date = ''
    datetemp = item.find('span', class_ = 'date').text.strip() 
    date = date.join(filter(str.isdigit, datetemp))
    
    job = {
        'title': jobTitle,
        'company': company,
        'location': location,
        'salary': salary,
        'summary': summary,
        'urgent': urgentHire,
        'date': date
    }
    jobList.append(job)
  return

jobList = []

for i in range(0,40,10):
  content = extract(i)
  transform(content)
    
df = pd.DataFrame(jobList)
df.to_csv('jobList.csv', header=["Title", "Company", "Location", "Salary", "Summary", "Is Urgent", "Date"], index=False)

print(jobList)