# prawScrape
basic reddit scraper via praw 

# Current Functions 
## scraper.__init__
constructor 
## scraper.printCommenters() 
this is a fn for just printing all current commenters within a scraper() object 
## scraper.getSubs() 
this is a fn for parsing a file that contains a subreddit name and its categories 
## scraper.getHotCommenters() 
this is a fn for scraping the commenter names of the `postLimit`th hottest posts for a subreddit given `subredditName` 
## scraper.getNewCommenters() 
this is a fn for scraping the commenter names of the `postLimit`th most recent posts for a subreddit given `subredditName` 
## scraper.getCommenterInterests() 
this is a fn for getting the names of the subreddits for the `commentLimit`th most recent comments for any given `commenter` 
