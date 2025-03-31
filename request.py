import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re
import google.generativeai as genai
import json
load_dotenv()
API_KEY=os.getenv(key="x-rapidapi-key")
GOOGLE_API_KEY=os.getenv(key="google-api-key")
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
    return json_response

def frame_context(json_response):
    context=f"""
    Product Name : {json_response.get('title','N/A')}
    Brand : {json_response.get('brand','N/A')}
    MRP : {json_response.get('mrp','N/A')}
    Discounted Price : {json_response.get('price','N/A')}
    Features : {json_response.get('features','N/A')}
    Reviews : {json_response.get('reviews','N/A')}
    """
    return context


def ask_llm(context):
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model=genai.GenerativeModel(model_name= "gemini-2.0-flash")
        chat=model.start_chat(history=[])
        while True:
                question=input("You: ")
                prompt = f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
                if(question.lower()=="exit"):
                    print("Bot: Goodbye!")
                    break
                response = chat.send_message(prompt,stream=True)
                for chunk in response:
                    print(chunk.text,end="",flush=True)

    except:    
        return "Sorry, I encountered an error while processing your request."


def main():
    id=get_flipkart_pid("Apple Macbook Air M4")
    json=fetch(id)
    context=frame_context(json)
    ask_llm(context)    


if __name__=='__main__':
    main()
