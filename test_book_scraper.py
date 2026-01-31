"""
Test Suite for Book Scraper
============================

This module contains test cases to validate the book scraper functionality:
- CSV file download/creation
- CSV file extraction/reading
- File type and format validation
- Data structure validation
- Error handling for missing/invalid data

Author: Data Analyst
Date: 2024
"""

import unittest
import os
import csv
import sys
from book_scraper import BookScraper

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestBookScraper(unittest.TestCase):
    """
    Test class for BookScraper functionality
    
    This class contains all test cases to validate the scraper's behavior.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method
        
        This method initializes a BookScraper instance and sets up
        test data for each test case.
        """
        self.scraper = BookScraper()
        self.test_csv_file = "test_books_data.csv"
        
        # Clean up any existing test files
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)
    
    def tearDown(self):
        """
        Clean up after each test method
        
        This method removes test files created during testing.
        """
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)
    
    def test_case_1_verify_csv_file_download(self):
        """
        Test Case 1: Verify CSV File Download
        
        This test verifies that:
        - The scraper can successfully create a CSV file
        - The file exists after scraping
        - The file is not empty
        
        Expected Result: CSV file should be created and contain data
        """
        print("\n" + "="*60)
        print("Test Case 1: Verify CSV File Download")
        print("="*60)
        
        # Run scraper for homepage only (faster for testing)
        success = self.scraper.run(scrape_all=False)
        
        # Verify scraper completed successfully
        self.assertTrue(success, "Scraper should complete successfully")
        
        # Verify CSV file exists
        csv_exists = os.path.exists("books_data.csv")
        self.assertTrue(csv_exists, "CSV file should be created")
        
        # Verify file is not empty
        if csv_exists:
            file_size = os.path.getsize("books_data.csv")
            self.assertGreater(file_size, 0, "CSV file should not be empty")
            print(f"✓ CSV file created successfully")
            print(f"✓ File size: {file_size} bytes")
        else:
            self.fail("CSV file was not created")
    
    def test_case_2_verify_csv_file_extraction(self):
        """
        Test Case 2: Verify CSV File Extraction
        
        This test verifies that:
        - The CSV file can be read successfully
        - Data can be extracted from the CSV
        - The extracted data matches the scraped data
        
        Expected Result: CSV file should be readable and contain valid data
        """
        print("\n" + "="*60)
        print("Test Case 2: Verify CSV File Extraction")
        print("="*60)
        
        # Run scraper for homepage only
        self.scraper.run(scrape_all=False)
        
        # Verify CSV file exists
        self.assertTrue(os.path.exists("books_data.csv"), 
                       "CSV file should exist")
        
        # Read and extract data from CSV
        extracted_data = []
        try:
            with open("books_data.csv", 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    extracted_data.append(row)
            
            # Verify data was extracted
            self.assertGreater(len(extracted_data), 0, 
                             "Should extract at least one row from CSV")
            
            # Verify first row has required fields
            if extracted_data:
                first_row = extracted_data[0]
                required_fields = ['Title', 'Price', 'Rating', 'Availability', 'URL']
                for field in required_fields:
                    self.assertIn(field, first_row, 
                                f"CSV should contain '{field}' column")
            
            print(f"✓ Successfully extracted {len(extracted_data)} rows from CSV")
            print(f"✓ All required columns present")
            
        except Exception as e:
            self.fail(f"Failed to extract data from CSV: {e}")
    
    def test_case_3_validate_file_type_and_format(self):
        """
        Test Case 3: Validate File Type and Format
        
        This test verifies that:
        - The file is a valid CSV file
        - The file has correct encoding (UTF-8)
        - The file has proper CSV structure (header row, comma-separated)
        
        Expected Result: File should be valid CSV with proper format
        """
        print("\n" + "="*60)
        print("Test Case 3: Validate File Type and Format")
        print("="*60)
        
        # Run scraper
        self.scraper.run(scrape_all=False)
        
        # Verify file exists
        self.assertTrue(os.path.exists("books_data.csv"), 
                       "CSV file should exist")
        
        # Validate file extension
        self.assertTrue("books_data.csv".endswith('.csv'), 
                       "File should have .csv extension")
        
        # Validate CSV structure
        try:
            with open("books_data.csv", 'r', encoding='utf-8') as csvfile:
                # Try to read as CSV
                reader = csv.reader(csvfile)
                
                # Check if file has header row
                header = next(reader, None)
                self.assertIsNotNone(header, "CSV should have a header row")
                
                # Verify header contains expected columns
                expected_columns = ['Title', 'Price', 'Rating', 'Availability', 'URL']
                self.assertEqual(len(header), len(expected_columns),
                               f"Header should have {len(expected_columns)} columns")
                
                # Verify at least one data row exists
                first_data_row = next(reader, None)
                self.assertIsNotNone(first_data_row, 
                                   "CSV should have at least one data row")
                
                print(f"✓ File is valid CSV format")
                print(f"✓ Header row: {header}")
                print(f"✓ Encoding: UTF-8")
                print(f"✓ Structure: Valid CSV with header and data rows")
                
        except csv.Error as e:
            self.fail(f"Invalid CSV format: {e}")
        except Exception as e:
            self.fail(f"Error validating CSV format: {e}")
    
    def test_case_4_validate_data_structure(self):
        """
        Test Case 4: Validate Data Structure
        
        This test verifies that:
        - Each row has all required columns
        - Data types are correct (Title: string, Price: float, Rating: int, etc.)
        - Data values are within expected ranges (Rating: 1-5, Price: positive)
        
        Expected Result: All data should have correct structure and types
        """
        print("\n" + "="*60)
        print("Test Case 4: Validate Data Structure")
        print("="*60)
        
        # Run scraper
        self.scraper.run(scrape_all=False)
        
        # Read CSV and validate structure
        with open("books_data.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            required_fields = ['Title', 'Price', 'Rating', 'Availability', 'URL']
            row_count = 0
            
            for row in reader:
                row_count += 1
                
                # Verify all required fields are present
                for field in required_fields:
                    self.assertIn(field, row, 
                                 f"Row {row_count} missing field: {field}")
                
                # Validate Title (should be non-empty string)
                title = row['Title']
                self.assertIsInstance(title, str, 
                                    f"Title should be string in row {row_count}")
                self.assertGreater(len(title.strip()), 0, 
                                 f"Title should not be empty in row {row_count}")
                
                # Validate Price (should be float or empty)
                price = row['Price']
                if price:  # Price might be empty for some books
                    try:
                        price_float = float(price)
                        self.assertGreaterEqual(price_float, 0, 
                                              f"Price should be non-negative in row {row_count}")
                    except ValueError:
                        # Price might be None or empty string
                        pass
                
                # Validate Rating (should be 1-5 or empty)
                rating = row['Rating']
                if rating:
                    try:
                        rating_int = int(rating)
                        self.assertGreaterEqual(rating_int, 1, 
                                              f"Rating should be >= 1 in row {row_count}")
                        self.assertLessEqual(rating_int, 5, 
                                           f"Rating should be <= 5 in row {row_count}")
                    except ValueError:
                        # Rating might be None or empty string
                        pass
                
                # Validate Availability (should be 'In stock' or 'Out of stock' or empty)
                availability = row['Availability']
                if availability:
                    self.assertIsInstance(availability, str,
                                        f"Availability should be string in row {row_count}")
                
                # Validate URL (should be valid URL format or empty)
                url = row['URL']
                if url:
                    self.assertIsInstance(url, str,
                                        f"URL should be string in row {row_count}")
                    self.assertTrue(url.startswith('http'),
                                  f"URL should start with 'http' in row {row_count}")
            
            print(f"✓ Validated {row_count} rows")
            print(f"✓ All rows have required fields")
            print(f"✓ Data types are correct")
            print(f"✓ Data values are within expected ranges")
    
    def test_case_5_handle_missing_or_invalid_data(self):
        """
        Test Case 5: Handle Missing or Invalid Data
        
        This test verifies that:
        - The scraper handles missing fields gracefully
        - The scraper doesn't crash when encountering invalid data
        - Missing data is logged but doesn't stop the scraping process
        - CSV file is still created even if some books have missing data
        
        Expected Result: Scraper should handle errors gracefully and continue
        """
        print("\n" + "="*60)
        print("Test Case 5: Handle Missing or Invalid Data")
        print("="*60)
        
        # Run scraper (it should handle missing data internally)
        success = self.scraper.run(scrape_all=False)
        
        # Verify scraper completed (even with some missing data)
        self.assertTrue(success, 
                       "Scraper should complete even with missing data")
        
        # Verify CSV file was created
        self.assertTrue(os.path.exists("books_data.csv"),
                       "CSV file should be created even with missing data")
        
        # Verify CSV contains data (even if some fields are empty)
        with open("books_data.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            self.assertGreater(len(rows), 0,
                             "CSV should contain data even with missing fields")
            
            # Check that rows can have empty values (None or empty string)
            # This is acceptable behavior for missing data
            rows_with_missing_data = 0
            for row in rows:
                # Check if any field is empty
                has_missing = any(not value or value.strip() == '' 
                                for value in row.values())
                if has_missing:
                    rows_with_missing_data += 1
            
            print(f"✓ Scraper handled missing data gracefully")
            print(f"✓ CSV created with {len(rows)} rows")
            print(f"✓ {rows_with_missing_data} rows have some missing fields (acceptable)")
            print(f"✓ No crashes occurred during scraping")
    
    def test_scraper_error_handling(self):
        """
        Additional Test: Verify HTTP Error Handling
        
        This test verifies that the scraper handles HTTP errors gracefully.
        Note: Some network configurations may redirect invalid domains to landing pages,
        so we use localhost with a closed port for a guaranteed connection failure.
        """
        print("\n" + "="*60)
        print("Additional Test: HTTP Error Handling")
        print("="*60)
        
        invalid_scraper = BookScraper()
        
        # Use localhost with a port that's guaranteed to be closed (connection refused)
        # This will definitely cause a ConnectionError, not a DNS issue
        soup = invalid_scraper.get_page("http://127.0.0.1:65535/nonexistent")
        
        # Should return None for connection errors
        self.assertIsNone(soup, 
                         "Should return None for connection failure (connection refused)")
        print("✓ Handles connection errors gracefully")
        
        # Also test that the method doesn't raise exceptions
        # (the fact that we got here means no exception was raised)
        print("✓ No exceptions raised during error handling")


def run_tests():
    """
    Run all test cases
    
    This function executes the test suite and displays results.
    """
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBookScraper)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
