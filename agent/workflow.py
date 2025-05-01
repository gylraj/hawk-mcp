import os
from dotenv import load_dotenv
from openai import OpenAI
from requests import post

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text, company_name):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful business analyst."},
            {"role": "user", "content": f"Summarize this content about {company_name}:\n\n{text}"}
        ],
        temperature=0.5,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

def perform_account_research(company_name: str):
    print(f"🔍 Researching {company_name}...")

    # Call MCP Web Scraper
    web = post("http://localhost:8001/scrape", json={"url": f"https://en.wikipedia.org/wiki/{company_name}"}).json()

    # Generate Summary via OpenAI
    summary = summarize_text(web.get("text", "")[:2000], company_name)

    res = post("http://localhost:8002/drive-upload", json={
        "filename": f"{company_name}_summary.txt",
        "content": summary
    })
    print("Upload raw response:", res.status_code, res.text)
    upload_response = res.json()

    # Call MCP Google Drive Search
    drive = post("http://localhost:8002/drive-search", json={"query": company_name}).json()

    return {
        "summary": summary,
        "uploaded_summary": upload_response,
        "drive_files": drive.get("results", [])
    }

if __name__ == "__main__":
    from pprint import pprint
    result = perform_account_research("OpenAI")
    pprint(result)
