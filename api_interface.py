
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi,_errors

import re
from urllib.error import HTTPError

from api_key import api_key

youtube = build('youtube', 'v3', developerKey=api_key)


# example url; https://www.youtube.com/watch?v=coZbOM6E47I starting from 'v=' is the id = coZbOM6E47I
def get_video_by_url(url):
    id = re.search('v=(\w+)&?', url)
    id = id.group(1)
    print(id)
    snippet = None
    details = None
    try:
        req_snipp = youtube.videos().list(
            part="snippet",
            id=id
        )
        snippet = req_snipp.execute()

        req_detail = youtube.videos().list(
            part="contentDetails",
            id=id
        )
        details = req_detail.execute()
    except HTTPError as e:
        print('HTTPERROR')
        print(e)
        pass
    return id, snippet, details


def get_transcript_by_id(id):
    try:
        return YouTubeTranscriptApi.get_transcript(id)
    except _errors.TranscriptsDisabled as e:
        print('cc disabled')
        return None
