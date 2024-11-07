# Scrapy settings for cookpad_crawler project
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "cookpad_crawler"

SPIDER_MODULES = ["cookpad_crawler.spiders"]
NEWSPIDER_MODULE = "cookpad_crawler.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Selenium settings
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_ARGUMENTS = ['--headless']  # '--headless' if using headless mode

# Enable the Selenium middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}

# Custom function to create the WebDriver instance
def get_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    for argument in SELENIUM_DRIVER_ARGUMENTS:
        options.add_argument(argument)
    return webdriver.Chrome(service=service, options=options)

SELENIUM_DRIVER_CREATOR = get_driver

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "cookpad_crawler.pipelines.CookpadCrawlerPipeline": 300,
#}