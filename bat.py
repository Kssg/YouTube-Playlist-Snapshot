import os
import json


with open('./LIST.json', 'r', encoding='utf-8') as file:
    lists = json.load(file)

exfile = './take_snapshot.py'
i = 1
for list in lists:
    os.system(f"python {exfile} {list['id']}")
    print(f"save list {list['title']} done.")
    i+=1
print("All tasks finished.")