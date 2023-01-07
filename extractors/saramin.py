from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_page_count(keyword):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지 코드
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #에러 메시지 제거
    
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options) #최신 크롬 유지
    cnt=1
    while True:
        base_url="https://www.saramin.co.kr/zf_user/search?searchword="
        browser.get(f"{base_url}{keyword}&recruitPage={cnt}")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        pagination = soup.find("div",class_="more_bottom")
        if pagination == None:
            return cnt
        cnt+=1
        if cnt==20 :
            return cnt
def extract_saramin_jobs(keyword):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지 코드
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #에러 메시지 제거
    
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options) #최신 크롬 유지
    
    base_url="https://www.saramin.co.kr/zf_user/search?searchword="
    pages = get_page_count(keyword)
    results=[]
    for x in range(1,pages+1):
        browser.get(f"{base_url}{keyword}&recruitPage={x}")
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("div", class_="content")
        jobs = job_list.find_all("div",class_="item_recruit")
        for job in jobs:
            to_name_link = job.find("div",class_="area_corp")
            anchor = to_name_link.select_one("strong a")
            name = anchor.string.strip()
            link = anchor['href']
            to_position = job.find("div",class_="job_sector")
            pos_a = to_position.find_all("a")
            position = ''
            for pos in pos_a:
                position = position+pos.string.strip()+' '
            location = ''
            to_location = job.find("div",class_="job_condition")
            loc_a = to_location.find_all("a")
            for loc in loc_a:
                location=location+loc.string.strip()+' '
            job_data={
                    'link':f"https://www.saramin.co.kr{link}",
                    'company':name,
                    'location':location,
                    'position':position
                }
            results.append(job_data)
    return results
