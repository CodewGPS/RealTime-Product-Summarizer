from fastapi import FastAPI, Query
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import re
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

API_KEY = os.getenv("x-rapidapi-key")
GOOGLE_API_KEY = os.getenv("google-api-key")

app = FastAPI()

# Optional CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QARequest(BaseModel):
    product_name: str
    question: str


def get_flipkart_pid(product_name):
    product_name = product_name.lower()
    query = product_name.replace(' ', '-')
    url = f'https://www.flipkart.com/search?q={query}'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, "Failed to retrieve data"
    soup = BeautifulSoup(response.text, 'html.parser')
    product_link = soup.find('a', href=re.compile(r'/p/itm'))
    if product_link:
        match = re.search(r'pid=([A-Z0-9]+)', product_link['href'])
        if match:
            return match.group(1), None
    return None, "Product not found"


def fetch_product_details(pid):
    str_id = str(pid).upper()
    url = "https://real-time-flipkart-api.p.rapidapi.com/product-details"
    querystring = {"pid": str_id, "pincode": "522237"}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "real-time-flipkart-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    try:
        return response.json(), None
    except Exception as e:
        return None, f"Error: {str(e)}"


def frame_context(json_response):
    return f"""
    Product Name: {json_response.get('title', 'N/A')}
    Brand: {json_response.get('brand', 'N/A')}
    url : {json_response.get('url','N/A')}
    variants : {json_response.get('variants','N/A')}
    Specifications : {json_response.get('specifications','N/A')}
    FAQ : {json_response.get('qna','N/A')}
    MRP: {json_response.get('mrp', 'N/A')}
    Discounted Price: {json_response.get('price', 'N/A')}
    Features: {json_response.get('features', 'N/A')}
    Reviews: {json_response.get('reviews', 'N/A')}
    """


def ask_gemini(context, question):
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        prompt = f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"Error: {str(e)}"


@app.get("/")
def root():
    return {"message": "Flipkart Product Q&A API is running."}


@app.post("/qa")
def product_qa(req: QARequest):
    pid, err = get_flipkart_pid(req.product_name)
    if err:
        return {"error": err}
    json_data, err = fetch_product_details(pid)
    if err:
        return {"error": err}
    context = frame_context(json_data)
    answer, err = ask_gemini(context, req.question)
    if err:
        return {"error": err}
    return {
        "product_id": pid,
        "product_title": json_data.get("title", "N/A"),
        "question": req.question,
        "answer": answer
    }
