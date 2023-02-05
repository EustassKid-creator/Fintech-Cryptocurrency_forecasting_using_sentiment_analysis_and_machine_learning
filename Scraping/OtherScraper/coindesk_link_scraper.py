import requests
import os 
import pandas as pd
import datetime


header = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                         "KHTML, like Gecko) Version/4.0 Safari/534.30"}

# Get article links from start_date until today
def get_article_links_since_date(coins :list, number_article :int, start_date :str, data_path :str) -> str:
    if isinstance(coins, str):
        coins = [coins]
    
    source_urls = []
    article_date_format = "%b %d, %Y"
    start_date_format = "%Y-%m-%d"
    # Convert start_date string to date object
    start_date = datetime.datetime.strptime(start_date, start_date_format).date()
    if not os.path.exists(data_path):
        os.makedirs(data_path)             
    path = os.path.join(data_path, coin + f"_article_links_{start_date}_coindesk.csv")

    # Iterate over each coin
    for coin in coins:
        article_count = 0
        end_index_num = 0
        exit_flag = False
        # Continue making requests until the number of articles is reached or the date of publication is before start_date
        while True:
            try:
                url = f"https://api.queryly.com/json.aspx?queryly_key=d0ab87fd70264c0a&query={coin}&endindex={end_index_num}&batchsize=10"
                end_index_num += 10
                response = requests.get(url, headers=header)
                if response.status_code == 200:
                    data = response.json()
                    exit_flag = False
                    # Iterate over each article in the response data
                    for i in range(len(data['items'])):
                        article_date = datetime.datetime.strptime(data['items'][i].get('pubdate', None), article_date_format).date()
                        # If the date of publication is after start_date, append the link and date to the respective lists
                        if article_date < start_date:
                            exit_flag = True
                            break
                        source_urls.append('https://coindesk.com' + data['items'][i].get('link', None))
                        article_count += 1
                if exit_flag:
                    df = pd.DataFrame({'sourceUrl': source_urls})
                    df.to_csv(path, index=False, header=False)
                    print(f"There have been {article_count} articles published for {coin} since {start_date}")
                    break
                if len(source_urls) == number_article:
                    break
            except Exception as e:
                break
    return path

def round_to_nearest_10(x):
    return round(x, -1)

def get_all_article_links(coins :list, data_path :str) -> str: 
    if isinstance(coins, str):
        coins = [coins]
    for coin, _ in coins.items():
        end_index_num = 0 
        hyperlinks = []
        # Create data dir if it's not existing
        if not os.path.exists(data_path):
            os.makedirs(data_path)              
        path = os.path.join(data_path, coin + "_all_article_links_coindesk.csv")
        df = pd.DataFrame()
        while True:
            url = f"https://api.queryly.com/json.aspx?queryly_key=d0ab87fd70264c0a&query={coin}&endindex={end_index_num}&batchsize=10"
            response = requests.get(url, headers=header)
            data = response.json()
            for i in range(len(data['items'])):
                hyperlinks.append('https://www.coindesk.com'+data['items'][i]['link']) 

            if end_index_num == round_to_nearest_10(int(data['metadata']['total'])):
                print(f"There have been {len(df)} articles published for {coin}")
                df = df.append(hyperlinks)
                df.to_csv(path, index=False, header=False)
                break
            else:
                end_index_num += 10
    return path