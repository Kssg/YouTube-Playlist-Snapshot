import sys
import json
import subprocess
from pathlib import Path

def run_bat():
    base_path = Path(__file__).parent.parent
    json_path = base_path / 'data' / 'list.json'
    exfile = base_path / 'src' / 'take_snapshot.py'
    
    with open(json_path, 'r', encoding='utf-8') as file:
        lists = json.load(file)

    print()

    for idx, item in enumerate(lists, start=1):
        try:
            subprocess.run([sys.executable, str(exfile), item['id']], check=True)
            print(f"[{idx}] ✅ Saved list: {item['title']}")

        except subprocess.CalledProcessError as e:
            print(f"[{idx}] ❌ Failed to save list: {item['title']} (id={item['id']})")
            print(f"    ↳ Error: {e}")
    
    print("\n=== All tasks finished. ===")

if __name__ == "__main__":
    run_bat()