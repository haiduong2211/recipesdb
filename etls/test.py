import time
import logging
from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Ensure chromedriver is in the system PATH
driver_path = which('chromedriver')
if not driver_path:
    logger.error("Chromedriver not found in system PATH")
    raise FileNotFoundError("Chromedriver not found in system PATH")


# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--disable-dev-shm-usage")

keyword = 'beef'
# Create a new instance of the Chrome driver
service = ChromeService(executable_path=driver_path)
with webdriver.Chrome(service=service, options=chrome_options) as driver:
    # Navigate to Cookpad
    driver.get(f'https://www.cookpad.com/vn/tim-kiem/{keyword}')
    time.sleep(3)
    # Perform actions on Cookpad here
    # get all the links
    try:
        recipe_links = driver.find_elements(By.XPATH,'//div[@class="flex-auto m-rg"]//a')
        if len(recipe_links) == 0:
            print("No elements found")
            # get the window size
            window_height = driver.execute_script("return window.innerHeight")
            window_width = driver.execute_script("return window.innerWidth")
            # Calcualte the cordinate
            x = window_width // 2
            y = window_height // 5 * 3
            # Perform actions on the cordinate
            actions = ActionChains(driver)
            actions.move_by_offset(x, y).pause(1).click_and_hold().perform()
            print("start clicking")
            # Wiggle the mouse while holding
            for _ in range(5):
                actions.move_by_offset(3, 0).pause(0.25).perform()  # Move right
                actions.move_by_offset(-4, 0).pause(0.13).perform()  # Move left
                actions.move_by_offset(0, 1).pause(0.5).perform()  # Move down
                actions.move_by_offset(0, -1).pause(0.2).perform()  # Move up
            time.sleep(4)
            actions.release().perform()
            time.sleep(90)
    except Exception as e:
        print(f"Timeout waiting for elements\n {e}")
        print(driver.page_source)
        recipe_links = []
    for link in recipe_links:
        href = link.get_attribute('href')
        if href.startswith('/vn/') is False:
            continue
        else:
            href = 'https://cookpad.com' + href
        print(href)
        # driver.get(href)
        time.sleep(50)
    # The browser will automatically close when exiting the context manager