# Project Name: recipesdb

IN PROGRESS 

## Description:
This project focusing on ETL process to create database about recipes on the internet at the moment.
I wish to using collected data to create insightful recipes that is loved and cooked the most. 

## Data Sources:
- Spoonacular API
- Cookpad (Crawled Data)
- bachhoaxanh (Crawled Data)

## Technologies Used:
- Database: Mongodb to save raw data
- Data Warehouse: Postgresql
- Language: Python
- Tools: Selenium, Scrapy, webdriver_manager

## Installation:
### Prerequisites
Before you begin, ensure you have the following installed on your machine:
- Python 3.12
- MongoDB (for database)

#### 1. Clone the Repository
First, clone the repository to your local machine using git:
```sh
git clone https://github.com/hai11duong/recipesdb.git
cd recipesdb
```
#### 2. Create virtual environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### 3. Instal Dependencies
```sh
pip install -r requirements.txt
```

#### 4. Setup Mongodb
I am currently using local mongoDB, you can use Mongo Atlas if you want.
Configure mongo client in utils/load_to_mongodb.py and etls/spoonacular_API/spoonacularTransfer.py for read and write to database server.

### FOR SPOONACULAR 
Crawler data is stored in config/spoonacularConf.json 
```json
{"offset": 0, "key_no": 0, "imported_file": []}
```
#### 1. Setup Spoonacular API.
create your .env, create your spoonacular account for daily free API
```sh
SPOONARCULAR_API_KEY_1=['YOUR_SPOONACULAR_API]
```
|**Note** I use 2 spoonacular accounts to get more free daily quota each day. This also implemented in the code.

#### 2. Run Spoonacular
- Run "spoonacularExtract.py" for saving data into data/output/
- Run "spoonacularTransfer.py" for saving those files into mongodb


### FOR COOKPAD CRAWL (In progress)
#### Running the spider:
1. Navigate to the crawler directory
```sh
cd cookpad_crawler
```
2. Run the crawler using Scrapy
```sh
scrapy crawl cookpad_spider
```
- A list of recipe links will be save in data/cookpad/output
*** Working on the bot check...


### FOR BACHHOAXANH.COM CRAWLER

#### Constants
- `LOG_LEVEL`: Sets the logging level to `logging.ERROR`.
- `MAX_CRAWL`: Defines the maximum number of recipes to crawl (set to 7981).

#### Custom Settings
The spider includes several custom settings to enhance its robustness:
- `RETRY_ENABLED`: Enables retrying failed requests.
- `RETRY_TIMES`: Sets the number of retries to 5.
- `DOWNLOAD_TIMEOUT`: Increases the download timeout to 15 seconds.
- `USER_AGENT`: Sets a custom user-agent string to mimic a real browser.
- `DOWNLOAD_DELAY`: Adds a delay of 2 seconds between requests to avoid overloading the server.

#### Run the spider

1. **Install Dependencies**:
   Ensure you have Scrapy and Selenium installed. You can install them using pip:
   ```sh
   pip install scrapy selenium
   ```

2. **Set Up WebDriver**:
   Download the appropriate WebDriver for your browser (e.g., ChromeDriver for Google Chrome) and ensure it's in your system's PATH.

3. **Run the Spider**:
   Run the spider directly with python file
   ```sh
   python3 bhx_spider.py
   ```

#### Notes
- Ensure that the WebDriver is correctly initialized and handle any exceptions.
- Implement the spider's parsing logic and other necessary methods.
- Test the spider thoroughly to ensure it handles retries, timeouts, and other settings as expected.

This documentation provides an overview of the `BhxSpiderSpider` class, its settings, and usage instructions. Add this to your `README.md` to help users understand and utilize your spider effectively.



