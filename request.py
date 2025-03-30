import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re
load_dotenv()
API_KEY=os.getenv(key="x-rapidapi-key")

def get_flipkart_pid(product_name):
    product_name=product_name.lower()
    query = product_name.replace(' ', '-')
    print(query)
    url = f'https://www.flipkart.com/search?q={query}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to retrieve data"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first product link
    product_link = soup.find('a', href=re.compile(r'/p/itm'))
    if product_link:
        match = re.search(r'pid=([A-Z0-9]+)', product_link['href'])
        if match:
            return match.group(1)  # Extract the PID

    return "PID not found"

def fetch(id):
    str_id=str(id).upper()
    
    url = "https://real-time-flipkart-api.p.rapidapi.com/product-details"

    querystring = {"pid" : str_id,"pincode" : "522237"}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "real-time-flipkart-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    json_response=response.json()
    #print(json_response['highlights'])
    desc=json_response.get("description")
    print(desc)


def main():
    id=get_flipkart_pid("cmf-nothing-phone-1-black-128-gb")
    fetch(id)


if __name__=='__main__':
    main()
