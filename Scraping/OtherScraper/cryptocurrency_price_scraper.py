import os 
from cryptocmd import CmcScraper
import quandl
import pandas as pd




def get_historical_price_data(coins :list, start_time :str, end_time :str,  data_path :str) -> str:
    if isinstance(coins, str):
        coins = [coins]
    # Create data dir if it's not existing
    if not os.path.exists(data_path):
        os.makedirs(data_path)  
    for coin in coins:
        try:
            scraper = CmcScraper(coin, start_time, end_time )
            headers, data = scraper.get_data()
            if coin == 'BTC':
                filename = 'bitcoin_price_data'
            elif coin == 'ETH':
                filename = 'ethereum_price_data'
            elif coin == 'BNB':
                filename = 'binance-coin_price_data'
            elif coin == 'ADA':
                filename = 'cardano_price_data'
            elif coin == 'XRP': 
                filename = 'xrp_price_data'
            else:
                filename = coin
            path=f'{filename}_all_time'
            scraper.export("csv", name=path, path=data_path)
            return path
        except Exception as e:
            print('historical_cryptocurrency: Method failed', e)


def get_additional_data(features :list, file_name :str, api_key :str, data_path :str) -> str:
    if isinstance(features, str):
        features = [features]
    # Create data dir if it's not existing
    if not os.path.exists(data_path):
        os.makedirs(data_path)  
    path = os.path.join(data_path, file_name)
    data_sets = []
    for feature in features:
        quandl.ApiConfig.api_key= api_key
        try:
            data = quandl.get(feature)
        except Exception as e:
            print('Qunadl data fetching failed', e)
        data = data.rename(columns={'Value': feature})
        data_sets.append(data)
        
    df = data_sets[0]
    for data in data_sets[1:]:
        df = pd.merge(df, data, on='Date', how='inner')
    df.to_csv(path,index=True, header=True)      
    return path
