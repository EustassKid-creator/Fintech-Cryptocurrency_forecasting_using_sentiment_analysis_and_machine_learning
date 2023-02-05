# Scrapy doesn’t process data in order https://doc.scrapy.org/en/latest/faq.html#does-scrapy-crawl-in-breadth-first-or-depth-first-order
import scrapy
from scrapy.http.request import Request
import os
import re

BASE_DIR = os.getcwd()
DATA_DIR_ARTICLE = os.path.join(BASE_DIR, 'Datasets\Article')[2:]
DATA_DIR_LINKS = os.path.join(BASE_DIR, 'Datasets\Links')


# Dictionary of coins and their respective file names
coins = {
    'bitcoin': 'bitcoin_article_links_coindesk.csv',
    'xrp': 'xrp_article_links_coindesk.csv',
    'ethereum': 'ethereum_article_links_coindesk.csv',
    'binance': 'binance-coin_article_links_coindesk.csv',
    'cardano': 'cardano_article_links_coindesk.csv'
}

ignore_section_links = [
    'https://www.coindesk.com/es/markets',
    'https://www.coindesk.com/markets'
    'https://www.coindesk.com/tech',
    'https://www.coindesk.com/business',
    'https://www.coindesk.com/coindesk'
    'https://www.coindesk.com/sponsored-content',
    'https://www.coindesk.com/consensus-magazine',
    'https://www.coindesk.com/newsletter',
    'https://www.coindesk.com/events',
    'https://www.coindesk.com/layer2',
    'https://www.coindesk.com/policy',
    'https://www.coindesk.com/data',
]

# Regular expression patterns for filtering out links
pattern_short_links = r'^https://www.coindesk.com.{0,30}$'
pattern_pdf_links = r'.pdf$'
pattern_spanish_links = r'/es/'
pattern_learn_links = r'^https://www.coindesk.com/learn/'
pattern_people_links = r'^https://www.coindesk.com/people/'
pattern_research_links = r'^https://downloads.coindesk.com/research/'
pattern_company_links = r'^https://www.coindesk.com/company'
pattern_incides = r'^https://www.coindesk.com/indices'
pattern_podcast = r'^https://www.coindesk.com/podcasts/'
pattern_tv = r'^https://www.coindesk.com/tv'
pattern_videos = r'^https://www.coindesk.com/video'
pattern_other_pages = r"^(?!https://www\.coindesk\.com).*$"
pattern_webinar = r'^https://www.coindesk.com/webinars/'

class coindeskSpider(scrapy.Spider):
    name = "coindesk"

    custom_settings = {
        'FEEDS': {
            fr'{DATA_DIR_ARTICLE}\article_content_coindesk.json': {
                'format': 'json',
                'encoding': 'utf8'
            }
        }
    }

    def start_requests(self):
        # Read the links of the dic files
        for coin, file in coins.items():      
            file_path = os.path.join(DATA_DIR_LINKS, file)
            try:
                with open(file_path, newline='') as f:
                    links = f.readlines()
                    # Remove whitespace
                    links = [link.strip() for link in links]
                    # Filter out links that match the section links and delete double links
                    links = list(set(links).difference(ignore_section_links))
                    # Filter out link that match the pattern links
                    links = [
                        link for link in links
                        if not re.search(pattern_short_links, link) 
                        and not re.search(pattern_pdf_links, link) 
                        and not re.search(pattern_spanish_links, link) 
                        and not re.search(pattern_learn_links, link) 
                        and not re.search(pattern_people_links, link) 
                        and not re.search(pattern_research_links, link) 
                        and not re.search(pattern_company_links, link) 
                        and not re.search(pattern_incides, link) 
                        and not re.search(pattern_podcast, link) 
                        and not re.search(pattern_tv, link) 
                        and not re.search(pattern_videos, link) 
                        and not re.search(pattern_webinar, link)
                        and not re.search(pattern_other_pages, link) 
                        ]
                    for link in links:
                        yield scrapy.Request(link, self.parse, meta={'coin': coin})
            except Exception as e:
                print("coindesk_spider: Links can't be read", e)

    def parse(self, response):
        coin = response.meta['coin']
        # Scrape the article content
        try:
            # specify css selector to ensure that only the article text is scraped (without image descriptions, etc.)
            if len(' '.join(response.css('.at-text p ::text').extract())) > len(' '.join(response.css('.contentstyle__StyledWrapper-g5cdrh-0.gCDWPA ::text').extract())):
                text = ' '.join(response.css('.at-text p ::text').extract())
            else:
                text = ' '.join(response.css('.contentstyle__StyledWrapper-g5cdrh-0.gCDWPA ::text').extract())
                
            yield {
                'date': response.css('.typography__StyledTypography-owin6q-0.fUOSEs::text').get(),
                'coin': coin,
                'section': response.css('.at-category ::text').get(),
                'title': response.css('.at-headline ::text').get(),  # response.css('.fPbJUO::text').get(),
                'text': text,
                'url': response.url
            }
        except Exception as e:
            print("coindesk_spider: Article can't be scraped", e)
