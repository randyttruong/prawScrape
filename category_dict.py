import requests
import numpy as np
from bs4 import BeautifulSoup
from collections import defaultdict

def get_subreddits_ranking(subs_wanted): ## returns dict of ["subreddit": number_of_users]
    ranking = []
    subs_count = 0
    for i in range(1, 5):
        url = f"https://www.reddit.com/best/communities/{i}/"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            parent_div = soup.find("div", class_="community-list")

            if parent_div:
                subreddit = parent_div.find_all("div", recursive=False)
                for div in subreddit:
                    if subs_count == subs_wanted:
                        return ranking
                    text_div = div.find_all("div")[0]
                    sreddit_name = text_div.find_all("a")[0].text.strip()
                    h6s = text_div.find_all("h6")
                    num_members = int(h6s[1].find("faceplate-number").get("number"))
                    ranking.append((sreddit_name[2:], num_members))
                    subs_count +=1
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return ranking



def get_subreddits_by_category(subs_wanted):
    sreddit_in_cat = defaultdict(list)
    subs_count = 0
    for i in range(1, 5):
        url = f"https://www.reddit.com/best/communities/{i}/"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            parent_div = soup.find("div", class_="community-list")

            if parent_div:
                subreddit = parent_div.find_all("div", recursive=False)
                for div in subreddit:
                    if subs_count == subs_wanted:
                        return sreddit_in_cat
                    text_div = div.find_all("div")[0]
                    sreddit_name = text_div.find_all("a")[0].text.strip()
                    category = text_div.find_all("h6")[0].text.strip()
                    sreddit_in_cat[category].append(sreddit_name[2:])
                    subs_count +=1
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return sreddit_in_cat


def top_k_keys(input_dict, k):
    # Count the number of items for each key
    counts = {key: len(value) for key, value in input_dict.items()}

    # Sort the keys based on counts in descending order and select the top k
    top_keys = sorted(counts, key=counts.get, reverse=True)[:k]
    print(top_keys)
    return top_keys


def get_pool_sizes(categories, sreddit_map):
    pool_sizes = [0]*len(categories)
    for i in range(len(pool_sizes)):
        pool_sizes[i] = len(sreddit_map[categories[i]])
    return pool_sizes


def get_prior(rankings):
    # Extract user counts and apply logarithmic scale
    user_counts = np.array([count for _, count in rankings])
    log_counts = np.log(user_counts)
    # Calculate probabilities
    probabilities = log_counts / log_counts.sum()
    # Assign probabilities to rankings
    prior = {subreddit: prob for (subreddit, _), prob in zip(rankings, probabilities)}
    return prior
def main():
    # sreddit_map = get_subreddits_by_category(1000)
    # top_categories = top_k_keys(sreddit_map, 10)
    # pool_sizes = get_pool_sizes(top_categories, sreddit_map)
    # print("Top Categories: ", top_categories)
    # print("Pool sizes: ", pool_sizes)
    
    rankings = get_subreddits_ranking(1000)
    prior = get_prior(rankings)
    print(prior)

main()