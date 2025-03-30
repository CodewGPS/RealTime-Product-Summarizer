import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re
from transformers import AutoModelForCausalLM,AutoTokenizer
import json
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
    
    #data={
        #'query' : 'What do the users say about this product>?',
        #'context' :  response
    #}
    #json_data=json.dumps(data)
    #tokenizer=AutoTokenizer.from_pretrained('gpt2')
    #model=AutoModelForCausalLM.from_pretrained('gpt2')
    #input=tokenizer(response,return_tensors='pt')
    #outputs=model.generate(**input)
    #answer=tokenizer.decode(outputs[0],skip_special_tokens=True)

    #print(answer)

    print(response.json())
    json_response=response.json()
    return json_response
    #print(json_response['highlights'])
    #desc=json_response.get("description")
   # print(desc)

def query(json_response):
    brand=json_response['brand']
    title=json_response['title']
    mrp=json_response['mrp']
    price=json_response['price']
    variants=json_response['variants']
    desc=json_response['description']
    qna=json_response['qna']
    reviews=json_response['reviews']

    print(brand)
    print(title)
    print(mrp)
    print(price)
    print(variants)
    print(desc)

def main():
    id=get_flipkart_pid("Apple iPhone 15")
    json=fetch(id)
    query(json)


if __name__=='__main__':
    main()
