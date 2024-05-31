# youtube_transcripts.py

from dotenv import load_dotenv
from googleapiclient.discovery import build
import os

load_dotenv()

def get_youtube_transcripts(video_ids):
    api_key = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    transcripts = []
    for video_id in video_ids:
        response = youtube.captions().list(part='snippet', videoId=video_id).execute()
        captions = response.get('items', [])
        if not captions:
            continue

        caption_id = captions[0]['id']
        subtitle = youtube.captions().download(id=caption_id, tfmt='srt').execute()
        transcripts.append(subtitle.decode('utf-8'))

    return transcripts
