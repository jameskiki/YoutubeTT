
from googleapiclient.discovery import build
from api_key import api_key

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(
        part= 'statistics',
        forUsername='schafer5'
    )
    response = request.execute()
    print(response)


