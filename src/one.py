import json
import sys
import subprocess
from pathlib import Path

def run_one(name):
    if not name:
        print("Please enter the playlist name!!")
        sys.exit(1)

    base_path = Path(__file__).parent.parent
    json_path = base_path / 'data' / 'list.json'
    exfile = base_path / 'src' / 'take_snapshot.py'

    with open(json_path, 'r', encoding='utf-8') as file:
        lists = json.load(file)

    selected_list = None
    for lst in lists:
        if lst['title'] == name:
            selected_list = lst
            break

    else:
        print("Playlist not found, please check again!")
        sys.exit(1)
    
    print()

    try:
        subprocess.run([sys.executable, str(exfile), selected_list['id']], check=True)
        print(f"✅ Saved list: {selected_list['title']}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to save list: {selected_list['title']} (id={selected_list['id']})")
        print(f"    ↳ Error: {e}")
    
    print("\n=== Task finished. ===")

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_one(arg)