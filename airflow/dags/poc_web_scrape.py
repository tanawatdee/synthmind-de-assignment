from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
from datetime import timedelta
import os
import json
import csv
from time import sleep

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime


def poc_web_scrape_1(ds, **kwargs):
    # ===
    # Aquire Context
    # ===
    print(ds)
    print(kwargs)
    print("kwargs['dag_run'].start_date:")
    print(kwargs["dag_run"].start_date)
    print("kwargs['dag_run'].execution_date:")
    print(kwargs["dag_run"].execution_date)

    # ===
    # Set date variables
    # ===
    now_bangkok = (dt.strptime(ds, "%Y-%m-%d")).isoformat()[:19]
    ytd_bangkok = (dt.strptime(ds, "%Y-%m-%d") + timedelta(days=-30)).isoformat()[:19]

    now_YYYY = now_bangkok[:4]
    now_mm   = now_bangkok[5:7]
    now_dd   = now_bangkok[8:10]

    ytd_YYYY = ytd_bangkok[:4]
    ytd_mm   = ytd_bangkok[5:7]
    ytd_dd   = ytd_bangkok[8:10]

    # ===
    # Config data
    # ===
    stock = 'ADVANC'
    url   = f"https://www.set.or.th/th/market/product/stock/quote/{stock}/news"
    url2  = f"https://www.set.or.th/api/set/news/search?symbol={stock}&fromDate={ytd_dd}%2F{ytd_mm}%2F{ytd_YYYY}&toDate={now_dd}%2F{now_mm}%2F{now_YYYY}&keyword=&lang=th"

    # ===
    # Scraping data
    # ===
    session = requests.Session()
    session.get(url)
    
    res = session.get(
    url2,
        headers={
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=1, i',
            'referer': f'https://www.set.or.th/th/market/product/stock/quote/{stock}/news',
        }
    )
    res_json = res.json()
    
    daily_dir_path_1 = f'./data/1_raw_response/01_set/{now_YYYY}-{now_mm}-{now_dd}'
    daily_dir_path_2 = f'./data/2_clean_response/01_set/{now_YYYY}-{now_mm}-{now_dd}'
    daily_dir_path_3 = f'./data/3_raw_news/01_set/{now_YYYY}-{now_mm}-{now_dd}'

    if not os.path.isdir(daily_dir_path_1):
        os.makedirs(daily_dir_path_1)
        
    if not os.path.isdir(daily_dir_path_2):
        os.makedirs(daily_dir_path_2)
        
    if not os.path.isdir(daily_dir_path_3):
        os.makedirs(daily_dir_path_3)
        
    for i_news, a_news in enumerate(res_json['newsInfoList']):
        try:
            res = requests.get(a_news['url'])
            print(f'Success {i_news:05d}.')
        except:
            print(f'Fail to fetch url `{a_news['url']}`.')

        with open(f'{daily_dir_path_1}/{i_news:05d}.json', 'w') as json_file:
            json.dump(
                {
                    "original_req": a_news,
                    "status_code": res.status_code,
                    "text": res.text,
                }, 
                json_file
            )
    
    # ===
    # Scrape news title, news content
    # ===
    raw_news_data = []
    raw_news_fields = ['news_datetime', 'news_title', 'news_content']

    for i_news, a_news in enumerate(res_json['newsInfoList']):
        with open(f'{daily_dir_path_1}/{i_news:05d}.json', 'r') as json_file:
            try:
                res = json.load(json_file)
                res_text = res['text']

                # print(res_text)

                soup = BeautifulSoup(res_text)

                news_datetime = res['original_req']['datetime']
                news_title    = soup.title.string
                news_content  = soup.select('.raw-html-new')[0].select(".raw-html")[0].string

                a_news = {
                    "news_datetime": news_datetime,
                    "news_title":    news_title,
                    "news_content":  news_content,
                }

                raw_news_data.append(a_news)

                with open(f'{daily_dir_path_2}/{i_news:05d}.json', 'w') as json_file:
                    json.dump(a_news, json_file)
                
                print(f'Success {i_news:05d}. {news_title}')
            except:
                print(f'Fail reading raw json `{a_news['url']}`.')

    with open(f'{daily_dir_path_3}/{i_news:05d}.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=raw_news_fields)
        writer.writeheader()
        writer.writerows(raw_news_data)

def poc_web_scrape_2(ds, **kwargs):
    # ===
    # Aquire Context
    # ===
    print(ds)
    print(kwargs)
    print("kwargs['dag_run'].start_date:")
    print(kwargs["dag_run"].start_date)
    print("kwargs['dag_run'].execution_date:")
    print(kwargs["dag_run"].execution_date)

    # ===
    # Set date variables
    # ===
    now_bangkok = (dt.strptime(ds, "%Y-%m-%d")).isoformat()[:19]
    ytd_bangkok = (dt.strptime(ds, "%Y-%m-%d") + timedelta(days=-30)).isoformat()[:19]

    now_YYYY = now_bangkok[:4]
    now_mm   = now_bangkok[5:7]
    now_dd   = now_bangkok[8:10]

    ytd_YYYY = ytd_bangkok[:4]
    ytd_mm   = ytd_bangkok[5:7]
    ytd_dd   = ytd_bangkok[8:10]
    ytd_dd   = ytd_bangkok[8:10]

    # ===
    # Config data
    # ===
    stock = 'ADVANC'
    urls  = [
        f'https://www.infoquest.co.th/?s={stock}',
        f'https://www.infoquest.co.th/page/2?s={stock}',
        f'https://www.infoquest.co.th/page/3?s={stock}',
        f'https://www.infoquest.co.th/page/4?s={stock}',
        f'https://www.infoquest.co.th/page/5?s={stock}',
    ]

    # ===
    # Scraping data
    # ===
    session = requests.Session()
    original_reqs = []

    for url in urls:
        res = session.get(url)
        res_text = res.text
        soup = BeautifulSoup(res_text)

        original_reqs.extend([
            {
                "title": a.select('.entry-title')[0].select('a')[0].string, 
                "href": a.select('.entry-title')[0].select('a')[0].get('href'),
                "text": a.select('.entry-summary')[0].string or a.select('.entry-summary')[0].text,
                "time": [{
                    "class":    b.get('class'),
                    "datetime": b.get('datetime'),
                    "text":     b.text,
                } for b in a.select('time')],
            }
            for a in soup.select('.content-item')
            if len(a.select('.entry-summary')[0].text) > 1
        ])

    daily_dir_path_1 = f'./data/1_raw_response/02_infoquest/{now_YYYY}-{now_mm}-{now_dd}'
    daily_dir_path_2 = f'./data/2_clean_response/02_infoquest/{now_YYYY}-{now_mm}-{now_dd}'
    daily_dir_path_3 = f'./data/3_raw_news/02_infoquest/{now_YYYY}-{now_mm}-{now_dd}'

    if not os.path.isdir(daily_dir_path_1):
        os.makedirs(daily_dir_path_1)
        
    if not os.path.isdir(daily_dir_path_2):
        os.makedirs(daily_dir_path_2)
        
    if not os.path.isdir(daily_dir_path_3):
        os.makedirs(daily_dir_path_3)

    for i_news, original_req in enumerate(original_reqs):
        try:
            res = requests.get(original_req['href'])
            print(f'Success {i_news:05d}.')
        except:
            print(f'Fail to fetch url `{original_req['href']}`.')

        with open(f'{daily_dir_path_1}/{i_news:05d}.json', 'w') as json_file:
            json.dump(
                {
                    "original_req": original_req,
                    "status_code": res.status_code,
                    "text": res.text,
                }, 
                json_file
            )

        sleep(0.2)

    # ===
    # Scrape news title, news content
    # ===
    raw_news_data = []
    raw_news_fields = ['news_datetime', 'news_title', 'news_content']

    for i_news, original_req in enumerate(original_reqs):
        with open(f'{daily_dir_path_1}/{i_news:05d}.json', 'r') as json_file:
            try:
                res = json.load(json_file)
                res_text = res['text']

                # print(res_text)

                soup = BeautifulSoup(res_text)

                news_datetime = res['original_req']['time'][1]['text']
                news_title    = res['original_req']['title']
                news_content  = soup.select('.entry-content')[0].text if len(soup.select('.entry-content')) > 0 else ''

                a_news = {
                    "news_datetime": news_datetime,
                    "news_title":    news_title,
                    "news_content":  news_content,
                }

                raw_news_data.append(a_news)

                with open(f'{daily_dir_path_2}/{i_news:05d}.json', 'w') as json_file:
                    json.dump(a_news, json_file)
                
                print(f'Success {i_news:05d}. {news_title}')
            except:
                print(f'Fail reading raw json `{a_news['url']}`.')

    with open(f'{daily_dir_path_3}/{i_news:05d}.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=raw_news_fields)
        writer.writeheader()
        writer.writerows(raw_news_data)

def poc_web_scrape_3(ds, **kwargs):
    # ===
    # Aquire Context
    # ===
    print(ds)
    print(kwargs)
    print("kwargs['dag_run'].start_date:")
    print(kwargs["dag_run"].start_date)
    print("kwargs['dag_run'].execution_date:")
    print(kwargs["dag_run"].execution_date)

    # ===
    # Set date variables
    # ===
    now_bangkok = (dt.strptime(ds, "%Y-%m-%d")).isoformat()[:19]
    ytd_bangkok = (dt.strptime(ds, "%Y-%m-%d") + timedelta(days=-30)).isoformat()[:19]

    now_YYYY = now_bangkok[:4]
    now_mm   = now_bangkok[5:7]
    now_dd   = now_bangkok[8:10]

    ytd_YYYY = ytd_bangkok[:4]
    ytd_mm   = ytd_bangkok[5:7]
    ytd_dd   = ytd_bangkok[8:10]

    # ===
    # Config data
    # ===
    stock = 'ADVANC'
    url   = f"https://www.set.or.th/en/market/product/stock/quote/{stock}/news"
    url2  = f"https://www.set.or.th/api/set/news/search?symbol={stock}&fromDate={ytd_dd}%2F{ytd_mm}%2F{ytd_YYYY}&toDate={now_dd}%2F{now_mm}%2F{now_YYYY}&keyword=&lang=en"

    # ===
    # Scraping data
    # ===
    session = requests.Session()
    session.get(url)
    
    res = session.get(
    url2,
        headers={
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=1, i',
            'referer': f'https://www.set.or.th/en/market/product/stock/quote/{stock}/news',
        }
    )
    res_json = res.json()
    
    daily_dir_path_1 = f'./data/1_raw_response/03_seten/{now_YYYY}-{now_mm}-{now_dd}'
    daily_dir_path_2 = f'./data/2_clean_response/03_seten/{now_YYYY}-{now_mm}-{now_dd}'
    daily_dir_path_3 = f'./data/3_raw_news/03_seten/{now_YYYY}-{now_mm}-{now_dd}'

    if not os.path.isdir(daily_dir_path_1):
        os.makedirs(daily_dir_path_1)
        
    if not os.path.isdir(daily_dir_path_2):
        os.makedirs(daily_dir_path_2)
        
    if not os.path.isdir(daily_dir_path_3):
        os.makedirs(daily_dir_path_3)
        
    for i_news, a_news in enumerate(res_json['newsInfoList']):
        try:
            res = requests.get(a_news['url'])
            print(f'Success {i_news:05d}.')
        except:
            print(f'Fail to fetch url `{a_news['url']}`.')

        with open(f'{daily_dir_path_1}/{i_news:05d}.json', 'w') as json_file:
            json.dump(
                {
                    "original_req": a_news,
                    "status_code": res.status_code,
                    "text": res.text,
                }, 
                json_file
            )
    
    # ===
    # Scrape news title, news content
    # ===
    raw_news_data = []
    raw_news_fields = ['news_datetime', 'news_title', 'news_content']

    for i_news, a_news in enumerate(res_json['newsInfoList']):
        with open(f'{daily_dir_path_1}/{i_news:05d}.json', 'r') as json_file:
            try:
                res = json.load(json_file)
                res_text = res['text']

                # print(res_text)

                soup = BeautifulSoup(res_text)

                news_datetime = res['original_req']['datetime']
                news_title    = soup.title.string
                news_content  = soup.select('.raw-html-new')[0].select(".raw-html")[0].string

                a_news = {
                    "news_datetime": news_datetime,
                    "news_title":    news_title,
                    "news_content":  news_content,
                }

                raw_news_data.append(a_news)

                with open(f'{daily_dir_path_2}/{i_news:05d}.json', 'w') as json_file:
                    json.dump(a_news, json_file)
                
                print(f'Success {i_news:05d}. {news_title}')
            except:
                print(f'Fail reading raw json `{a_news['url']}`.')

    with open(f'{daily_dir_path_3}/{i_news:05d}.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=raw_news_fields)
        writer.writeheader()
        writer.writerows(raw_news_data)

def poc_web_scrape_4(ds, **kwargs):
    # ===
    # Aquire Context
    # ===
    print(ds)
    print(kwargs)
    print("kwargs['dag_run'].start_date:")
    print(kwargs["dag_run"].start_date)
    print("kwargs['dag_run'].execution_date:")
    print(kwargs["dag_run"].execution_date)

    # ===
    # Set date variables
    # ===
    now_bangkok = (dt.strptime(ds, "%Y-%m-%d")).isoformat()[:19]
    ytd_bangkok = (dt.strptime(ds, "%Y-%m-%d") + timedelta(days=-30)).isoformat()[:19]

    now_YYYY = now_bangkok[:4]
    now_mm   = now_bangkok[5:7]
    now_dd   = now_bangkok[8:10]

    ytd_YYYY = ytd_bangkok[:4]
    ytd_mm   = ytd_bangkok[5:7]
    ytd_dd   = ytd_bangkok[8:10]
    ytd_dd   = ytd_bangkok[8:10]

    # ===
    # Config data
    # ===
    stock = 'ADVANC'
    urls  = [
        f'https://www.kaohooninternational.com/?s={stock}',
        f'https://www.kaohooninternational.com/page/2?s={stock}',
        f'https://www.kaohooninternational.com/page/3?s={stock}',
        f'https://www.kaohooninternational.com/page/4?s={stock}',
        f'https://www.kaohooninternational.com/page/5?s={stock}',
    ]

    # ===
    # Scraping data
    # ===
    session = requests.Session()
    original_reqs = []

    for url in urls:
        res = session.get(url)
        res_text = res.text
        soup = BeautifulSoup(res_text)

        original_reqs.extend([
            {
                "title": a.select('.entry-title')[0].select('a')[0].string, 
                "href": a.select('.entry-title')[0].select('a')[0].get('href'),
                "text": a.select('.entry-content')[0].string or a.select('.entry-content')[0].text,
                "time": [{
                    "datetime": b.get('datetime'),
                    "text":     b.text,
                } for b in a.select('time')],
            }
            for a in soup.select('.search-item')
            if len(a.select('.entry-content')[0].text) > 1
        ])
    
    daily_dir_path_1 = f'./data/1_raw_response/04_kaohoon/{now_YYYY}-{now_mm}-{now_dd}'
    daily_dir_path_2 = f'./data/2_clean_response/04_kaohoon/{now_YYYY}-{now_mm}-{now_dd}'
    daily_dir_path_3 = f'./data/3_raw_news/04_kaohoon/{now_YYYY}-{now_mm}-{now_dd}'

    if not os.path.isdir(daily_dir_path_1):
        os.makedirs(daily_dir_path_1)
        
    if not os.path.isdir(daily_dir_path_2):
        os.makedirs(daily_dir_path_2)
        
    if not os.path.isdir(daily_dir_path_3):
        os.makedirs(daily_dir_path_3)

    for i_news, original_req in enumerate(original_reqs):
        try:
            res = requests.get(original_req['href'])
            print(f'Success {i_news:05d}.')
        except:
            print(f'Fail to fetch url `{original_req['href']}`.')

        with open(f'{daily_dir_path_1}/{i_news:05d}.json', 'w') as json_file:
            json.dump(
                {
                    "original_req": original_req,
                    "status_code": res.status_code,
                    "text": res.text,
                }, 
                json_file
            )

        sleep(0.2)

    # ===
    # Scrape news title, news content
    # ===
    raw_news_data = []
    raw_news_fields = ['news_datetime', 'news_title', 'news_content']

    for i_news, original_req in enumerate(original_reqs):
        with open(f'{daily_dir_path_1}/{i_news:05d}.json', 'r') as json_file:
            try:
                res = json.load(json_file)
                res_text = res['text']

                # print(res_text)

                soup = BeautifulSoup(res_text)

                news_datetime = res['original_req']['time'][0]['datetime']
                news_title    = res['original_req']['title']
                news_content  = soup.select('.entry-content')[0].text

                a_news = {
                    "news_datetime": news_datetime,
                    "news_title":    news_title,
                    "news_content":  news_content,
                }

                raw_news_data.append(a_news)

                with open(f'{daily_dir_path_2}/{i_news:05d}.json', 'w') as json_file:
                    json.dump(a_news, json_file)
                
                print(f'Success {i_news:05d}. {news_title}')
            except:
                print(f'Fail reading raw json `{a_news['url']}`.')

    with open(f'{daily_dir_path_3}/{i_news:05d}.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=raw_news_fields)
        writer.writeheader()
        writer.writerows(raw_news_data)


# ===
# DAG
# ===
ssh_hook = SSHHook(
    remote_host='spark-master',
    port=22,
    username='root',
    key_file='./config/demo_sshkey',
    cmd_timeout=None
)

with DAG(
    'poc_web_scrape',
    description='POC Web Scrape',
    schedule_interval='@daily',
    start_date=datetime(2025, 5, 12),
    catchup=False,
    concurrency=1,
    max_active_runs=1 # due to resources limitation (not enough RAM)
) as dag:
    op_poc_web_scrape_1 = PythonOperator(
        task_id=f"poc_web_scrape_1", 
        provide_context=True,
        python_callable=poc_web_scrape_1, 
        dag=dag,
    )

    op_poc_web_scrape_2 = PythonOperator(
        task_id=f"poc_web_scrape_2", 
        provide_context=True,
        python_callable=poc_web_scrape_2, 
        dag=dag,
    )

    op_poc_web_scrape_3 = PythonOperator(
        task_id=f"poc_web_scrape_3", 
        provide_context=True,
        python_callable=poc_web_scrape_3, 
        dag=dag,
    )

    op_poc_web_scrape_4 = PythonOperator(
        task_id=f"poc_web_scrape_4", 
        provide_context=True,
        python_callable=poc_web_scrape_4, 
        dag=dag,
    )