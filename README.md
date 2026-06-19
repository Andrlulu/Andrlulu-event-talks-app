# 📋 BigQuery Release Notes Viewer

A lightweight **Python Flask** web application that fetches the latest **Google BigQuery release notes** from the official Atom/XML feed and displays them in a clean, responsive, and beautiful dashboard. It comes packed with user-friendly utilities like copy-to-clipboard, CSV exports, search/tag filtering, and a Twitter draft editor.

---

## 🚀 Features

- 🔄 **Live feed** — pulls release notes directly from Google's public Atom feed.
- ⚡ **Refresh on demand** — click Refresh anytime; a shimmering **Skeleton Loader** screen displays while data fetches.
- 🖥️ **Rich content rendering** — notes are rendered as formatted HTML with customized styles for headings, lists, inline code, and code blocks (`<pre>`).
- 🌙 **Dark/Light Mode** — a custom toggle switch with seamless HSL color scheme transitions that persists your preference via `localStorage`.
- 🔍 **Live Search** — dynamic, instant client-side keyword search to quickly locate specific updates (e.g. "JSON", "nested").
- 🏷️ **Category Tags** — quick-filter updates by type: **Features**, **Changes**, **Fixes**, and **Deprecated**.
- ⬇️ **Export to CSV** — export the active, filtered list of release notes to a CSV file in one click.
- 📋 **Copy to Clipboard** — copy clean, plaintext summaries of release notes for quick sharing.
- 🐦 **𝕏 Tweet review modal** — draft and edit your tweets in a custom modal container featuring character count limit checks (up to 280 chars) before posting to the simulated Twitter endpoint.
- 🔗 **View on Google Cloud** — direct link to the official release notes page for each date.

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Server** | Python 3, Flask 3.x |
| **HTTP client** | `requests` library |
| **XML parsing** | `xml.etree.ElementTree` (built-in) |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript (ES2017+), Google Fonts (Inter, Fira Code) |
| **Data source** | [Google BigQuery Atom feed](https://docs.cloud.google.com/feeds/bigquery-release-notes.xml) |

---

## 📁 Project Structure

```
.
├── app.py                  # Flask server — routes, XML parsing, tweet endpoint
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignores venv, __pycache__, .env, etc.
└── templates/
    └── index.html          # Frontend — HTML structure, CSS styling, JavaScript
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

### 1. Clone the repository

```bash
git clone https://github.com/Andrlulu/Andrlulu-event-talks-app.git
cd Andrlulu-event-talks-app
```

### 2. (Recommended) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the development server

```bash
python app.py
```

Or using the Flask CLI:

```bash
flask --app app.py run --host=0.0.0.0 --port=5001
```

### 5. Open in your browser

```
http://127.0.0.1:5001
```

---

## 🖥️ How It Works

```
Browser                    Flask Server              Google Cloud
   │                           │                          │
   │  GET /                    │                          │
   │ ─────────────────────── ► │  serve index.html        │
   │ ◄─────────────────────── │                          │
   │                           │                          │
   │  GET /api/notes           │                          │
   │ ─────────────────────── ► │  requests.get(feed_url)  │
   │                           │ ──────────────────────── ►│
   │                           │  200 OK (Atom XML)       │
   │                           │ ◄────────────────────────│
   │                           │  parse XML → JSON        │
   │  200 OK (JSON)            │                          │
   │ ◄─────────────────────── │                          │
   │  render note cards        │                          │
   │                           │                          │
   │  POST /api/tweet          │                          │
   │ ─────────────────────── ► │  post_tweet() [simulated]│
   │  200 OK                   │                          │
   │ ◄─────────────────────── │                          │
```

---

## 🔌 API Reference

### `GET /`
Returns the main HTML page.

---

### `GET /api/notes`
Fetches and returns all BigQuery release notes.

**Response**
```json
{
  "status": "ok",
  "notes": [
    {
      "title":   "June 17, 2026",
      "link":    "https://docs.cloud.google.com/bigquery/docs/release-notes#June_17_2026",
      "updated": "2026-06-17T00:00:00-07:00",
      "summary": "<h3>Feature</h3><p>You can enable autonomous embedding...</p>"
    }
  ]
}
```

---

### `POST /api/tweet`
Sends a tweet for a selected note (currently simulated).

**Request body**
```json
{ "content": "BigQuery Update: June 17, 2026\n\nFeature: You can enable autonomous embedding...\n\nhttps://docs.cloud.google.com/bigquery/docs/release-notes#June_17_2026" }
```

**Success response**
```json
{ "status": "ok" }
```

**Error response**
```json
{ "status": "error", "error": "No content provided" }
```

---

## 🐦 Adding Real Twitter / X Integration

The `post_tweet()` function in `app.py` is a placeholder. To make tweets real:

1. Install `tweepy`:
   ```bash
   pip install tweepy
   ```

2. Add your Twitter API credentials to a `.env` file:
   ```env
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_SECRET=your_access_secret
   ```

3. Replace `post_tweet()` in `app.py`:
   ```python
   import tweepy, os

   def post_tweet(content: str) -> bool:
       client = tweepy.Client(
           consumer_key=os.getenv('TWITTER_API_KEY'),
           consumer_secret=os.getenv('TWITTER_API_SECRET'),
           access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
           access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
       )
       client.create_tweet(text=content[:280])
       return True
   ```

---

## 🚀 Deployment

For production, use a WSGI server instead of Flask's built-in dev server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

You can also containerise with Docker and deploy to **Google Cloud Run**, **Heroku**, or any container platform.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- Release notes data sourced from the [Google BigQuery documentation](https://cloud.google.com/bigquery/docs/release-notes).
- Built with [Flask](https://flask.palletsprojects.com/).
