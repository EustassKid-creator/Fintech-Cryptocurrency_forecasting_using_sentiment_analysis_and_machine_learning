import scrapy
# Scrapy doesn’t process data in order https://doc.scrapy.org/en/latest/faq.html#does-scrapy-crawl-in-breadth-first-or-depth-first-order
import os 

BASE_DIR = os.getcwd()
DATA_DIR_ARTICLE = os.path.join(BASE_DIR, 'Datasets\Article')[2:]


class uTodaySpider(scrapy.Spider):
    name = "utoday"

    custom_settings = {
        'FEEDS': {
            fr'{DATA_DIR_ARTICLE}\article_content_utoday.json':{
                'format':'json',
                'encoding': 'utf8'
            }
        }
    }

    start_urls = [
        'https://u.today/ethereum-news',
        'https://u.today/bitcoin-news',
        'https://u.today/cardano-ada-coin-news',
        'https://u.today/ripple-news'
    ]

    def parse(self, response):
        try:
            posts = response.css('a.category-item__title-link')
            for post in posts:
                url = post.css('a::attr(href)').get()
                yield response.follow(url=url, callback=self.parse_articles, meta={'Coin':response.url})
        except Exception as e:
            print(e)
            print("\nuToday urls can't be scraped")

        try:
            for n in range(1, len(response.css('li.pag-nav__item a::attr(href)').extract())):
                yield response.follow(response.css('li.pag-nav__item a::attr(href)')[n].extract(), callback=self.parse)
        except Exception as e: 
            print("utoday_spider: Next page can't be crawled", e)

    def parse_articles(self, response):
        coin = response.request.meta['Coin']
        print(coin)
        coin = str.split(str.split(coin,"-")[0],"/")[-1]
        try:
            date = response.css('span::text').get()
            if date == 'Original U.Today article' or date =='Original article based on tweet':
                date = response.css('.humble span::text').get()
            yield {
                'date': date,
                'coin': coin,
                'title': response.css('div.article h1::text').get(),
                'text': ' '.join(response.css('div.article__content p ::text').extract()), 
                'url': response.url
            }
        except Exception as e:
            print("utoday_spider: Article can't be scraped", e)
