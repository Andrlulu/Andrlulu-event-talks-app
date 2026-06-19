from flask import Flask, render_template, jsonify, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

BIGQUERY_FEED_URL = 'https://docs.cloud.google.com/feeds/bigquery-release-notes.xml'

def fetch_release_notes():
    """Fetch and parse the BigQuery release notes Atom feed.
    Returns a list of dicts with title, link, updated, and summary.
    """
    resp = requests.get(BIGQUERY_FEED_URL, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    notes = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text if entry.find('atom:title', ns) is not None else ''
        link_elem = entry.find('atom:link', ns)
        link = link_elem.attrib.get('href') if link_elem is not None else ''
        updated = entry.find('atom:updated', ns).text if entry.find('atom:updated', ns) is not None else ''
        # Try <atom:summary> first; if missing, fall back to <atom:content>
        summary_elem = entry.find('atom:summary', ns)
        if summary_elem is not None and summary_elem.text:
            summary = summary_elem.text
        else:
            content_elem = entry.find('atom:content', ns)
            summary = content_elem.text if content_elem is not None else ''
        notes.append({
            'title': title,
            'link': link,
            'updated': updated,
            'summary': summary
        })
    return notes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes')
def api_notes():
    try:
        notes = fetch_release_notes()
        return jsonify({'status': 'ok', 'notes': notes})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

# Placeholder tweet function – replace with real Twitter API integration.
def post_tweet(content: str) -> bool:
    print('Tweeting:', content)
    return True

@app.route('/api/tweet', methods=['POST'])
def api_tweet():
    data = request.get_json(silent=True) or {}
    content = data.get('content', '')
    if not content:
        return jsonify({'status': 'error', 'error': 'No content provided'}), 400
    success = post_tweet(content)
    if success:
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'error', 'error': 'Failed to post tweet'}), 500

if __name__ == '__main__':
    # Development server – use a production WSGI server for deployment.
    app.run(host='0.0.0.0', port=5000, debug=True)
