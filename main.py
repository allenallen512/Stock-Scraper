import streamlit as st
from scrape import scrape_website, split_content, clean_body_content, extract_body_content
from bs4 import BeautifulSoup
import newspaper
import nltk
nltk.download('punkt')
def main():
    
    st.title("Welcome to Stock Scraper")
    url = st.text_input("Enter website url")
    
    if url:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        article.nlp()
        authors = article.authors
        
        st.text(authors)
        st.text(article.keywords)
        tab1, tab2 = st.tabs(["Article", "Summary"])
        
        with tab1:
            st.text(article.title)
            st.text(article.text)
            
        with tab2:
            st.text(article.summary)    
        
    return

# def main():
#     st.title("Welcome to Stock Scraper")
#     url = st.text_input("Enter website url")
    
#     if st.button("Scrape Site"):
#         st.write("Scraping Now...")
#         result = scrape_website(url)
#         body_content = extract_body_content(result)
#         cleaned_content = clean_body_content(body_content)
        
#         st.session_state.dom_content = cleaned_content
        
#         with st.expander("View DOM Content"):
#             st.text_area("DOM Content", cleaned_content, height=300)
            
        
#     return


if __name__ == "__main__":
    main()


