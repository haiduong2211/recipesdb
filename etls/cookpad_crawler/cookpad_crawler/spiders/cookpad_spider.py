# cookpad_crawler/spiders/cookpad_spider.py

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


class CookpadSpider(scrapy.Spider):
    name = "cookpad_spider"
    start_urls = ['https://cookpad.com/vn/tim-kiem/pork']
    # start_urls = ['https://google.com']

    def start_requests(self):
        chrome_options = Options()
        # Comment out the next line to disable headless mode
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse,wait_time=10,screenshot=True)

    def parse(self, response):
        # driver = response.meta['driver']
        driver = uc.Chrome(headless=True,use_subprocess=False)
        driver = uc.Chrome(headless=True,use_subprocess=False)
        driver.get('https://nowsecure.nl')


        #export driver to a html file
        with open('cookpad.html', 'w') as f:
            f.write(driver.page_source)
        try:
            self.humanize(driver)
            recipe_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="flex-auto m-rg"]//a'))
            )
        except TimeoutException:
            print("Timeout waiting for elements")
            recipe_links = []
        time.sleep(5)
        print("\n=====================================")
        print(recipe_links)
        for link in recipe_links[0:2]:
            href = link.get_attribute('href')
            if href.startswith('/vn/') is False:
                continue
            else:
                href = 'https://cookpad.com' + href
            yield scrapy.Request(url=href, callback=self.parse_recipe)

    def parse_recipe(self, response):
        # Extract attributes from the recipe page
        # Get ingredients using XPATH
        ingredients = response.xpath('//div[@class="ingredient-list "]//ol/li').getall()
        for ingredient in ingredients:
            ingredient_id = ingredient.xpath('@id').get()
            print(f"==========={ingredient_id}==============")  
            print(ingredient)
            print("=====================================")
        recipe = {
            'url': response.url,
            'title': response.xpath('//h1/text()').get(),
            'thumpnail': response.xpath('//div[@id="recipe_image"]/a/@href').get(),
            'author': response.xpath('//div[@id="author_profile"]//a/@href').get(),

            # 'ingredients': response.css('div.ingredient::text').getall(),
            # 'instructions': response.css('div.step::text').getall(),
            # 'rating': response.css('span.rating::text').get(),
            # 'reviews': response.css('span.reviews::text').get(),
        }            
        print("=====================================")
        # print(ingredients)
        print("=====================================")
        yield recipe
    
    def humanize(self, driver):
        try:
        # Example: Click on the CAPTCHA toggle button
            toggle_button = driver.find_element(By.ID, "px-block-toggle-button")
            actions = ActionChains(driver)
            actions.click_and_hold(toggle_button).perform()
            time.sleep(10)  # Adjust the wait time as
            actions.release(toggle_button).perform()

        except Exception as e:
            exit(1)
            print(f"\nHUMANIZE ERROR: {e}\n")


# Save the data into a JSON file
# Run the spider with: scrapy crawl cookpad -a keyword=<your-keyword> -o output.json

