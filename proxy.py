from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")  # Store your secret as an env var
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com"

@app.route("/save", methods=["POST"])
def save_page():
    """Relay a page creation request to Notion"""
    payload = request.json
    resp = requests.post(
        f"{BASE_URL}/v1/pages",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        json=payload,
    )
    return (resp.text, resp.status_code, resp.headers.items())

@app.route("/query", methods=["POST"])
def query_db():
    """Relay a query to a Notion database"""
    db_id = request.args.get("db_id")
    payload = request.json or {}
    resp = requests.post(
        f"{BASE_URL}/v1/databases/{db_id}/query",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        json=payload,
    )
    return (resp.text, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

