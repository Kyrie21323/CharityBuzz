import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
import time
from fuzzywuzzy import process

load_dotenv()
api_key = os.getenv('NEWS_API_KEY')

#fetch news articles from News API
def fetch_news(query, api_key):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"Error: {response.status_code}")
        return []

#scrape Chuffed.org campaign data using Selenium
def scrape_chuffed_with_selenium():
    driver = webdriver.Chrome()
    url = 'https://chuffed.org/discover'
    driver.get(url)
    time.sleep(5)
    #page source after JavaScript has loaded the content
    html = driver.page_source
    
    #parse the page content with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    #find campaign elements
    campaigns = soup.find_all('a', class_='campaign-card__heading-link')

    #store the scraped data
    campaign_titles = []
    campaign_urls = []
    
    #extract the title and URL
    for campaign in campaigns:
        title = campaign.text.strip()
        campaign_titles.append(title)
        #extract campaign URL
        link = campaign['href']
        campaign_urls.append(f"https://chuffed.org{link}")
    
    #create a DataFrame to store the scraped data
    df_chuffed = pd.DataFrame({
        'Campaign Title': campaign_titles,
        'Campaign URL': campaign_urls
    })
    
    #aave the scraped data to a CSV file
    df_chuffed.to_csv('chuffed_campaigns.csv', index=False)
    print("Chuffed campaigns saved to chuffed_campaigns.csv")
    driver.quit()
    
    return df_chuffed

#scrape Chuffed campaign data using Selenium
df_chuffed = scrape_chuffed_with_selenium()

#fetch news articles about charity fundraising
query = 'charity fundraising'
articles = fetch_news(query, api_key)

#check if there are articles returned
if articles:
    #convert articles to a pandas DataFrame
    df_news = pd.DataFrame(articles)
    #data polishing
    #select only title, description, and publishedAt columns for analysis
    df_clean = df_news[['title', 'description', 'publishedAt']].copy()
    
    #convert 'publishedAt' column to datetime format for better handling
    df_clean['publishedAt'] = pd.to_datetime(df_clean['publishedAt'])
    df_clean = df_clean.dropna(subset=['title', 'description', 'publishedAt'])

    #save the cleaned news data to a CSV file
    df_clean.to_csv('cleaned_charity_news.csv', index=False)
    print("Cleaned news articles saved to cleaned_charity_news.csv")
    
else:
    print("No articles found.")
    df_clean = pd.DataFrame()

# Fuzzy Matching Function
def fuzzy_merge(df1, df2, key1, key2, threshold=80, limit=2):
    """
    df1: First dataframe
    df2: Second dataframe
    key1: Column name in df1 for merging
    key2: Column name in df2 for merging
    threshold: Matching threshold (0-100)
    limit: Number of top matches to return
    """
    s = df2[key2].tolist()

    matches = df1[key1].apply(lambda x: process.extract(x, s, limit=limit))
    
    # Extract matches that meet the threshold
    df1['Best Match'] = matches.apply(lambda x: [i[0] for i in x if i[1] >= threshold])
    df1['Match Score'] = matches.apply(lambda x: [i[1] for i in x if i[1] >= threshold])

    # Expand the matches into a new DataFrame and merge
    df1_exploded = df1.explode(['Best Match', 'Match Score'])
    return pd.merge(df1_exploded, df2, left_on='Best Match', right_on=key2, how='left')

# Use fuzzy matching to merge the Chuffed data with the News API data based on similar titles
if not df_chuffed.empty and not df_clean.empty:
    combined_df = fuzzy_merge(df_chuffed, df_clean, 'Campaign Title', 'title', threshold=80)

    #save the combined dataset to a new CSV file
    combined_df.to_csv('combined_data.csv', index=False)
    print("Combined dataset saved to combined_data.csv")
else:
    print("One of the datasets is empty; cannot merge.")
