import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from scrapy.crawler import CrawlerProcess
import requests
import os

class BhxSpiderCsv(scrapy.Spider):
    name = 'bhx_spider_csv'
    custom_settings = {
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
        'DOWNLOAD_TIMEOUT': 15,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOAD_DELAY': 2,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    }

    def __init__(self, *args, **kwargs):
        super(BhxSpiderCsv, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.count = 0

    def start_requests(self):
        # Read URLs from the CSV file
        with open('bhx_link.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                url = row[3]
                view_count = row[2]
                no_csv = row[0]
                yield scrapy.Request(url=url, meta={'view_count': view_count, 'no_csv': no_csv}, callback=self.parse)

    def parse(self, response):
        view_count = response.meta.get('view_count')
        no = response.meta.get('no_csv')
        self.count += 1
        try:
            self.driver.get(response.url)
        except Exception as e:
            self.logger.error(f"Error getting URL: {e}")
            yield {'title': 'Error getting URL'}
            return

        time.sleep(2)  # Wait for JavaScript to load the content

        # Extract and decode the title
        title_element = self.driver.find_element(By.XPATH, "//title")
        if title_element.get_attribute("textContent") == "Nội dung không tồn tại - BachhoaXANH.com":
            self.logger.error("404 Page Not Found")
            yield {'title': title_element.get_attribute("textContent")}
            return
        title = title_element.get_attribute("textContent").strip()

        # Extract ingredient text and quantity
        ingredient_elements = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'ingredients')]/li")
        ingredients = []
        for element in ingredient_elements:
            try:
                quantity = element.get_attribute("textContent").replace(element.find_element(By.TAG_NAME, 'a').get_attribute("textContent"), "").strip()
            except Exception as e:
                quantity = '0'
                self.logger.error(f"Error extracting quantity: {e}")
            try:
                ingredient_element = element.find_element(By.TAG_NAME, 'a')
                ingredient = ingredient_element.get_attribute("textContent").strip()
            except Exception as e:
                ingredient = 'a'
                self.logger.error(f"Error extracting ingredient: {e}")
            ingredients.append({'quantity': quantity, 'ingredient': ingredient})

        # Extract serve_size, prep_time, and cook_time
        try:
            serve_size = self.driver.find_element(By.XPATH, "//span[contains(@class, 'resources')]/span[3]").get_attribute("textContent").strip()
        except Exception as e:
            serve_size = 'N/A'
            self.logger.error(f"Error extracting serve_size: {e}")

        try:
            prep_time = self.driver.find_element(By.XPATH, "//span[contains(@class, 'resources')]/span[1]").get_attribute("textContent").strip()
        except Exception as e:
            prep_time = 'N/A'
            self.logger.error(f"Error extracting prep_time: {e}")

        try:
            cook_time = self.driver.find_element(By.XPATH, "//span[contains(@class, 'resources')]/span[2]").get_attribute("textContent").strip()
        except Exception as e:
            cook_time = 'N/A'
            self.logger.error(f"Error extracting cook_time: {e}")

        # Locate the ingredients <ul> element
        try:
            ingredients_ul = self.driver.find_element(By.XPATH, "//ul[contains(@class, 'ingredients')]")
            paragraph_divs = ingredients_ul.find_elements(By.XPATH, "following-sibling::div[@class='paragraph']")
            paragraph_texts = []
            for p in paragraph_divs:
                direct_text = self.driver.execute_script("""
                    var element = arguments[0];
                    var child = element.firstChild;
                    var text = '';
                    while (child) {
                        if (child.nodeType === Node.TEXT_NODE) {
                            text += child.nodeValue;
                        }
                        child = child.nextSibling;
                    }
                    return text;
                """, p)
                paragraph_texts.append(direct_text)
            join_text = ' '.join(paragraph_texts)
        except Exception as e:
            join_text = ''
            self.logger.error(f"Error extracting paragraph text: {e}")

        # Yield data to the output file
        yield {
            'no': self.count,
            'no_csv': no,
            'title': title,
            'serving': serve_size,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'ingredients': ingredients,
            'method': join_text,
            'view_count': view_count
        }

    def closed(self, reason):
        self.driver.quit()

    def download_image(self, url, title):
        self.image_count = 0
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.image_count += 1
                image_folder = 'images'
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)
                image_path = os.path.join(image_folder, f"{self.count}.{self.image_count}_{title}.jpg")
                with open(image_path, 'wb') as file:
                    file.write(response.content)
            else:
                self.logger.error(f"Failed to download image: {url}")
        except Exception as e:
            self.logger.error(f"Error downloading image: {e}")

# Run the spider
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BhxSpiderCsv)
    process.start()