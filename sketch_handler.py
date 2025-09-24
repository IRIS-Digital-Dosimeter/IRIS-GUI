import sys
import os
import arduino_helper as ah
import tomllib
import requests
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path

LOCKFILE_PATH = Path(__file__).parent / "iris_sketches" / "sketches.lock"
load_dotenv()
GH_TOKEN = os.getenv("GITHUB_PAT")

def get_sketch(name, version="latest", owner="IRIS-Digital-Dosimeter", repo="IRIS-Project", branch: str = None):
    try:
        lock = load_lockfile(LOCKFILE_PATH)
    except Exception:
        raise Exception("Malformed TOML lockfile")

    sketch_info = lock.get(name)
    if not sketch_info:
        raise SketchHandlerException("Sketch not in lock file.")

    print("sketch info below: ")
    pprint(sketch_info)
    print()

    if version == "latest":
        if not online():
            raise RuntimeError("Cannot fetch 'latest' while offline.")
        
        commit = get_latest_commit(sketch_info["remote_path"], owner, repo, branch)[0]

        # pprint(commit)
        return commit['commit']['tree']['sha'][0]

    else:
        raise NotImplementedError()
        commit = version  # explicit commit hash

    

    # # Not in lockfile → fetch
    # if not sketch_info or sketch_info["commit"] != commit:
    #     if not online() and not os.path.exists(f"./downloads/{name}"):
    #         raise RuntimeError(f"{name}@{commit} not available offline.")
    #     download_sketch(name, commit)
    #     lock[name] = record_metadata(name, commit)
    #     save_lockfile(lock)
    # else:
    #     print(f"Using cached {name}@{commit}")

    # compile_and_upload(lock[name]["local_path"])

    
def load_lockfile(p: Path) -> dict | None:
    with open(p.as_posix(), "rb") as f:
        data = tomllib.load(f)
        return data

def online(timeout=2) -> bool:
    try:
        r = requests.head("https://api.github.com", timeout=timeout)
        return r.status_code < 500
    except requests.RequestException:
        return False
    
def get_latest_commit(remote_path: str, owner: str, repo: str, branch: str = None) -> str | None:
    # return None

    req_params = {
        "path": remote_path,
        "pages": 1,
        "per_page": 1,
    }
    if branch:
        req_params['sha'] = branch
        
    try:
        r = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/commits",
            data=req_params,
            headers= {
                "Authorization": "Bearer: {GH_TOKEN}",
                "accept": "application/vnd.github+json",
            }
        )
        return r.json()
    except requests.RequestException:
        return None


class SketchHandlerException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

if __name__ == "__main__":
    
    print('running main')
    
    arduino = ah.ExtendoArduino(
        additional_urls=[
            'https://adafruit.github.io/arduino-board-index/package_adafruit_index.json'
        ]
    )
    
    # load_lockfile(LOCKFILE_PATH)
    print(f"github reachable? {online()}")
    print()
    commits = get_sketch("M4", branch="cleanup")
    print(len(commits))
    print()
    print(commits)
    
    # for commit in commits:
        # pprint(commit['commit'])
        # print('----')
        # print(commit['commit']['message'])
        # print()
        # print(commit['commit']['tree']['sha'])