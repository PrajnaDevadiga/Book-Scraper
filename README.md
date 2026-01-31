# Book Scraper - Books to Scrape Website

## 📋 Project Overview

This project implements a comprehensive web scraper to extract book data from [Books to Scrape](http://books.toscrape.com/), a practice website designed for web scraping. The scraper collects book information including titles, prices, ratings, availability status, and product URLs, then stores the data in a structured CSV format for analysis.

## 🎯 Business Objectives

### Primary Goals
- **Data Collection**: Automate the collection of book data from the Books to Scrape website
- **Data Analysis**: Enable data analysts to analyze book trends, pricing patterns, and stock availability
- **Scalability**: Handle large-scale data extraction (1000+ books) across multiple pages
- **Reliability**: Implement robust error handling to ensure data collection continues even when encountering issues

### Use Cases
1. **Market Research**: Analyze book pricing trends and availability across different categories
2. **Inventory Analysis**: Track stock availability patterns
3. **Competitive Analysis**: Compare book ratings and pricing
4. **Data Mining**: Extract structured data for further processing and analysis

## 🏗️ Business Flow

### High-Level Process Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    BOOK SCRAPER WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

1. INITIALIZATION
   ├── Create scraper instance
   ├── Configure HTTP session with headers
   └── Initialize data storage

2. PAGE NAVIGATION
   ├── Start from homepage (http://books.toscrape.com/)
   ├── Extract books from current page
   └── Find and follow pagination links

3. DATA EXTRACTION (Per Book)
   ├── Extract Title
   ├── Extract Price
   ├── Extract Rating (1-5 stars)
   ├── Extract Availability (In stock/Out of stock)
   └── Extract Product URL

4. ERROR HANDLING
   ├── Handle missing fields (skip book, log warning)
   ├── Handle HTTP errors (404, 503, etc.)
   ├── Handle network errors (timeout, connection issues)
   └── Continue processing despite errors

5. DATA STORAGE
   ├── Collect all book data
   ├── Validate data structure
   └── Write to CSV file (books_data.csv)

6. COMPLETION
   ├── Log summary statistics
   └── Return success/failure status
```

### Detailed Business Logic

#### 1. **Initialization Phase**
- **Purpose**: Set up the scraper environment
- **Actions**:
  - Initialize HTTP session with appropriate headers (User-Agent)
  - Set request delay to be respectful to the server
  - Initialize empty data storage list
- **Output**: Ready-to-use scraper instance

#### 2. **Page Scraping Phase**
- **Purpose**: Extract all books from a single page
- **Actions**:
  - Send HTTP GET request to page URL
  - Parse HTML using BeautifulSoup
  - Locate all book elements (`<article class="product_pod">`)
  - Extract data from each book element
- **Output**: List of book dictionaries from the page

#### 3. **Pagination Handling**
- **Purpose**: Navigate through all pages of books
- **Actions**:
  - Start from homepage
  - After scraping each page, find the "next" button
  - Construct next page URL
  - Continue until no "next" button exists
- **Output**: Complete list of all books across all pages

#### 4. **Data Extraction Logic**
- **Title Extraction**:
  - Source: `<h3><a title="...">` tag
  - Validation: Must exist (critical field)
  - Error Handling: Skip book if title missing

- **Price Extraction**:
  - Source: `<p class="price_color">` tag
  - Format: "£XX.XX" (British pounds)
  - Conversion: Remove currency symbol, convert to float
  - Error Handling: Set to None if missing

- **Rating Extraction**:
  - Source: `<p class="star-rating X">` tag
  - Mapping: "One"→1, "Two"→2, ..., "Five"→5
  - Validation: Must be between 1-5
  - Error Handling: Set to None if missing

- **Availability Extraction**:
  - Source: `<p class="instock">` or `<p class="outofstock">` tag
  - Normalization: Convert to "In stock" or "Out of stock"
  - Error Handling: Set to None if missing

- **URL Extraction**:
  - Source: `<h3><a href="...">` tag
  - Conversion: Convert relative URL to absolute URL
  - Error Handling: Set to None if missing

#### 5. **Error Handling Strategy**
- **Missing Fields**: Log warning, set field to None, continue processing
- **HTTP Errors (404, 503, etc.)**: Log error, return None, skip page
- **Network Errors**: Log error, retry logic (if needed), continue
- **Invalid Data Format**: Log warning, set to None, continue
- **Critical Errors**: Log error, skip book/page, don't crash entire process

#### 6. **Data Storage Phase**
- **Purpose**: Persist scraped data to CSV file
- **Actions**:
  - Define CSV columns: Title, Price, Rating, Availability, URL
  - Write header row
  - Write data rows (one per book)
  - Handle encoding (UTF-8)
- **Output**: `books_data.csv` file

## 📁 Project Structure

```
User Story4/
│
├── book_scraper.py          # Main scraper script
├── test_book_scraper.py     # Test suite
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation file
├── books_data.csv           # Output file (generated after running)
└── scraper.log              # Log file (generated during execution)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd "User Story4"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "import requests, bs4; print('Dependencies installed successfully!')"
   ```

## 💻 Usage

### Basic Usage

#### Scrape All Books (All Pages)
```bash
python book_scraper.py
```

This will:
- Scrape all books from all pages (~1000 books)
- Save data to `books_data.csv`
- Create log file `scraper.log`

#### Scrape Homepage Only (20 Books)
```python
from book_scraper import BookScraper

scraper = BookScraper()
scraper.run(scrape_all=False)  # Only homepage
```

#### Custom Usage
```python
from book_scraper import BookScraper

# Create scraper instance
scraper = BookScraper(base_url="http://books.toscrape.com/")

# Scrape all pages
scraper.run(scrape_all=True)

# Access scraped data
print(f"Total books scraped: {len(scraper.books_data)}")
print(scraper.books_data[0])  # First book data
```

### Running Tests

```bash
python test_book_scraper.py
```

Or using unittest:
```bash
python -m unittest test_book_scraper.py -v
```

## 📊 Output Format

### CSV File Structure

The `books_data.csv` file contains the following columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Title | String | Book title | "A Light in the Attic" |
| Price | Float | Book price in GBP | 51.77 |
| Rating | Integer | Star rating (1-5) | 3 |
| Availability | String | Stock status | "In stock" |
| URL | String | Product page URL | "http://books.toscrape.com/.../index.html" |

### Sample CSV Output
```csv
Title,Price,Rating,Availability,URL
"A Light in the Attic",51.77,3,"In stock","http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
"Tipping the Velvet",53.74,1,"In stock","http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
...
```

## 🧪 Test Cases

The project includes comprehensive test cases:

### Test Case 1: Verify CSV File Download
- **Objective**: Ensure CSV file is created successfully
- **Validates**: File existence, file size > 0
- **Status**: ✅ Implemented

### Test Case 2: Verify CSV File Extraction
- **Objective**: Ensure data can be read from CSV
- **Validates**: CSV readability, data extraction, required columns
- **Status**: ✅ Implemented

### Test Case 3: Validate File Type and Format
- **Objective**: Ensure file is valid CSV format
- **Validates**: File extension, encoding (UTF-8), CSV structure
- **Status**: ✅ Implemented

### Test Case 4: Validate Data Structure
- **Objective**: Ensure data has correct structure and types
- **Validates**: Required fields, data types, value ranges
- **Status**: ✅ Implemented

### Test Case 5: Handle Missing or Invalid Data
- **Objective**: Ensure scraper handles errors gracefully
- **Validates**: Error handling, graceful degradation, no crashes
- **Status**: ✅ Implemented

## 🔧 Configuration

### Adjustable Parameters

In `book_scraper.py`, you can modify:

```python
# Request delay (seconds between requests)
scraper.request_delay = 1  # Default: 1 second

# Base URL
scraper = BookScraper(base_url="http://books.toscrape.com/")

# Output filename
scraper.save_to_csv(filename="custom_filename.csv")
```

## 📝 Logging

The scraper generates detailed logs in `scraper.log`:

- **INFO**: General progress information
- **WARNING**: Missing fields, skipped books
- **ERROR**: HTTP errors, network issues, critical failures

### Log Format
```
2024-01-15 10:30:45 - INFO - Fetching page: http://books.toscrape.com/
2024-01-15 10:30:46 - INFO - Found 20 books on page
2024-01-15 10:30:47 - WARNING - Price not found for book: Example Book
2024-01-15 10:30:50 - INFO - Scraping completed. Total books scraped: 1000
```

## ⚠️ Error Handling

### Handled Scenarios

1. **Missing Book Fields**
   - Action: Log warning, set field to None, continue
   - Example: Book without price

2. **HTTP Errors (404, 503, etc.)**
   - Action: Log error, skip page, continue
   - Example: Page not found

3. **Network Errors**
   - Action: Log error, return None, continue
   - Example: Connection timeout

4. **Invalid Data Format**
   - Action: Log warning, set to None, continue
   - Example: Invalid price format

5. **Empty Pages**
   - Action: Log info, continue to next page
   - Example: No books found

## 🔍 Code Documentation

### Key Classes

#### `BookScraper`
Main scraper class that handles all scraping operations.

**Methods**:
- `__init__()`: Initialize scraper
- `get_page()`: Fetch and parse webpage
- `extract_rating()`: Convert rating class to number
- `extract_book_data()`: Extract data from book element
- `scrape_page()`: Scrape all books from a page
- `get_next_page_url()`: Find next page URL
- `scrape_all_pages()`: Scrape all pages with pagination
- `save_to_csv()`: Save data to CSV file
- `run()`: Main execution method

### Key Functions

#### `extract_book_data(book_element)`
Extracts all required fields from a single book HTML element.

**Returns**: Dictionary with keys: Title, Price, Rating, Availability, URL

#### `scrape_all_pages()`
Orchestrates pagination and scrapes all books across all pages.

**Returns**: List of all book dictionaries

## 📈 Performance Considerations

- **Request Delay**: 1 second between requests (configurable)
- **Timeout**: 10 seconds per request
- **Expected Duration**: ~20-30 minutes for all pages (1000 books)
- **Memory Usage**: Moderate (stores all books in memory before writing)

## 🛡️ Best Practices Implemented

1. **Respectful Scraping**: Delays between requests
2. **Error Handling**: Graceful degradation, no crashes
3. **Logging**: Comprehensive logging for debugging
4. **Code Documentation**: Detailed comments and docstrings
5. **Type Hints**: Type annotations for better code clarity
6. **Modular Design**: Separated concerns, reusable methods
7. **Testing**: Comprehensive test suite

## 🐛 Troubleshooting

### Common Issues

1. **No books scraped**
   - Check internet connection
   - Verify website is accessible
   - Check `scraper.log` for errors

2. **CSV file not created**
   - Check file permissions
   - Verify scraper completed successfully
   - Check `scraper.log` for errors

3. **Missing data in CSV**
   - Some books may have missing fields (expected behavior)
   - Check `scraper.log` for warnings

4. **Slow scraping**
   - Normal for large datasets
   - Adjust `request_delay` if needed (but be respectful)

## 📄 License

This project is for educational and data analysis purposes.

## 👥 Author

Data Analyst - UnifyCX Internship

## 📅 Version History

- **v1.0** (2024): Initial release
  - Full scraping functionality
  - Pagination support
  - Error handling
  - CSV export
  - Comprehensive test suite

## 🔗 References

- [Books to Scrape Website](http://books.toscrape.com/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Library Documentation](https://requests.readthedocs.io/)

---

## 📞 Support

For issues or questions, please check:
1. `scraper.log` for detailed error messages
2. Test suite output for validation issues
3. Code comments for implementation details

---

**Happy Scraping! 📚**
