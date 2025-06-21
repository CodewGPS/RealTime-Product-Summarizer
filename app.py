from fastapi import FastAPI, Query
from dotenv import load_dotenv
import os, requests, re, json
from bs4 import BeautifulSoup
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("x-rapidapi-key")
GOOGLE_API_KEY = os.getenv("google-api-key")

app = FastAPI()

def get_flipkart_pid(product_name):
    product_name = product_name.lower()
    query = product_name.replace(' ', '-')
    url = f'https://www.flipkart.com/search?q={query}'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    product_link = soup.find('a', href=re.compile(r'/p/itm'))
    if product_link:
        match = re.search(r'pid=([A-Z0-9]+)', product_link['href'])
        if match:
            return match.group(1)
    return None

def fetch(id):
    url = "https://real-time-flipkart-api.p.rapidapi.com/product-details"
    querystring = {"pid": id.upper(), "pincode": "522237"}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "real-time-flipkart-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def frame_context(json_response):
    return f"""
    Product Name: {json_response.get('title','N/A')}
    Brand: {json_response.get('brand','N/A')}
    MRP: {json_response.get('mrp','N/A')}
    Discounted Price: {json_response.get('price','N/A')}
    Features: {json_response.get('features','N/A')}
    Reviews: {json_response.get('reviews','N/A')}
    """

@app.get("/")
def root():
    return {"message": "Flipkart Product Query API"}

@app.get("/query/")
def ask(product_name: str, question: str):
    pid = get_flipkart_pid(product_name)
    if not pid:
        return {"error": "Product PID not found"}
    data = fetch(pid)
    context = frame_context(data)

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
    response = model.generate_content(prompt)
    return {"response": response.text}
