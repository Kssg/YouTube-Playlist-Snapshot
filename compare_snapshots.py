import json
from datetime import datetime
import sys, os
import select_file

path = './put'

snapshot_1 = {}
snapshot_2 = {}

input1, input2 = select_file.select_file_in_category(path)

with open(os.path.join(path, input1), 'r', encoding='utf-8') as file:
    snapshot_1 = json.load(file)
with open(os.path.join(path, input2), 'r', encoding='utf-8') as file:
    snapshot_2 = json.load(file)

if snapshot_1['playlistId'] != snapshot_2['playlistId']:
    sys.exit("Snapshot's don't have the same playlist id.") 

snapshot_1_time = datetime.fromisoformat(snapshot_1['timeTaken'])
snapshot_2_time = datetime.fromisoformat(snapshot_2['timeTaken'])

newer_snapshot = {}
older_snapshot = {}

if snapshot_1_time > snapshot_2_time:
    newer_snapshot = snapshot_1
    older_snapshot = snapshot_2
else:
    newer_snapshot = snapshot_2
    older_snapshot = snapshot_1

def exclusive_to_list1(list1, list2):
    exclusive_to_list1 = []
    for item in list1:
        is_in_list2 = False
        for item2 in list2:
            if item["videoId"] == item2["videoId"] and item["title"] == item2["title"]:
                is_in_list2 = True
                break
        if not is_in_list2:
            exclusive_to_list1.append(item)
    return exclusive_to_list1
# 看list1的東西有無在list2裡，有就沒事換下一個，沒有就記起來
exclusive_to_older = exclusive_to_list1(older_snapshot['videos'], newer_snapshot['videos'])
exclusive_to_newer = exclusive_to_list1(newer_snapshot['videos'], older_snapshot['videos'])

print()
# 舊的list有而新的list沒有
if len(exclusive_to_older) > 0:
    print('Videos exclusive to older snapshot:')
    for video in exclusive_to_older:
        print(f"Video: {video['title']}, YT Channel: {video['channelTitle']}, Position: {video['position']}, Video ID: {video['videoId']}")
else:
    print('No videos exclusive to the older snapshot.')
print()
if len(exclusive_to_newer) > 0:
    print('Videos exclusive to newer snapshot:')
    for video in exclusive_to_newer:
        print(f"Video: {video['title']}, YT Channel: {video['channelTitle']}, Position: {video['position']}, Video ID: {video['videoId']}")
else:
    print('No videos exclusive to the newer snapshot.')
print()