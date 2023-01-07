from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from extractors.indeed import extract_indeed_jobs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from extractors.saramin import extract_saramin_jobs
from extractors.file import save_to_file
keyword = input("원하는 직업의 언어를 입력해주세요!")

indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
saramin = extract_saramin_jobs(keyword)

jobs= indeed+saramin+wwr

save_to_file(keyword,jobs)
    
 