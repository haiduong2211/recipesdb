# Project Name: recipesdb

## Description:
This project focusing on ETL process to create database about recipes on the internet at the moment.
I wish to using collected data to create insightful recipes that is loved and cooked the most. 

## Data Sources:
- Spoonacular API
- Cookpad (Crawled Data)
- bachhoaxanh (Crawled Data)

## Technologies Used:
- Database: Mongodb to save raw data
- Data Warehouse: [To Be Update]
- Language: Python
- Tools: Selenium, Scrapy, webdriver_manager

## Installation:
### Prerequisites
Before you begin, ensure you have the following installed on your machine:
- Python 3.x
- pip
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
#### 5. Setup Spoonacular API.
create your .env, create your spoonacular account for daily free API
```sh
SPOONARCULAR_API_KEY_1=['YOUR_SPOONACULAR_API]
```
- I use 2 spoonacular accounts to get more free daily quota each day.

#### 6. Run Spoonacular
- Run "spoonacularExtract.py" for saving data into data/output/
- Run "spoonacularTransfer.py" for saving those files into mongodb


### FOR COOKPAD CRAWL (In progress)
#### 7. Running the spider:
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

