# Scrapy doesn’t process data in order https://doc.scrapy.org/en/latest/faq.html#does-scrapy-crawl-in-breadth-first-or-depth-first-order
# 111 minutes
import scrapy
from scrapy.http.request import Request
import os

BASE_DIR = os.getcwd()
DATA_DIR_ARTICLE = os.path.join(BASE_DIR, 'Datasets\Article')[2:]
DATA_DIR_LINKS = os.path.join(BASE_DIR, 'Datasets\Links')

ignore = 'The views and opinions expressed here are solely those of the author and do not necessarily reflect the views of Cointelegraph. Every investment and trading move involves risk. You should conduct your own research when making a decision.'
ignore2 = 'Market data is provided by  HitBTC  exchange'
# ignore sponsored content

# Dictionary of coins and their respective file names
coins = {
    'bitcoin':'bitcoin_article_links_cointelegraph.txt',
    'xrp':'xrp_article_links_cointelegraph.txt',
    'ethereum':'ethereum_article_links_cointelegraph.txt',
    'binance':'binance-coin_article_links_cointelegraph.txt', 
    'cardano':'cardano__article_links_cointelegraph.txt'
    }

class cointelegraphSpider(scrapy.Spider):
    name = "cointelegraph"

    custom_settings = {
        'FEEDS': {
            fr'{DATA_DIR_ARTICLE}\article_content_cointelegraph.json':{
                'format':'json',
                'encoding': 'utf8'
            }
        }
    }


    def start_requests(self):
        # Read the links of the dic files 
        for coin, file in coins.items():
            file_path = os.path.join(DATA_DIR_LINKS, file)
            try:
                with open(file_path, 'r') as f:
                    links = f.readlines()
                    # Remove whitespace
                    links = [link.strip() for link in links]
                    # Open the links (article)
                    for link in links:
                       yield scrapy.Request(link, self.parse, meta={'coin':coin})
            except Exception as e:
                print("coitelegraph_spider: Links can't be read failed", e)

    def parse(self, response):
        coin = response.meta['coin']
        # Scrape the article content

        try:
            yield{
                'date': response.css('time::text').get(), 
                'coin': coin,
                'section':  response.css('.post-cover__badge::text').get(),
                'title': response.css('.post__title::text').get(),
                'text':  " ".join(response.css('.post-content ::text').extract()),
                'url': response.url
                }
        except Exception as e:
            print("coitelegraph_spider: Article can't be scraped", e)