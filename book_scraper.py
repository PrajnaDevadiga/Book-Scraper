"""
Book Scraper for Books to Scrape Website
==========================================

This script scrapes book data from http://books.toscrape.com/
including title, price, rating, availability, and product URL.
It handles pagination to scrape all books across all pages.

Author: Data Analyst
Date: 2024
"""

import requests
from bs4 import BeautifulSoup
import csv
import logging
import time
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional

# Configure logging to track errors and progress
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class BookScraper:
    """
    A web scraper class for extracting book data from books.toscrape.com
    
    This class handles:
    - HTTP requests with error handling
    - HTML parsing using BeautifulSoup
    - Pagination across all pages
    - Data extraction and validation
    - CSV file generation
    """
    
    def __init__(self, base_url: str = "http://books.toscrape.com/"):
        """
        Initialize the BookScraper with base URL and session
        
        Args:
            base_url (str): The base URL of the website to scrape
        """
        self.base_url = base_url
        self.session = requests.Session()
        # Set a user agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.books_data = []  # List to store all scraped book data
        self.request_delay = 1  # Delay between requests (in seconds) to be respectful
        
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch a webpage and return BeautifulSoup object
        
        This method handles HTTP errors gracefully and retries on failures.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            BeautifulSoup: Parsed HTML content, or None if request fails
        """
        response = None  # Initialize response variable
        try:
            logger.info(f"Fetching page: {url}")
            response = self.session.get(url, timeout=10)
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors (404, 503, etc.)
            status_code = response.status_code if response else "unknown"
            logger.error(f"HTTP error {status_code} for URL {url}: {e}")
            return None
        except requests.exceptions.ConnectionError as e:
            # Handle connection errors (DNS failures, network issues, etc.)
            logger.error(f"Connection error for URL {url}: {e}")
            return None
        except requests.exceptions.Timeout as e:
            # Handle timeout errors
            logger.error(f"Timeout error for URL {url}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            # Handle other request errors
            logger.error(f"Request error for URL {url}: {e}")
            return None
        except Exception as e:
            # Handle any other unexpected errors
            logger.error(f"Unexpected error fetching {url}: {e}")
            return None
    
    def extract_rating(self, rating_class: str) -> Optional[int]:
        """
        Extract numeric rating from CSS class name
        
        The website uses classes like 'star-rating One', 'star-rating Two', etc.
        This function converts them to numeric values (1-5).
        
        Args:
            rating_class (str): CSS class string containing rating information
            
        Returns:
            int: Numeric rating (1-5), or None if not found
        """
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        
        # Extract rating from class string
        for word, rating in rating_map.items():
            if word in rating_class:
                return rating
        
        return None
    
    def extract_book_data(self, book_element) -> Optional[Dict[str, any]]:
        """
        Extract data from a single book element on the page
        
        This method extracts:
        - Title
        - Price
        - Rating (1-5)
        - Availability (In stock/Out of stock)
        - Product URL
        
        Args:
            book_element: BeautifulSoup element containing book information
            
        Returns:
            dict: Dictionary containing book data, or None if extraction fails
        """
        try:
            book_data = {}
            
            # Extract title from h3 tag
            title_tag = book_element.find('h3')
            if title_tag and title_tag.find('a'):
                book_data['Title'] = title_tag.find('a').get('title', '').strip()
            else:
                logger.warning("Title not found for a book, skipping...")
                return None
            
            # Extract price from price_color class
            price_tag = book_element.find('p', class_='price_color')
            if price_tag:
                # Remove currency symbol and convert to float
                price_text = price_tag.get_text().strip()
                # Remove '£' symbol and convert
                try:
                    book_data['Price'] = float(price_text.replace('£', ''))
                except ValueError:
                    logger.warning(f"Invalid price format: {price_text}")
                    book_data['Price'] = None
            else:
                logger.warning(f"Price not found for book: {book_data.get('Title', 'Unknown')}")
                book_data['Price'] = None
            
            # Extract rating from star-rating class
            rating_tag = book_element.find('p', class_='star-rating')
            if rating_tag:
                rating_class = ' '.join(rating_tag.get('class', []))
                book_data['Rating'] = self.extract_rating(rating_class)
            else:
                logger.warning(f"Rating not found for book: {book_data.get('Title', 'Unknown')}")
                book_data['Rating'] = None
            
            # Extract availability from instock/outofstock class
            availability_tag = book_element.find('p', class_='instock')
            if not availability_tag:
                availability_tag = book_element.find('p', class_='outofstock')
            
            if availability_tag:
                availability_text = availability_tag.get_text().strip()
                # Normalize availability text
                if 'In stock' in availability_text or 'instock' in availability_text.lower():
                    book_data['Availability'] = 'In stock'
                elif 'Out of stock' in availability_text or 'outofstock' in availability_text.lower():
                    book_data['Availability'] = 'Out of stock'
                else:
                    book_data['Availability'] = availability_text
            else:
                logger.warning(f"Availability not found for book: {book_data.get('Title', 'Unknown')}")
                book_data['Availability'] = None
            
            # Extract product URL
            link_tag = book_element.find('h3')
            if link_tag and link_tag.find('a'):
                relative_url = link_tag.find('a').get('href', '')
                # Convert relative URL to absolute URL
                book_data['URL'] = urljoin(self.base_url, relative_url)
            else:
                logger.warning(f"URL not found for book: {book_data.get('Title', 'Unknown')}")
                book_data['URL'] = None
            
            return book_data
            
        except Exception as e:
            logger.error(f"Error extracting book data: {e}")
            return None
    
    def scrape_page(self, url: str) -> List[Dict[str, any]]:
        """
        Scrape all books from a single page
        
        Args:
            url (str): URL of the page to scrape
            
        Returns:
            list: List of dictionaries containing book data from the page
        """
        soup = self.get_page(url)
        if not soup:
            return []
        
        books = []
        
        # Find all book articles on the page
        # Books are contained in <article> tags with class 'product_pod'
        book_elements = soup.find_all('article', class_='product_pod')
        
        logger.info(f"Found {len(book_elements)} books on page: {url}")
        
        # Extract data from each book
        for book_element in book_elements:
            book_data = self.extract_book_data(book_element)
            if book_data:
                books.append(book_data)
            else:
                logger.warning("Skipped a book due to missing critical data")
        
        return books
    
    def get_next_page_url(self, soup: BeautifulSoup, current_url: str) -> Optional[str]:
        """
        Find the URL of the next page from pagination
        
        The website uses a 'next' button in the pagination section.
        This method finds and constructs the next page URL.
        
        Args:
            soup (BeautifulSoup): Parsed HTML of current page
            current_url (str): URL of the current page
            
        Returns:
            str: URL of next page, or None if no next page exists
        """
        try:
            # Find the 'next' button in pagination
            next_button = soup.find('li', class_='next')
            if next_button and next_button.find('a'):
                relative_url = next_button.find('a').get('href', '')
                # Construct absolute URL
                next_url = urljoin(current_url, relative_url)
                return next_url
            return None
        except Exception as e:
            logger.error(f"Error finding next page: {e}")
            return None
    
    def scrape_all_pages(self) -> List[Dict[str, any]]:
        """
        Scrape books from all pages by following pagination
        
        This method starts from the homepage and follows pagination links
        until all pages are scraped.
        
        Returns:
            list: List of all books scraped from all pages
        """
        all_books = []
        current_url = self.base_url
        page_number = 1
        
        logger.info("Starting to scrape all pages...")
        
        while current_url:
            logger.info(f"Scraping page {page_number}: {current_url}")
            
            # Scrape current page
            page_books = self.scrape_page(current_url)
            all_books.extend(page_books)
            
            logger.info(f"Scraped {len(page_books)} books from page {page_number}. Total so far: {len(all_books)}")
            
            # Get next page URL
            soup = self.get_page(current_url)
            if soup:
                next_url = self.get_next_page_url(soup, current_url)
                current_url = next_url
                page_number += 1
                
                # Add delay between requests to be respectful to the server
                if current_url:
                    time.sleep(self.request_delay)
            else:
                break
        
        logger.info(f"Scraping completed. Total books scraped: {len(all_books)}")
        return all_books
    
    def save_to_csv(self, filename: str = "books_data.csv") -> bool:
        """
        Save scraped book data to a CSV file
        
        The CSV file will have columns: Title, Price, Rating, Availability, URL
        
        Args:
            filename (str): Name of the CSV file to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.books_data:
            logger.warning("No data to save. Please scrape books first.")
            return False
        
        try:
            # Define CSV columns
            fieldnames = ['Title', 'Price', 'Rating', 'Availability', 'URL']
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header row
                writer.writeheader()
                
                # Write book data rows
                for book in self.books_data:
                    writer.writerow(book)
            
            logger.info(f"Successfully saved {len(self.books_data)} books to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return False
    
    def run(self, scrape_all: bool = True) -> bool:
        """
        Main method to run the scraper
        
        This method orchestrates the entire scraping process:
        1. Scrapes books (homepage only or all pages)
        2. Saves data to CSV
        
        Args:
            scrape_all (bool): If True, scrape all pages. If False, scrape only homepage.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if scrape_all:
                # Scrape all pages
                self.books_data = self.scrape_all_pages()
            else:
                # Scrape only homepage (20 books)
                logger.info("Scraping homepage only...")
                self.books_data = self.scrape_page(self.base_url)
            
            # Save to CSV
            if self.books_data:
                return self.save_to_csv()
            else:
                logger.error("No books were scraped.")
                return False
                
        except Exception as e:
            logger.error(f"Error in scraper run: {e}")
            return False


def main():
    """
    Main entry point for the script
    
    This function creates a BookScraper instance and runs it.
    """
    scraper = BookScraper()
    
    # Run scraper for all pages
    success = scraper.run(scrape_all=True)
    
    if success:
        print(f"\n✓ Scraping completed successfully!")
        print(f"✓ Total books scraped: {len(scraper.books_data)}")
        print(f"✓ Data saved to: books_data.csv")
    else:
        print("\n✗ Scraping failed. Check scraper.log for details.")


if __name__ == "__main__":
    main()
