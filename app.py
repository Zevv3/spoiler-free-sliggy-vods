from flask import Flask, render_template, request
from scraping import get_videos

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
        video_data = {"use Refresh button to view VODS. Note that this will open a chrome window, don't look at it to avoid spoilers": "data"}
        processed_video_data = {}
        for teams, links in video_data.items():
            processed_links = [(i+1, link) for i, link in enumerate(links)]
            processed_video_data[teams] = processed_links
        return render_template('index.html', video_data=processed_video_data)


@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        video_data = get_videos()
        return render_template('index.html', video_data=video_data)
