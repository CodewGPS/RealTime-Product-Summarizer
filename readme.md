# 🛒 Flipkart Q&A Genie

**Smart Product Assistant powered by AI**

A Streamlit-based web application that lets you search for any product on Flipkart and ask intelligent questions about it using Google's Gemini AI. Simply enter a product name, and the app will fetch detailed product information and provide instant answers to your queries in natural language.


## ✨ Features

- **🔍 Smart Product Search**: Search for products by name with automatic Flipkart integration
- **📊 Comprehensive Product Details**: View images, specifications, reviews, pricing, and features
- **🤖 AI-Powered Q&A**: Ask natural language questions about any product using Gemini AI
- **💬 Interactive Chat Interface**: Maintain conversation history with the AI assistant
- **📱 Responsive Design**: Clean, modern UI that works across all devices
- **⚡ Real-time Data**: Fetch live product information directly from Flipkart

## 🚀 Demo

Try asking questions like:
- "What are the key features of this laptop?"
- "Is this product good for gaming?"
- "What do customers say about the battery life?"
- "How does this compare to similar products?"

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.0 Flash
- **Product Data**: RapidAPI Flipkart API
- **Web Scraping**: BeautifulSoup4
- **HTTP Requests**: Requests library
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8 or higher
- RapidAPI account with Flipkart API access
- Google AI Studio account for Gemini API

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/flipkart-qna-genie.git
   cd flipkart-qna-genie
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create requirements.txt** (if not exists)
   ```txt
   streamlit
   requests
   python-dotenv
   beautifulsoup4
   google-generativeai
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   x-rapidapi-key=your_rapidapi_key_here
   google-api-key=your_google_api_key_here
   ```

## 🔑 API Keys Setup

### RapidAPI Key
1. Visit [RapidAPI](https://rapidapi.com/)
2. Sign up/Login to your account
3. Subscribe to the [Real Time Flipkart API](https://rapidapi.com/opendatapointcom/api/real-time-flipkart-api)
4. Copy your API key from the dashboard

### Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the generated API key

### Environment Variables
Add these keys to your `.env` file:
```env
x-rapidapi-key=your_rapidapi_key_from_rapidapi
google-api-key=your_google_gemini_api_key
```

## 🚀 Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in your terminal

3. **Start using the app**
   - Enter a product name (e.g., "Apple MacBook Air M4")
   - Click "Search" to fetch product details
   - Ask questions about the product in the chat interface

## 📁 Project Structure

```
flipkart-qna-genie/
├── app.py                 # Main Streamlit application
├── .env                   # Environment variables (create this)
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Git ignore file
```

## 🎯 Usage Examples

### Search for Products
```
Search Query: "Samsung Galaxy S23"
Result: Fetches product details, images, specifications, and reviews
```

### Ask Questions
```
Question: "What is the camera quality like?"
AI Response: Based on the product specifications and reviews, the Samsung Galaxy S23 features a triple camera setup with...
```

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them publicly
- The app includes rate limiting considerations for API calls

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web app framework
- **Google Gemini** - For providing powerful AI capabilities
- **RapidAPI** - For Flipkart product data access
- **Flipkart** - For the product information
- **BeautifulSoup** - For web scraping capabilities

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Review the [Gemini API documentation](https://ai.google.dev/docs)

## 🌟 Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

**Made with ❤️ using Streamlit and Gemini AI**
