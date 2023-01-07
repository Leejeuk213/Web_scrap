from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

total_cnt=0
def get_page_count(keyword):
    global total_cnt
    if total_cnt >= 15:
        total_cnt=15
        return
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지 코드
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #에러 메시지 제거
    
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options) #최신 크롬 유지
    
    base_url="https://kr.indeed.com/jobs?q="
    browser.get(f"{base_url}{keyword}&start={total_cnt*10}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav",class_="css-jbuxu0 ecydgvn0")
    if pagination == None:
        total_cnt+=1
        return 
    pages = pagination.find_all("div",recursive=False)
    if len(pages)==5:
        total_cnt+=5
    elif len(pages)>5:
        total_cnt+=5
        get_page_count(keyword)
    else :
        total_cnt+=len(pages)
    return
    
def extract_indeed_jobs(keyword):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지 코드
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #에러 메시지 제거
    
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options) #최신 크롬 유지
    
    base_url="https://kr.indeed.com/jobs?q="
    pages = get_page_count(keyword)
    results=[]
    for x in range(total_cnt):
        browser.get(f"{base_url}{keyword}&start={10*x}")
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all('li', recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span",class_="companyName")
                location = job.find("div",class_="companyLocation")
                job_data={
                    'link':f"https://kr.indeed.com{link}",
                    'company':company.string.replace(","," "),
                    'location':location.string.replace(","," "),
                    'position':title.replace(","," ")
                }
                results.append(job_data)
    return results