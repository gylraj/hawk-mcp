from fastapi import FastAPI, Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
import base64

app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.file']

@app.post("/drive-search")
async def drive_search(request: Request):
    body = await request.json()
    query = body.get("query")

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("drive", "v3", credentials=creds)

    results = service.files().list(q=f"name contains '{query}'",
                                   pageSize=5,
                                   fields="files(id, name, webViewLink)").execute()
    files = results.get("files", [])
    return {"results": files}


@app.post("/drive-upload")
async def drive_upload(request: Request):
    body = await request.json()
    filename = body.get("filename")
    content = body.get("content")

    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        service = build("drive", "v3", credentials=creds)

        media_body = MediaInMemoryUpload(content.encode(), mimetype="text/plain")
        file_metadata = {
            "name": filename
        }

        file = service.files().create(
            body=file_metadata,
            media_body=media_body,
            fields="id, name, webViewLink"
        ).execute()

        return {
            "id": file["id"],
            "name": file["name"],
            "link": file["webViewLink"]
        }

    except Exception as e:
        return {"error": str(e)}
