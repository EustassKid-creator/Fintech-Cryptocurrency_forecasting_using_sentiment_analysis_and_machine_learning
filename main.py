import os 
from dotenv import load_dotenv 

from Scraping.OtherScraper import cryptocurrency_price_scraper as cryptocurreny
from Scraping.OtherScraper import cointelegraph_link_scraper as cointelegraph
from Scraping.OtherScraper import coindesk_link_scraper as coindesk
from Scraping.OtherScraper import coinmarketcap_article_scraper as coinmarketcap

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Scraping.ScrapyScraper.ScrapyScraper.spiders.coindesk_spider import coindeskSpider
from Scraping.ScrapyScraper.ScrapyScraper.spiders.cointelegraph_spider import cointelegraphSpider
from Scraping.ScrapyScraper.ScrapyScraper.spiders.utoday_spider import uTodaySpider


coindesk_coins = ['bitcoin','xrp','ethereum','binance-coin', 'cardano']
cointelegraph_coins = ['bitcoin','ripple','ethereum','binance-coin', 'cardano']
tickers = ['BTC','XRP','ETH','BNB','ADA']
btc_features = ['BCHAIN/DIFF', 'BCHAIN/AVBLS', 'BCHAIN/HRATE', 'BCHAIN/TOTBC']

BASE_DIR = os.path.dirname(__file__)
#cahnge to update folder
DATA_DIR_LINKS = os.path.join(BASE_DIR,r"Datasets\Links\Update")
DATA_DIR_PRICE= os.path.join(BASE_DIR,r"\Datasets\Price\Update")
DATA_DIR_ARTICLE = os.path.join(BASE_DIR,r"Datasets\Article\Update")
def configure():
    load_dotenv

def run_spider(spider):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
    process.start()

def main():
    # Get coindesk articles links
    #coindesk.get_all_article_links(coins=coindesk_coins, data_path=DATA_DIR_LINKS)
    # Get coindesk article for some days (YYYY-MM-DD)
    #coindesk.get_article_links_since_date(coins=coindesk_coins, number_article=27000, start_date='2015-01-01', DATA_DIR=DATA_DIR_LINKS)

    # Get Cointelegraph article with Selenium (very time-consuming not robust)
    #cointelegraph.start_cointelegraph_scraper(coins=cointelegraph_coins,data_path=DATA_DIR_LINKS )

    # Scrape article from coindesk links
    #run_spider(coindeskSpider)
    # Scrape article from cointelegraph links 
    #run_spider(cointelegraphSpider)
    # Scrape article from uToday
    #run_spider(uTodaySpider)

    # Get all time historical data of a cryptocurrency (start_time=None, end_time=None) or get data of a cryptocurrency for some days
    #cryptocurreny.get_historical_price_data(coins=tickers, start_time="28-12-2022", end_time="31-12-2022", data_path=DATA_DIR_PRICE)
    # Get additional btc price data 
    #cryptocurreny.get_additional_data(features=btc_features, file_name='bitcoin_price_data_additional.csv', api_key=os.getenv('api_key_quandle'), data_path=DATA_DIR_PRICE)

    # Get the latest news articles from coinmarket (Newsaggregator): It's not possible to select article from previous year
    # Scrapes from the current date to the start date -> set the number_of_article high enough
    coinmarketcap.get_latest_article(tickers=tickers,number_of_article=942,start_date='2023-01-01',data_path=DATA_DIR_ARTICLE)





if __name__  == '__main__':
    configure()
    main()
