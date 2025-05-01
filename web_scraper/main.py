from fastapi import FastAPI, Request
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.post("/scrape")
async def scrape(request: Request):
    body = await request.json()
    url = body.get("url")
    headers = {"User-Agent": "MCP-Agent/1.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return {
        "url": url,
        "title": soup.title.string if soup.title else "No title",
        "text": soup.get_text()
    }
