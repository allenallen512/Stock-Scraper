import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
def scrape_website(website):
    print("launching the browser from scrape")
    
    AUTH = 'brd-customer-hl_2fdf6e4b-zone-stock_scraper:uwlu91lxk8yh'
    SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'
    # SBR_WEBDRIVER = f'https://brd-customer-hl_2fdf6e4b-zone-stock_scraper:uwlu91lxk8yh@brd.superproxy.io:9515'
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        # solve_res = driver.execute('executeCdpCommand', {
        #     'cmd': 'Captcha.waitForSolve',
        #     'params': {'detectTimeout': 10000}, 
        # })
        # # print('Taking page screenshot to file page.png')
        # # driver.get_screenshot_as_file('./page.png')
        # print('Captcha solve status: ', solve_res['value']['status'])
        print('Navigated! Scraping page content...')
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'lxml')  # You can also use 'html.parser' instead of 'lxml'
        
        # Find all <h5> tags
        tags = soup.find_all('h5')
        
        print("--------------------------the page source--------------------------")
        print(page_html)
        print("----------------------------------------------------")
        return page_html
        
    #https://brd-customer-hl_2fdf6e4b-zone-stock_scraper:uwlu91lxk8yh@brd.superproxy.io:9515
    
def extract_body_content(htmlContent):
    soup = BeautifulSoup(htmlContent, "lxml")
    bodyContent = soup.body
    
    if bodyContent:
        return str(bodyContent)
    
    return ""

def clean_body_content(body):
    soup = BeautifulSoup(body, "lxml")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
        
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip()) 
    #if a backslash n is not seperating anything, then we are going to remove it to get rid of random backslashes that do  not seperate text
    
    # print(cleaned_content)
    return cleaned_content

def split_content(dom_content, max_length = 6000): #split into batches of maximum batch size for LLM
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
    
    
    
    
    
    

# if __name__ == '__main__':
#   main()