import requests
import os
import json
import pandas as pd 
from oxylabs import RealtimeClient
import pprint

UNWRANGLE_API_KEY = os.getenv('UNWRANGLE_API_KEY')

PRODUCT_INFORMATION_COLS = ['name', 'price', 'brand', 'url', 'rating', 'is_prime', 'shipping_info']

def get_products(search_word: str, retailer: str, n_search_results: int, sorting_attribute: str):

    #country_dict = {'USA': 'us'}

    #country_code = country_dict[country]

    url = f'https://data.unwrangle.com/api/getter/?platform=amazon_search&search={search_word}&country_code=de&api_key={UNWRANGLE_API_KEY}'
    response = requests.get(url).json()
    data = dict(response)

    if data['success'] == True:
        products_df = pd.DataFrame(data['results'])

        if sorting_attribute == 'rating':
            products_df = products_df.sort_values(by='rating', ascending=False).reset_index(drop=True)
        elif sorting_attribute == 'price':
            products_df = products_df.sort_values(by='price', ascending=True).reset_index(drop=True)


    products_df = products_df.head(n_search_results)  

    products_df = products_df[PRODUCT_INFORMATION_COLS]
   
    return products_df

def create_oxylab_client():
    OXYLABS_USERNAME = os.getenv("OXYLABS_USERNAME")
    OXYLABS_PASSWORD = os.getenv("OXYLABS_PASSWORD")
    oxy_client = RealtimeClient(OXYLABS_USERNAME, OXYLABS_PASSWORD)
    return oxy_client

def search_products(search_query: str, retailer: str, n_search_results: int, sorting_attribute:str):

    source_mapping = {
        'amazon': "amazon_search"
    }

    payload = {
    'source': source_mapping[retailer],
    'query': search_query,
    'domain': 'de',
   # 'geo_location': '90210',
    'start_page': '1',
    'pages': '2',
    'parse': True
    }

    USER_NAME = os.getenv("OXYLABS_USERNAME")
    PASSWORD = os.getenv("OXYLABS_PASSWORD")

    response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=(USER_NAME, PASSWORD),
    json=payload,
)   
    result = json.loads(response.text)['results']
    return result

print(search_products(search_query="baby phone", retailer="amazon", n_search_results=3, sorting_attribute='price'))