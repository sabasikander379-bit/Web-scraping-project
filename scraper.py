import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sys

def scrape_quotes(url):
    """
    Scrape quotes and authors from quotes.toscrape.com
    Returns: List of dictionaries with Quote and Author
    """
    try:
        # Send request to website
        print(f"Connecting to {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if page loaded successfully
        
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract data
        quotes = soup.find_all("span", class_="text")
        authors = soup.find_all("small", class_="author")
        
        # Store in list
        data = []
        for quote, author in zip(quotes, authors):
            data.append({
                "Quote": quote.text.strip('"'),
                "Author": author.text,
                "Scraped_Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        print(f"Successfully scraped {len(data)} quotes!")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to website. {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def save_to_csv(data, filename="quotes.csv"):
    """
    Save scraped data to CSV file
    """
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Data saved successfully to {filename}")
        return df
    except Exception as e:
        print(f"Error saving file: {e}")
        sys.exit(1)

def main():
    """
    Main function to run the scraper
    """
    URL = "https://quotes.toscrape.com/"
    
    print("="*50)
    print("  CodeAlpha Task 1: Web Scraping Project")
    print("="*50)
    
    # Scrape data
    scraped_data = scrape_quotes(URL)
    
    # Save to CSV
    df = save_to_csv(scraped_data)
    
    # Show preview
    print("\nPreview of scraped data:")
    print(df.head(10))
    print("\nTotal records:", len(df))

if __name__ == "__main__":
    main()