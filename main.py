import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
import time
from fuzzywuzzy import process

# Load API key from .env file
load_dotenv()
api_key = os.getenv('NEWS_API_KEY')

# Function to fetch news articles from News API
def fetch_news(query, api_key):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"Error: {response.status_code}")
        return []

# Function to scrape Chuffed.org campaign data using Selenium
def scrape_chuffed_with_selenium():
    # Initialize Selenium WebDriver (ensure ChromeDriver or GeckoDriver is installed and added to PATH)
    driver = webdriver.Chrome()  # or webdriver.Firefox() if using Firefox
    
    # URL of the Chuffed.org campaign page
    url = 'https://chuffed.org/discover'
    
    # Open the webpage using Selenium
    driver.get(url)
    
    # Allow some time for the page to load completely
    time.sleep(5)  # You can adjust the sleep time as needed
    
    # Get the page source after JavaScript has loaded the content
    html = driver.page_source
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all campaign elements (adjust based on the correct class name)
    campaigns = soup.find_all('a', class_='campaign-card__heading-link')

    # Lists to store the scraped data
    campaign_titles = []
    campaign_urls = []
    
    # Loop through each campaign and extract the title and URL
    for campaign in campaigns:
        # Extract campaign title (the text content of the <a> tag)
        title = campaign.text.strip()
        campaign_titles.append(title)
        
        # Extract campaign URL
        link = campaign['href']
        campaign_urls.append(f"https://chuffed.org{link}")
    
    # Create a DataFrame to store the scraped data
    df_chuffed = pd.DataFrame({
        'Campaign Title': campaign_titles,
        'Campaign URL': campaign_urls
    })
    
    # Save the scraped data to a CSV file
    df_chuffed.to_csv('chuffed_campaigns.csv', index=False)
    print("Chuffed campaigns saved to chuffed_campaigns.csv")
    
    # Close the Selenium WebDriver when done
    driver.quit()
    
    return df_chuffed

# Scrape Chuffed campaign data using Selenium
df_chuffed = scrape_chuffed_with_selenium()

# Fetch news articles about charity fundraising
query = 'charity fundraising'
articles = fetch_news(query, api_key)

# Check if there are articles returned
if articles:
    # Convert articles to a pandas DataFrame
    df_news = pd.DataFrame(articles)
    
    # Select only title, description, and publishedAt columns for analysis
    df_clean = df_news[['title', 'description', 'publishedAt']].copy()
    
    # Convert 'publishedAt' column to datetime format for better handling
    df_clean['publishedAt'] = pd.to_datetime(df_clean['publishedAt'])
    
    # Drop rows with missing values in the selected columns
    df_clean = df_clean.dropna(subset=['title', 'description', 'publishedAt'])

    # Save the cleaned news data to a CSV file
    df_clean.to_csv('cleaned_charity_news.csv', index=False)
    print("Cleaned news articles saved to cleaned_charity_news.csv")
    
else:
    print("No articles found.")
    df_clean = pd.DataFrame()  # Return an empty DataFrame if no articles found

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

    # Save the combined dataset to a new CSV file
    combined_df.to_csv('combined_data.csv', index=False)
    print("Combined dataset saved to combined_data.csv")
else:
    print("One of the datasets is empty; cannot merge.")
