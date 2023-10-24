import requests
from bs4 import BeautifulSoup
from collections import defaultdict

sreddit_in_cat = defaultdict(list)

for i in range(1, 5):
    url = f"https://www.reddit.com/best/communities/{i}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        parent_div = soup.find("div", class_="community-list")

        if parent_div:
            subreddit = parent_div.find_all("div", recursive=False)
            for div in subreddit:
                # print(div.get("id"))
                text_div = div.find_all("div")[0]
                sreddit_name = text_div.find_all("a")[0].text.strip()
                category = text_div.find_all("h6")[0].text.strip()
                sreddit_in_cat[category].append(sreddit_name[2:])
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

for k, v in sreddit_in_cat.items():
    print(f"{k} {v}")
