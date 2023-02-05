import requests
import os
import pandas as pd
import datetime 
# it's not possible to select article from previous years
# Get articles from start_date until today
header = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                         "KHTML, like Gecko) Version/4.0 Safari/534.30"}

ticker_map = {'btc': 1, 'eth': 1027, 'bnb': 1839, 'xrp': 52, 'ada': 2010}
file_name = {'btc': 'bitcoin', 'eth': 'ethereum', 'bnb': 'binance-coin', 'xrp': 'xrp', 'ada': 'cardano'}

def get_latest_article(tickers :list, number_of_article :int, start_date :str, data_path: str) -> str: 
    if isinstance(tickers, str):
        tickers = [tickers]
    df = pd.DataFrame()
    article_date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    start_date_date_format = "%Y-%m-%d"
    start_date = datetime.datetime.strptime(start_date,start_date_date_format).date()
    # Create data dir if it's not existing
    if not os.path.exists(data_path):
        os.makedirs(data_path)  
    for ticker in tickers:
        coin_number = ticker_map.get(ticker.lower(), None)
        if coin_number is None:
            raise Exception(r'It seems that the coin numbers have changed. Please check: https://coinmarketcap.com/currencies/{fullcoinname}/news/')
        path = os.path.join(data_path, "coinmarket_latest_news.csv")
        #url = f"https://api.coinmarketcap.com/content/v3/news/aggregated?coins=&page=1&size=5"
        url = f"https://api.coinmarketcap.com/content/v3/news?coins={coin_number}&page=1&size={number_of_article}"
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            data = response.json()
            if len(data['data']) == 0:
                print('Choose less articles')
            else:
                for n in range(len(data['data'])):
                    meta = data['data'][n]['meta']
                    if meta.get('releasedAt', None) is not None:
                        article_date = datetime.datetime.strptime(meta.get('releasedAt', None), article_date_format).date()
                        if start_date < article_date:
                            date = meta.get('releasedAt', None)
                            coin = ticker
                            section = meta.get('type', None)
                            title = meta.get('title', None)
                            text = meta.get('content', None)
                            sourceUrl = meta.get('sourceUrl', None)
                            source = meta.get('sourceName', None)
                            language = meta.get('language', None)
                            row = pd.DataFrame({
                                
                                'date':date,
                                'coin':coin,
                                'section':section,
                                'title':title,
                                'text' :text,
                                'sourceUrl': sourceUrl,
                                'source':source,
                                'language':language
                            }, index=[0])
                            df = pd.concat([df,row])
    if len(df)<number_of_article:
        print(f"There have been {len(df)} articles published since {start_date}")
    df.to_csv(path, index=False)
    return path
