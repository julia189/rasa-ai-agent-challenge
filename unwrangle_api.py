import requests
import os
import json
import pandas as pd 

UNWRANGLE_API_KEY = os.getenv('UNWRANGLE_API_KEY')

PRODUCT_INFORMATION_COLS = ['name', 'price', 'brand', 'url', 'rating', 'is_prime', 'shipping_info']

def get_products(search_word: str, retailer: str, n_search_results, sorting_attribute: str):

    #country_dict = {'USA': 'us'}

    #country_code = country_dict[country]

    url = f'https://data.unwrangle.com/api/getter/?platform=amazon_search&search={search_word}&country_code=de&api_key={UNWRANGLE_API_KEY}'
    response = requests.get(url).json()
    data = dict(response)

    if data['success'] == True:
        products_df = pd.DataFrame(data['results'])

        if sorting_attribute == 'rating':
            products_df = products_df.sort_values(by='rating', ascending=False)
        elif sorting_attribute == 'price':
            products_df = products_df.sort_values(by='price', ascending=True)

    products_df = products_df.head(n_search_results)  

    products_df = products_df[PRODUCT_INFORMATION_COLS]
   
    return products_df

print(get_products("baby phone", retailer='amazon', n_search_results=3, sorting_attribute='price'))
