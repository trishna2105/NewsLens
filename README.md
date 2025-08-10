# NewsLens

**AI-powered news search and summarization app** built with **FastAPI**, **BART transformer model**, and **GNews API**.  
Fetches and summarizes news articles based on category and date.

---

## Features
- Search news articles by **keyword**, **category**, and **date**
- Summarizes articles using `facebook/bart-large-cnn`
- Category filtering: Sports, Politics, Technology, etc.
- Clean, responsive UI (HTML + CSS)
- Fast backend with FastAPI
- Workflow:
  <p align="center">
  <img src="https://github.com/user-attachments/assets/477f8168-5193-4ac1-a699-3191e32e6989" alt="Workflow" width="700" />
  </p>


---

## Tech Stack
**Backend:** FastAPI, Transformers, Newspaper3k, Requests  
**Frontend:** HTML, CSS, JavaScript  
**API:** GNews API  
**Model:** facebook/bart-large-cnn

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/newslens.git
cd newslens

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn media:app --reload --port 8002
