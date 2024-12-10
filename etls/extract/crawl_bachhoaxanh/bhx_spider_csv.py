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
from colorama import Fore, Style


class BhxSpiderCsv(scrapy.Spider):
    name = 'bhx_spider_csv'
    custom_settings = {
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,  # Number of retries
        'DOWNLOAD_TIMEOUT': 15,  # Increase download timeout
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOAD_DELAY': 2,  # Add a delay between requests
        'FEED_FORMAT': 'json',  # Output format
        'FEED_URI': 'recipe.json',  # Output file
        # 'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'  # Disable duplicate filter

    }

    def __init__(self, *args, **kwargs):
        super(BhxSpiderCsv, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.count = 0

    def start_requests(self):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the CSV file
        csv_file_path = '/Users/duongnguyen/Code/DE_reddit/recipesdb/data/bachhoaxanh/recipelinks/recipe_links.csv'

        # Read URLs from the CSV file
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            reader.__next__()
            print(Fore.GREEN + f"{reader}" + Style.RESET_ALL)
            # rows = list(reader)
            # print(Fore.CYAN + f"Total rows in CSV: {len(rows)}" + Style.RESET_ALL)  # Debugging line for total rows

            for row in reader:
                # print(Fore.GREEN + f"Processing row: {row}" + Style.RESET_ALL)  # Colored debugging line
                url = row[3]
                view_count = row[2]       
                no_csv = row[0]
                print(Fore.GREEN + f"Processing row: {row}" + Style.RESET_ALL)  # Colored debugging line
                print(Fore.GREEN + f"{no_csv} + {view_count}" + Style.RESET_ALL)  # Colored debugging line
                yield scrapy.Request(url=url, meta={'view_count' : view_count,'no_csv':no_csv},callback=self.parse)

    def parse(self, response):
        view_count = response.meta.get('view_count')
        no = response.meta.get('no_csv')
        self.count += 1
        print(Fore.BLUE + f"Processing recipe {self.count}: {response.url}" + Style.RESET_ALL)  # Colored debugging line

        try:
            self.driver.get(response.url)
        except Exception as e:
            self.logger.error(f"Error getting URL: {e}")
            yield {'title': 'Error getting URL'}
            return
    
        time.sleep(1)  # Wait for JavaScript to load the content
        # Extract and decode the title
        title_element = self.driver.find_element(By.XPATH, "//title")
        if title_element.get_attribute("textContent") == "Nội dung không tồn tại - BachhoaXANH.com":
            self.logger.error("404 Page Not Found")
            yield {'title': title_element.get_attribute("textContent")}
            return
        title = title_element.get_attribute("textContent").strip()
        # image_elements = self.driver.find_elements(By.XPATH, "//img[contains(@class,'imgcontent')]")
        # images = [img.get_attribute('src') for img in image_elements]

        # Extract ingredient text and quantity
        ingredient_elements = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'ingredients')]/li")
        ingredients = []
        for element in ingredient_elements:
            try:
                # Extract the full text content
                quantity = element.get_attribute("textContent").replace(element.find_element(By.TAG_NAME, 'a').get_attribute("textContent"), "").strip()
            except Exception as e:
                quantity = '0'
                self.logger.error(f"Error extracting quantity and ingredient: {e}")
            try:
                # Extract the ingredient from the <a> tag within the <li> tag
                ingredient_element = element.find_element(By.TAG_NAME, 'a')
                ingredient = ingredient_element.get_attribute("textContent").strip()
            except Exception as e:
                ingredient = 'a'
                self.logger.error(f"Error extracting quantity and ingredient: {e}")
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

        # # DOWNLOAD IMAGES
        # content_div= self.driver.find_element(By.XPATH, "//div[contains(@class, 'content')]")
        # img_elements = content_div.find_elements(By.TAG_NAME, 'img')
        # for img in img_elements:
        #     img_src = img.get_attribute('src')
        #     self.download_image(img_src, title)

        # # Get Note
        # try:
        #     quote_element = self.driver.find_element(By.XPATH, "//span[@class='quoteGreen quote']")
        #     quote_text = quote_element.get_attribute("textContent").strip()
        #     # self.logger.info(f"Extracted quote text: {quote_text}")
        # except Exception as e:
        #     self.logger.error(f"Error extracting quote text: {e}")
       
        # Locate the ingredients <ul> element
        try:
            ingredients_ul = self.driver.find_element(By.XPATH, "//ul[contains(@class, 'ingredients')]")
            # Find the next sibling <div> with class 'paragraph'
            paragraph_divs = ingredients_ul.find_elements(By.XPATH, "following-sibling::div[@class='paragraph']")
            # Extract the direct text content
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
                    """,p)
                paragraph_texts.append(direct_text)
            join_text = ' '.join(paragraph_texts)

        except Exception as e:
            self.logger.error(f"Error extracting paragraph text: {e}")

        recipe_data = {
            'no': self.count,
            'no_csv': no,
            'title': title,
            'serving': serve_size,
            'prep_time': prep_time,
            'cook_time': cook_time,
            # 'image': images,
            # 'quote': quote_text,
            'ingredients': ingredients,
            'method': join_text,
            'view_count' : view_count
        }
        print(Fore.YELLOW + f"Extracted data: {recipe_data}" + Style.RESET_ALL)  # Debugging line for extracted data
        yield recipe_data



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
                # self.logger.info(f"Image saved: {image_path}")
            else:
                self.logger.error(f"Failed to download image: {url}")
        except Exception as e:
            self.logger.error(f"Error downloading image: {e}")



# Run the spider
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BhxSpiderCsv)
    process.start()