import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.common.by import By

directory_path = os.path.dirname(__file__)
chrome_driver_path = os.path.join(directory_path, 'chromedriver.exe')
baseUrl = 'https://cointelegraph.com/tags/'
adguard_path = os.path.join(directory_path, 'adguard.crx')

class CoinTelegraphScraper():
    
    def __init__(self):
        self.chrome_options = ChromeOption()
        self.chrome_options.headless = True
        userAgent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36"
        self.chrome_options.add_argument(f'user-agent={userAgent}')
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(
            executable_path=chrome_driver_path, options=self.chrome_options)

    def scrape_links(self,coin :str) -> list:
        article_links = []
        url = baseUrl+coin
        self.driver.get(url)
        initial_height = self.driver.execute_script("return Math.max( document.body.scrollHeight);")
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#__layout > div > div.layout__wrp > div.bottom-zone > div.privacy-policy.bottom-zone__privacy-policy > div > button.btn.privacy-policy__accept-btn').click()
            while True:
                # Find the load next page button and click it
                next_page_button = self.driver.find_element(By.CSS_SELECTOR, '#__layout > div > div.layout__wrp > main > div > div > div.tag-page__rows > div > div > div > div > button')
                # Scroll to the bottom of the page
                self.driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
                # Click ne load next page button
                next_page_button.click()
                time.sleep(2)
                
                # Get the articles links
                article_links.extend([(e.get_attribute('href')) for e in self.driver.find_elements(By.CSS_SELECTOR, '.post-card-inline__title-link')])
                
                current_height = self.driver.execute_script("return Math.max( document.body.scrollHeight);")
                print(f'Current height:{current_height} , Initial height: {initial_height}')
                # Break if len of articles didn't increased
                if  current_height <= initial_height:
                    break
                initial_height = current_height     
        except Exception as e:
            print('cointelegraph_scraper: Start failed', e)
        finally:
            return article_links


    def close(self):
        self.driver.quit()

def start_cointelegraph_scraper(coins :list, data_path :str) -> str:
    if isinstance(coins, str):
        coins = [coins]
    for coin in coins:
        try:
            # Scrape article links
            scraper = CoinTelegraphScraper()
            links = scraper.scrape_links(coin=coin)
            scraper.close()
            #Create data dir if it's not existing
            if not os.path.exists(data_path):
                os.makedirs(data_path)      
            #Safe scraped article links in .txt file in data dir
            if coin == 'ripple':
                coin == 'xrp'
            path = f'{data_path}/{coin}_article_links_cointelegraph.txt'
            with open(path, 'w') as url_list:
                for link in set(links):
                    url_list.write('%s\n' % link)
            return path
        except Exception as e:
            print(f'cointelegraph_scraper: Cointelegraph-Scraping for coin {coin} failed', e)