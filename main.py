#!/usr/bin/env python3

import praw
from collections import Counter
import category_dict
import json
import time


class Scraper:
    #
    # scraper.__init__()
    def __init__(self, bot: str, *, user_agent: str, subs_wanted: int = 1000, subreddits: str=None, commenters: str=None):
        self.reddit = praw.Reddit(bot, user_agent=user_agent)

        self.commenters, self.subs = set(), set()
        self.subList: list[str] = []
        if commenters is not None:
            with open(commenters, 'r') as f:
                self.commenters = set(json.load(f))
        if subreddits is not None:
            with open(subreddits, 'r') as f:
                self.subs = set(json.load(f))
        else:
            self.subredditCats: dict = category_dict.getList(subs_wanted)
            self.getSubs()

    def writeToFile(self, suffix: str=""):
        with open(f"commenters_{suffix}.json", 'w') as f:
            f.write(json.dumps(list(self.commenters)))
        with open(f"subs_{suffix}.json", 'w') as f:
            f.write(json.dumps(list(self.subs)))
    #
    # scraper.getSubs()
    def getSubs(self) -> None:
        for cat in self.subredditCats.values():
            for sub in cat:
                self.subs.add(sub)

    #
    # scraper.printCommenters()
    def printCommenters(self) -> None:
        print(self.commenters)

    #
    # scraper.getHotCommenters()
    def getHotCommenters(
        self,
        subredditName: str = "None",
        postLimit: int = 10,
        childCommentLimit: int = 0,
    ) -> None:
        sub = self.reddit.subreddit(subredditName)

        # Get hot posts
        hotPosts = sub.hot(limit=postLimit)

        for post in hotPosts:
            # replace_more(limit=0): removes all child comments within comment thread

            post.comments.replace_more(limit=childCommentLimit)
            comments = post.comments.list()

            for comment in comments:
                if hasattr(comment, "author") and comment.author:
                    self.commenters.add(comment.author.name)

    #
    # scraper.getRecentCommenters()
    def getNewCommenters(
        self,
        subredditName: str = "None",
        postLimit: int = 10,
        childCommentLimit: int = 0,
    ) -> None:
        sub = self.reddit.subreddit(subredditName)

        # Get recent posts
        recentPosts = sub.new(limit=postLimit)

        for post in recentPosts:
            print(post)
            post.comments.replace_more(limit=childCommentLimit)
            comments = post.comments.list()

            for comment in comments:
                if hasattr(comment, "author") and comment.author:
                    self.commenters.add(comment.author.name)

    #
    # scraper.getCommenterProfiles
    def getCommenterProfiles(self) -> None:
        pass

    #
    # scraper.getCommenterInterests
    def getCommenterInterests(
        self, commenter: str = "spez", commentLimit: int = 10
    ) -> None:
        recentSubs = {}  # Need freq
        recentSubNames = set()
        commenterProf = self.reddit.redditor(commenter)
        comments = commenterProf.comments.new(limit=commentLimit)

        for comment in comments:
            currSub = comment.subreddit.display_name

            if currSub not in recentSubs:
                recentSubs[currSub] = 0
                recentSubNames.add(currSub)
                self.subList.append(currSub)
            else:
                recentSubs[currSub] += 1

        print(
            f"Here are the recently interacted subnames for {commenter}: {recentSubNames}"
        )
        pass

    #
    # scraper.getCommenterSubs
    def getCommenterSubs(self, username: str) -> list:
        redditor = self.reddit.redditor(username)
        comments = list(redditor.comments.new())
        subreddits = [comment.subreddit.display_name for comment in comments]
        return subreddits

    #
    # scraper.getCommenterSubCount
    def getCommenterSubCount(self, username: str) -> dict:
        subreddits = self.getCommenterSubs(username)
        return Counter(subreddits)

    #
    # scraper.getCats
    def getCommenterCategories(self, username: str):
        redditor = self.reddit.redditor(username)
        self.getCommenterInterests(commenter=username)
        finalCats = []
        for sub in self.subList:
            for key in self.subredditCats:
                if sub in self.subredditCats[key]:
                    finalCats.append(key)

        return finalCats


def main():
    print("input bot name from praw.ini:\n")
    bot = input()

    user = "chromiridium"  # my username

    scraper = Scraper(bot, user_agent=f"script:pool-inf:v0.0 by u/{user}",subs_wanted=1000)

    for sub in scraper.subs:
        while True:
            try:
                print(f"getting commenters from {sub}")
                scraper.getHotCommenters(sub, postLimit=100)
                break
            except Exception as e:
                time.sleep(60)
                pass

    print(f'total commenters: {len(scraper.commenters)}')
    comments = dict()
    for commenter in scraper.commenters:
        while True:
            try:
                print(f"counting comments by {commenter}")
                comments[commenter] = scraper.getCommenterSubs(commenter)
                break
            except Exception as e:
                time.sleep(60)
                pass

    with open("comments.json", 'w') as f_out:
        f_out.write(json.dumps(comments))


if __name__ == "__main__":
    main()

