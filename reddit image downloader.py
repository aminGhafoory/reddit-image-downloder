# reddit photo link downloader

import requests
import json
from argparse import ArgumentParser

# ===============Argument parsing===================
parser = ArgumentParser(description="Process subreddit name and filters.")

parser.add_argument(
    "-sub",
    help="name of subreddit example: DataHoarder",
    required=True,
    type=str,
)

parser.add_argument(
    "-sort",
    help="how to sort \n options: <hot|new|rising|top>",
    required=False,
    type=str,
)

parser.add_argument(
    "-top",
    help="top_time \n options: <all|year|month|week|day>",
    required=False,
    type=str,
)

args = vars(parser.parse_args())
args = parser.parse_args()

sort = args.sort
subreddit = args.sub
top_time = args.top

if sort == None:
    sort = "hot"
if top_time == None:
    top_time = "all"

# ==============================Scraper=============================
url = f"https://www.reddit.com/r/{subreddit}/{sort}/.json?raw_json=1&t={top_time}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Connection": "keep-alive",
}


# ===================main function=====================
def main(url: str, headers: dict) -> list:

    r = requests.get(url, headers=headers)
    json_object = json.loads(r.text)
    after = json_object["data"]["after"]
    image_links = []
    number_of_links = 0
    while after != None:
        json_object = json.loads(r.text)
        after = json_object["data"]["after"]
        childs = json_object["data"]["children"]

        for child in childs:
            try:
                image_link = child["data"]["url_overridden_by_dest"]
                image_links.append(image_link)
            except:
                pass

        url = f"https://www.reddit.com/r/{subreddit}/{sort}/.json?raw_json=1&t={top_time}&after={after}"
        r = requests.get(url, headers=headers)
        save_in_text_file(image_links)
        number_of_links += len(image_links)
        image_links.clear()
        print(f"Total number of links == {number_of_links}")


# ==============write in txt file function================
def save_in_text_file(output_list: list) -> None:
    with open("output_file.txt", "a") as f:
        for i in output_list:
            f.write(f"{i}\n")


if __name__ == "__main__":
    main(url, headers)
