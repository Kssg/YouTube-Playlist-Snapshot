import requests
import json
import sys
import re
from pathlib import Path

def santize_filename(filename: str) -> str:
    return re.sub(r'[\/\\\*\?\:"<>|]', '', filename)

base_path = Path(__file__).parent.parent
json_path = base_path / 'data' / 'key.json'
lst_path = base_path / 'data' / 'list.json'

with open(json_path, 'r', encoding='utf8') as f:
    jdata = json.load(f)
api_key = jdata['YTAPIKEY']

playlist_id = sys.argv[1]
save_path = base_path / 'snapshots'

payload = {'part': 'snippet, contentDetails', 'playlistId': playlist_id,
           'maxResults': 50, 'pageToken': None, 'key': api_key}

response = requests.get('https://youtube.googleapis.com/youtube/v3/playlistItems', params=payload)
response_json = response.json()

videos_in_playlist = []
videos_processed = 0

while True:
    for item in response_json['items']:
        item_snippet = item['snippet']
        item_content = item['contentDetails']
        if item_snippet['title'] == 'Private video' or item_snippet['title'] == 'Deleted video':
            videos_in_playlist.append({'title': item_snippet['title'],
                                   'channelTitle': None, 
                                   'position': item_snippet['position'],
                                   'videoId': item_content['videoId'],
                                   'uploadAt': None,
                                   'listAt': item_snippet['publishedAt']})
        else:
            videos_in_playlist.append({'title': item_snippet['title'],
                                   'channelTitle': item_snippet['videoOwnerChannelTitle'],
                                   'position': item_snippet['position'],
                                   'videoId': item_content['videoId'],
                                   'uploadAt': item_content['videoPublishedAt'],
                                   'listAt': item_snippet['publishedAt']})

    # 不滿50或最後一頁就什麼都沒有
    if not 'previousPageToken' in response_json and not 'nextPageToken' in response_json:
        break

    payload['pageToken'] = response_json['nextPageToken']
    response = requests.get('https://youtube.googleapis.com/youtube/v3/playlistItems', params=payload)
    response.raise_for_status()
    response_json = response.json()


    videos_processed += response_json['pageInfo']['resultsPerPage']
    #print(str(videos_processed) + ' of ' + str(response_json['pageInfo']['totalResults']) + ' videos processed.', end='\r', flush=True)

# get playlist name
playlist_payload = {'part': 'snippet', 'id': playlist_id, 'key': api_key}
playlist_response = requests.get("https://youtube.googleapis.com/youtube/v3/playlists", playlist_payload)
playlist_response.raise_for_status()
playlist_json = playlist_response.json()

playlist_name = playlist_json['items'][0]['snippet']['title']
playlist_name = santize_filename(playlist_name)
snapshot_file_name = f"{save_path}/{playlist_name}.json"

with open(snapshot_file_name, 'w', encoding='utf-8') as file:
    file.write(json.dumps({'playlistId': playlist_id, 'videos': videos_in_playlist}, ensure_ascii=False, indent=4))