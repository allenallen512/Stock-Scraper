import requests
from bs4 import BeautifulSoup
from newspaper import Article
import urllib.parse

def get_first_news_url(company_name):
    query = urllib.parse.quote(f"{company_name} news")
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try different selectors to find news articles
    selectors = [
        'div.g div.yuRUbf > a',  # Common selector for news results
        'div.xuvV6b > a',        # Alternative selector
        'div.g a[href^="https://"]',  # Any link in a result div starting with https://
    ]
    
    for selector in selectors:
        results = soup.select(selector)
        if results:
            return results[0]['href']
    
    return None

def get_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def main():
    company_name = input("Enter the company name: ")
    
    news_url = get_first_news_url(company_name)
    if news_url:
        print(f"Found news article: {news_url}")
        article_text = get_article_text(news_url)
        print("\nArticle text:")
        print(article_text)
    else:
        print("No news articles found for the given company.")

if __name__ == "__main__":
    main()