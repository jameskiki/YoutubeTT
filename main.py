import os
import re
from datetime import timedelta

from googleapiclient.discovery import build
from urllib.error import HTTPError
from api_key import api_key

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.videos().list(
    part="snippet",
    id='coZbOM6E47I'        # example url; https://www.youtube.com/watch?v=coZbOM6E47I starting from = is the id
)
try:
    response = request.execute()
except OSError as e:
    print(e)
    exit(1)

print(response)


