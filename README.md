NewsLens
AI-powered news search and summarization app built with FastAPI, BART transformer model, and GNews API. Fetches and summarizes news articles based on category and date.

Features
Search news articles by keyword, category, and date

Summarizes articles using facebook/bart-large-cnn

Category filtering (Sports, Politics, Technology, etc.)

Clean, responsive UI (HTML + CSS)

Fast backend with FastAPI

Tech Stack
Backend: FastAPI, Transformers, Newspaper3k, Requests

Frontend: HTML, CSS, JavaScript

API: GNews API

Model: facebook/bart-large-cnn

Installation
bash
Copy
Edit
# Clone the repository
git clone https://github.com/yourusername/newslens.git
cd newslens

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn media:app --reload --port 8002
Usage
Open http://127.0.0.1:8002 in your browser

Enter a query, select date and category, and click Search News

Read AI-generated summaries instantly

