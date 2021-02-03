
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

from urllib.error import HTTPError

from api_key import api_key

youtube = build('youtube', 'v3', developerKey=api_key)


# example url; https://www.youtube.com/watch?v=coZbOM6E47I starting from 'v=' is the id = coZbOM6E47I
def get_video_by_url(url):
    id = url.split('=')
    print(id)
    request = None
    details = None
    try:
        req_snipp = youtube.videos().list(
            part="snippet",
            id=id[1].strip('&t')
        )
        snippet = req_snipp.execute()

        req_detail = youtube.videos().list(
            part="contentDetails",
            id=id[1].strip('&t')
        )
        details = req_detail.execute()
    except IndexError as e:
        print('Index out of bounds')
        print(e)
        pass
    except HTTPError as e:
        print('HTTPERROR')
        print(e)
        pass
    return snippet, details


def get_transcript_by_id(id):
    return YouTubeTranscriptApi.get_transcript(id)
