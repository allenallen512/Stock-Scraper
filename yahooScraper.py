from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from transformers import pipeline
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

#links below work well
AP_url = "https://apnews.com/article/jpmorgan-chase-jamie-dimon-banks-inflation-interest-rates-548e07bdf224819952a626633904b5cf"
dell_news = "https://arstechnica.com/gadgets/2024/06/nearly-half-of-dells-workforce-refused-to-return-to-the-office/"
apple_news = "https://www.cnet.com/personal-finance/credit-cards/apple-and-goldman-sachs-fined-89-million-by-cfpb-for-apple-card-failures/"
jp_link = "https://www.cnet.com/news/privacy/jpmorgan-cyberbreach-exposed-contact-info-for-75m-households/"
link = "https://finance.yahoo.com/news/heres-why-bank-ozk-ozk-135009802.html"
yahoo_test_link = "https://finance.yahoo.com/news/image-playground-chatgpt-more-apple-171354855.html"


ticker = "AAPL"
yahooLanding: f"https://finance.yahoo.com/quote/{ticker}/news/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_yahoo_article_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, 'html.parser')
    
    article_content = soup.find('div', class_='body yf-5ef8bf')
    title_content = soup.find('h1', class_='cover-title yf-j1dsr3')
    
    if article_content and title_content:
        paragraphs = article_content.find_all('p')
        full_article = '\n'.join([p.text for p in paragraphs])
        # print("title: ", title_content.text)
        # print("content: ", full_article)
        return title_content.text, full_article
    else:
        print("could not get content")
        return None, None
    
    
def get_yahoo_finance_news_links(ticker):
    
    yahoo_news_url = f"https://finance.yahoo.com/quote/{ticker}/news/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Get the news page
    news_page = requests.get(yahoo_news_url, headers=headers)
    news_soup = BeautifulSoup(news_page.text, 'html.parser')

    # Find all news items
    news_items = news_soup.find_all('li', class_="stream-item story-item yf-1usaaz9")

    # Extract links from all news items
    links = []
    for item in news_items:
        link_element = item.find('a', class_="subtle-link fin-size-small thumb yf-1e4diqp")
        if link_element and 'href' in link_element.attrs:
            # Use urljoin to handle relative URLs
            full_url = urljoin('https://finance.yahoo.com', link_element['href'])
            links.append(full_url)

    return links, len(links)

# # Example usage
# ticker = "Dell"
# news_links = get_yahoo_finance_news_links(ticker)
# for i, link in enumerate(news_links, 1):
#     print(f"Article {i}: {link}")
#     print("\n")

def get_yahoo_articles_for_ticker(ticker, num_links=5):
    news_links, total_links = get_yahoo_finance_news_links(ticker)
    print("here are the links: ", news_links)
    articles_dict = {}
    total_articles = 0
    link_index = 0

    while total_articles < 5 and link_index < total_links:
        title, content = get_yahoo_article_content(news_links[link_index])
        if title is not None and content is not None:
            print("inside first if")
            articles_dict[title] = content
            total_articles += 1
            print("added one to the list")
        link_index += 1

        if total_articles < 5:
            additional_links = get_yahoo_finance_news_links(ticker)
            news_links.extend(additional_links)

    # Print the dictionary in a readable format
    print(f"\nArticles for {ticker}:")
    for i, (title, content) in enumerate(articles_dict.items(), 1):
        print(f"\n{i}. Title: {title}")
        print("-" * 50)
        print(f"Content: {content[:200]}...")  # Print first 200 characters of content
        print("-" * 50)

    return articles_dict




def analyze_sentiment(title, content):
    from transformers import pipeline
    tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
    model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')

    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)    
    
    # Tokenize the content
    encoded = tokenizer.encode(content, add_special_tokens=False)
    
    # Split content into chunks of 510 tokens to allow for [CLS] and [SEP] tokens
    chunk_size = 510
    chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
    
    sentiment_scores = []
    
    for chunk in chunks:
        # Decode the chunk back to text
        chunk_text = tokenizer.decode(chunk)
        result = sentiment_pipeline(chunk_text)[0]
        print(f"Label: {result['label']}, Score: {result['score']:.4f}")
        sentiment_scores.append(result['score'] if result['label'] == 'POSITIVE' else -result['score'] if result['label'] == 'NEGATIVE' else 0)
    
    # Calculate average sentiment
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    
    # Determine overall sentiment label
    overall_label = 'POSITIVE' if avg_sentiment > 0 else 'NEGATIVE' if avg_sentiment < 0 else 'NEUTRAL' if avg_sentiment == 0 else 'NEUTRAL'
    
    # Print the sentiment analysis result
    print("\nSentiment Analysis Result:")
    print(f"\nTitle: {title}")
    print(f"Overall Sentiment: {overall_label}")
    print(f"Average Sentiment Score: {abs(avg_sentiment):.4f}")
    
    return {
        'label': overall_label,
        'score': abs(avg_sentiment)
    }

# # Example usage
ticker = "AAPL"
articles = get_yahoo_articles_for_ticker(ticker)

print(f"\nSentiment Analysis for {ticker} articles:")
print("=" * 50)

for i, (title, content) in enumerate(articles.items(), 1):
    sentiment_result = analyze_sentiment(title, content)
    
    print(f"\nArticle {i}:")
    print(f"Title: {title}")
    print(f"Sentiment: {sentiment_result['label']}")
    print(f"Score: {sentiment_result['score']:.4f}")
    print("-" * 50)

print("\nAnalysis complete.")






