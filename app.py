from flask import Flask, render_template, request, send_from_directory
from scraping import get_videos
import os

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
    
@app.route('/favicon.ico', methods=['GET'])
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')