#!/usr/bin/env python3

import praw
from collections import Counter
import category_dict


class scraper:
    #
    # scraper.__init__()
    def __init__(self, cid: str, c_secret: str, uagent: str, uname: str):
        self.signIn = praw.Reddit(
            client_id=cid, client_secret=c_secret, user_agent=uagent, username=uname
        )

        self.commenters, self.subs = set(), set()
        self.subList: List[str] = []
        self.subredditCats: dict = category_dict.getList()

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
        sub = self.signIn.subreddit(subredditName)

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
        sub = self.signIn.subreddit(subredditName)

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
        commenterProf = self.signIn.redditor(commenter)
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
    # scraper.getCommentSubCount
    def getCommentSubCount(self, username: str) -> dict:
        redditor = self.signIn.redditor(username)
        comments = list(redditor.comments.new())
        subreddits = [comment.subreddit.display_name for comment in comments]
        return Counter(subreddits)

    #
    # scraper.getCats
    def getCommenterCategories(self, username: str):
        redditor = self.signIn.redditor(username)
        self.getCommenterInterests(commenter=username)
        finalCats = []
        for subname in self.subList:
            for key in self.subredditCats:
                if subname in self.subredditCats[key]:
                    finalCats.append(key)

        return finalCats


if __name__ == "__main__":
    cid = "6fW8tp7LsoQsq6CpvW9-Eg"
    c_secret = "wJjYN1FfBxFlSvhjPH3ZVp6L6xPwlw"
    uagent = "phantom_rift"
    uname = None
    subname = "gaming"

    inst = scraper(cid, c_secret, uagent, uname)
    # inst.getNewCommenters(subname)
    # inst.printCommenters()
    # inst.parseSubFile("test.txt")
    # inst.getCommenterInterests()
    print(inst.getCommenterCategories("fruitrollupsalad"))

    # print(test)
