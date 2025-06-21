import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import google.generativeai as genai
import json


API_KEY = st.secrets["x-rapidapi-key"]
GOOGLE_API_KEY = st.secrets["google-api-key"]


st.set_page_config(
    page_title="Flipkart Product Q&A",
    page_icon="🛒",
    layout="wide",
)


st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .product-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #e1f5fe;
        margin-left: 40px;
    }
    .assistant-message {
        background-color: #f0f4c3;
        margin-right: 40px;
    }
</style>
""", unsafe_allow_html=True)

def get_flipkart_pid(product_name):
    product_name = product_name.lower()
    query = product_name.replace(' ', '-')
    url = f'https://www.flipkart.com/search?q={query}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    with st.spinner('Searching for product...'):
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

    with st.spinner('Fetching product details...'):
        response = requests.get(url, headers=headers, params=querystring)
        try:
            return response.json(), None
        except Exception as e:
            return None, f"Error: {str(e)}"

def frame_context(json_response):
    context = f"""
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
    return context

def ask_gemini(context, question):
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        prompt = f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"Error: {str(e)}"


st.title("🛒 Flipkart Product Q&A")
st.subheader("Search for a product and ask questions about it")


if "product_data" not in st.session_state:
    st.session_state.product_data = None
if "context" not in st.session_state:
    st.session_state.context = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        product_name = st.text_input("Enter product name", placeholder="e.g., Apple Macbook Air M4")
    with col1:
        search_button = st.button("Search", type="primary")

    if search_button and product_name:
        pid, error = get_flipkart_pid(product_name)
        if error:
            st.error(error)
        elif pid:
            st.success(f"Found product with ID: {pid}")
            json_data, error = fetch_product_details(pid)
            if error:
                st.error(error)
            elif json_data:
                st.session_state.product_data = json_data
                st.session_state.context = frame_context(json_data)
                st.session_state.chat_history = []  
                st.rerun()


if st.session_state.product_data:
    with st.container():
        st.markdown("## Product Information")
        data = st.session_state.product_data
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if "images" in data:
                st.image(data["images"][0], width=250)
            else:
                st.info("No image available")
        
        with col2:
            st.markdown(f"### {data.get('title', 'Unknown Product')}")
            st.markdown(f"**Brand:** {data.get('brand', 'N/A')}")
            
            col_price1, col_price2 = st.columns(2)
            with col_price1:
                st.markdown(f"**MRP:** ₹{data.get('mrp', 'N/A')}")
            with col_price2:
                st.markdown(f"**Price:** ₹{data.get('price', 'N/A')}")
            
            if "rating" in data:
                st.markdown(f"**Rating:** {data.get('rating', 'N/A')} ⭐")
            
            st.markdown("### Features:")
            if "highlights" in data and data["highlights"]:
                for feature in data["highlights"]:
                    st.markdown(f"- {feature}")
            else:
                st.info("No feature information available")

    # Q&A Section
    st.markdown("## Ask about this product")
    user_question = st.text_input("Your question", placeholder="Ask anything about this product...")
    
    if st.button("Ask", type="primary"):
        if user_question:
            # Add user question to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            # Get response from Gemini
            answer, error = ask_gemini(st.session_state.context, user_question)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "content": f"Sorry, I encountered an error: {error}"})
            else:
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
            # Clear the input box
            st.rerun()

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### Conversation")
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <b>You:</b> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <b>Assistant:</b> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("👆 Search for a product to get started")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit & Gemini AI")
