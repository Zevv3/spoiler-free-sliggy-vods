from flask import Flask, render_template, request, send_from_directory
from vods.scraping import get_videos
import os
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_data = {}
        video_data = get_videos()
        processed_video_data = {}
        for teams, links in video_data.items():
            processed_links = [(i+1, link) for i, link in enumerate(links)]
            processed_video_data[teams] = processed_links
        return render_template('index.html', video_data=processed_video_data)
    else:
        return render_template('index.html', video_data=None)
    
MAX_RETRIES = 3
RETRY_DELAY = 1

@app.route('/favicon.ico')
def favicon():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
        except FileNotFoundError:
            retries += 1
            print('retry')
            time.sleep(RETRY_DELAY)
    return ''