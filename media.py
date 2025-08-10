from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from datetime import datetime
from transformers import pipeline
from newspaper import Article
import uvicorn
from urllib.parse import quote_plus

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# API Key
GNEWS_API_KEY = "88da545f6ccf328eea4c709e35c66fb9"
GNEWS_API_URL = "https://gnews.io/api/v4/search"

CATEGORY_KEYWORDS = {
    "sports": ["match", "tournament", "game", "league", "player", "coach", "goal", "score"],
    "politics": ["election", "government", "policy", "minister", "bill", "parliament", "law"],
    "technology": ["AI", "blockchain", "software", "gadget", "innovation", "cybersecurity"],
    "business": ["market", "economy", "finance", "stocks", "trade", "investment"],
    "health": ["virus", "disease", "hospital", "vaccine", "medical", "doctor"],
    "entertainment": ["movie", "celebrity", "film", "music", "TV", "actor", "director"]
}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/fetch_news", response_class=HTMLResponse)
def fetch_news(request: Request, query: str = Form(...), date: str = Form(...), category: str = Form("general")):
    query = query.strip()
    if not query:
        return "<h3>Error: Query cannot be empty.</h3>"

    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

    params = {
        "q": query,
        "from": formatted_date,
        "to": formatted_date,
        "lang": "en",
        "token": GNEWS_API_KEY,
        "max": 10
    }

    response = requests.get(GNEWS_API_URL, params=params)
    if response.status_code != 200:
        return f"<h3>Error fetching news: {response.text}</h3>"

    articles = response.json().get("articles", [])
    if not articles:
        return "<h3>No articles found for this date and query.</h3>"

    category_keywords = CATEGORY_KEYWORDS.get(category, [])
    filtered_articles = [
        a for a in articles
        if category == "general" or any(kw.lower() in (a.get("title", "") + a.get("description", "")).lower() for kw in category_keywords)
    ]

    if not filtered_articles:
        return f"<h3>No relevant news found in the selected category ({category}).</h3>"

    articles_html = ""
    for article in filtered_articles:
        try:
            url = article["url"]
            news_article = Article(url)
            news_article.download()
            news_article.parse()
            content = news_article.text[:2000]

            if not content:
                continue

            if len(content.split()) < 30:
                summary = content
            else:
                input_length = len(content.split())
                dynamic_max_length = min(200, int(input_length * 0.6))
                dynamic_min_length = max(30, int(dynamic_max_length * 0.5))
                summary = summarizer(content, max_length=dynamic_max_length, min_length=dynamic_min_length, do_sample=False)[0]['summary_text']

            articles_html += f"""
            <li>
                <a href="{url}" target="_blank">{article['title']}</a>
                <p><strong>Summary:</strong> {summary}</p>
            </li>
            """
        except Exception as e:
            articles_html += f"""
            <li>
                <a href="{article['url']}" target="_blank">{article['title']}</a>
                <p><strong>Error summarizing article:</strong> {str(e)}</p>
            </li>
            """

    return f"""
    <html>
        <head><title>NewsLens Results</title></head>
        <body>
            <h2>Search Results for '{query}' on {date} ({category.capitalize()})</h2>
            <ul>{articles_html}</ul>
            <a href="/">Search Again</a>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
