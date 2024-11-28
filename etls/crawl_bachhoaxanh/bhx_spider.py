# https://www.bachhoaxanh.com/kinh-nghiem-hay/cong-thuc-nau-an/2086
from filelock import FileLock

import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv
import logging

#constants
LOG_LEVEL = logging.ERROR
MAX_CRAWL = 7981  # Maximum number of recipes to crawl
# Set up logging
logging.basicConfig(level=LOG_LEVEL)

class BhxSpiderSpider(scrapy.Spider):
    name = "bhx-spider"
    allowed_domains = ["www.bachhoaxanh.com"]
    start_urls = ["https://www.bachhoaxanh.com/kinh-nghiem-hay/cong-thuc-nau-an/2086"]

    # Setup crawler settings HERE FIRST
    custom_settings = {
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,  # Number of retries
        'DOWNLOAD_TIMEOUT': 15,  # Increase download timeout
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOAD_DELAY': 2,  # Add a delay between requests
    }

    def __init__(self, *args, **kwargs):
        super(BhxSpiderSpider, self).__init__(*args, **kwargs)

        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.image_alts = []  # List to store image alt texts and view counts
        self.processed_count = 0
        self.print_count = 0

    def parse(self, response):
        self.driver.get(response.url)
        self.start_index = 0
        while self.processed_count < MAX_CRAWL:
            blog_posts = []
            # Wait for the elements to be present
            try:
                blog_posts = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "mb-5")]'))
                )
            except Exception as e:
                self.logger.error(f"Error waiting for elements: {e}\n ==================")
                return
            
            if not blog_posts:
                self.logger.error("No elements found with the given XPath.\n ==================")

            for post in blog_posts[self.processed_count:]:
                print("TRYING TO GET DATA \n ==================",len(blog_posts))
                # Extract the alt text from the image element
                try:
                    href = post.get_attribute('href')
                    image = post.find_element(By.XPATH, './/img')
                    image_alt = image.get_attribute('alt')
                    view_count_element = post.find_element(By.XPATH, './/div[contains(@class, "leading-3")]')
                    view_count = view_count_element.text.strip()
                    self.image_alts.append({'no': self.processed_count +1,'alt': image_alt, 'view_count': int(view_count.replace('.', '')),'href':href})
                    self.processed_count += 1
                except Exception as e:
                    self.logger.error(f"Error extracting data: {e}")
            
            # Save data by batch
            lock = FileLock("recipe_links.csv.lock")
            with lock:
                self.save_data(start_index=self.start_index, end_index=self.processed_count+1)
            self.start_index = self.processed_count
            #Click "See More" button to load more content
            try:
                see_more_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex cursor-pointer')]")))
                # Scroll to the button
                # time.sleep(1)
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", see_more_button)
                
                # Random sleep to simulate human behavior
                time.sleep(random.randint(1, 3))
                see_more_button.click()                    
                # Wait for new content to load
                WebDriverWait(self.driver, 20).until(EC.staleness_of(see_more_button))
            except Exception as e:
                self.logger.error(f"Error clicking 'See More' button: {e}")
                print(f"\033[91mError clicking 'See More' button: {e}\033[0m")  # Red color
                break


    #Save the list of recipes link to the main data file. 
    def save_data(self,start_index, end_index):
        with open('data/bachhoaxanh/recipelinks/recipe_links.csv', 'a+', newline='') as csvfile:
            fieldnames = ['no','alt', 'view_count', 'href']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not csvfile.tell():
                writer.writeheader()
            for item in self.image_alts[start_index:end_index]:
                writer.writerow(item)
        self.print_count +=1
        print("======================== \n==========================\n",self.print_count)

    def get_recipe(self, url):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "recipe-class")]'))
            )
        except Exception as e:
            self.logger.error(f"Error waiting for recipe elements: {e}\n ==================")
            return None

        recipe_elements = self.driver.find_elements(By.XPATH, '//*[contains(@class, "recipe-class")]')
        recipe_data = [element.text for element in recipe_elements]
        return recipe_data

    def close_spider(self):
        print("Everything is done!")
        self.driver.quit()

# Set up and run the spider
process = CrawlerProcess()
process.crawl(BhxSpiderSpider)
process.start()