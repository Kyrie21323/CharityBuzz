# Charity Campaigns and News Data Analysis

## Project Description

This project collects data on charity campaigns from **Chuffed.org** using **Selenium** for web scraping and gathers related news articles using the **News API**. The primary goal is to analyze how charity campaigns are represented in the media and to find potential correlations between campaigns and media coverage. The data is combined and analyzed to provide insights into how similar topics are covered in fundraising efforts and news articles.

To handle potential differences between campaign titles and news article titles, **fuzzy matching** is used to compare similar topics. This approach is necessary because the exact matches between titles from both sources are rare, making it difficult to find overlapping topics directly.

### Data Collected:
- **Chuffed.org Campaigns**: The project scrapes campaign titles and URLs from the https://chuffed.org/discover website.
- **News Articles**: The project fetches charity-related news articles from the News API, gathering the title, description, and publication date.

---

## Purpose:
This project aims to understand the relationship between charity campaigns and how they are covered in news media. By using fuzzy matching to compare campaign and article titles, the project attempts to find correlations between fundraising efforts and media attention.

### Why This Dataset Is Valuable:
While charity platforms like Chuffed.org provide information about campaigns, there is no publicly available dataset that directly compares charity campaigns to their coverage in the media. The combination of data from both **Chuffed.org** and the **News API** allows us to explore patterns in media coverage, which could be useful for campaigners, analysts, or researchers looking to improve their understanding of how charitable efforts are represented in the news.

This dataset is not publicly available for free elsewhere, making it a unique resource for analysis.

---

## How to Run the Project

### Prerequisites:
Before running the project, you need the following installed on your system:
- **Python 3.x**
- **Selenium**
- **Pandas**
- **Requests**
- **BeautifulSoup4**
- **fuzzywuzzy**

### Step-by-Step Instructions:

1. **Clone the Repository**:
   First, clone this GitHub repository to your local machine:
   ```bash
   git clone https://github.com/your-username/charity_campaigns_analysis.git
   cd charity_campaigns_analysis
   ```

2. **Set Up the Environment**:
   Install the required Python libraries by running the following command:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scraper**:
   To scrape the Chuffed.org campaigns and fetch the News API data, run the following command:
   ```bash
   python main.py
   ```

   This will scrape the campaign titles from Chuffed.org and fetch news articles related to charity fundraising. The data will be cleaned, and the results will be saved to `chuffed_campaigns.csv` and `cleaned_charity_news.csv`.

4. **Analyze the Combined Data**:
   After running the scraper, the project will use fuzzy matching to compare campaign titles and news article titles. The combined data is saved in:
   ```bash
   combined_data.csv
   ```

---

## Key Files in This Repository

- **main.py**: The main script that scrapes Chuffed.org campaign data, fetches charity news articles using the News API, and combines the two datasets using fuzzy matching.
- **chuffed_campaigns.csv**: Contains the scraped Chuffed.org campaign titles and URLs.
- **cleaned_charity_news.csv**: Contains the cleaned news data (title, description, and publication date) fetched from the News API.
- **combined_data.csv**: The final merged dataset that uses fuzzy matching to compare charity campaigns and news articles.
- **requirements.txt**: Lists all the necessary dependencies to run the project.
- **ETHICS.md**: Contains a description of the ethical considerations taken into account for this project.

---

## Ethical Considerations

### Respect for Website’s Terms of Service:
I have reviewed **Chuffed.org**'s [robots.txt](https://chuffed.org/robots.txt) and ensured that my web scraping complies with their guidelines. The scraping is done responsibly with proper rate limiting to avoid overwhelming the server.

### Data Handling and Privacy:
- The data collected from **Chuffed.org** and the **News API** is used solely for educational purposes and personal analysis.
- I did not collect or share any personally identifiable information.
- No sensitive data is stored or misused, ensuring compliance with user privacy guidelines.

### Responsible API Use:
- My use of the **News API** follows the terms of service, and API calls are limited to prevent excessive usage or overloading the server.

---

## Note About Fuzzy Matching

For this project, **fuzzy matching** was implemented to compare similar topics between Chuffed.org campaigns and news articles. I used **ChatGPT** to learn how to effectively implement fuzzy matching with the **fuzzywuzzy** library because I wasn't able to get enough exact matches between the scraped data and the fetched data from the News API.

The reason for using fuzzy matching is that the titles from Chuffed.org and the news articles tend to differ a lot, and exact matches between the two sources were rare. Without fuzzy matching, the combined dataset would have been too small to provide meaningful analysis.
