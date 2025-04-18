import requests
from requests.exceptions import RequestException
from typing import Union
import pandas as pd
import logging

def get_available_doctors(location: Union[str,int], availabilities: Union[str,int]=1):

    base_url='https://www.doctolib.de'
    speciality='kinderheilkunde-kinder-und-jugendmedizin'
    location=location.lower()

    final_url=f"{base_url}/{speciality}/{location}?/availabilities={availabilities}&insurance_sector=public"

    headers="""accept: application/json
    accept-language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7
    cache-control: no-cache 
    content-type: application/json; charset=utf-8
    referer: https://www.doctolib.de/
    """
    headers = dict(line.strip().split(': ', 1) for line in headers.strip().split('\n') if ': ' in line)

    try:
        response=requests.get(final_url,headers=headers)
        response.raise_for_status()
        
        result_data = dict(response.json())['data']['doctors']
        return pd.DataFrame({'name' : [result_data[i]['name_with_title'] for i in range(3)],
                 'address': [result_data[i]['address'] for i in range(3)],
                'profile_path': [result_data[i]['profile_path'] for i in range(3)]
                 })

    except RequestException as e:
        logging.error(e)
        return None 


#print(get_available_doctors(location='stuttgart', availabilities=1))


