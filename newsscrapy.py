import feedparser as fp
from newspaper import Article
from time import mktime
import newspaper
from datetime import datetime
from pymongo import MongoClient
import json

"""
     Connect to MongoDB database to store news articles.
     Database name : NewsScrapy
     Datacollection : newscollection
     information scrapied by the application are:
           Authors:
           Title:
           Text:
           Link:        
           Image:
           Videos:	
           Published_Date:
"""
#Connect to MongoDB to insert article data
##########################################

try:
	conn = MongoClient()
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

#Connect to NewScrapy Database
db = conn.NewsScrapy
collection = db.newscollections
############################################

LIMIT = 1000000000
articles_array=[]
data = {}
data['newpapaers'] = {}
count =1

"""
    New website information are read from JSON file.
    More no of New websites links can be added in this file.
    News webiste used of this example is : www.bbc.com
"""

#Read news network info from JSON file
with open('NewsPapers.json') as data_file:
    newsnetworks = json.load(data_file)


# Iterate through each news networks
for newsnetwork, value in newsnetworks.items():
    if 'rss' in value:
        d = fp.parse(value['rss'])
        print("Articles from ", newsnetwork)
        newsPaper = {
            "rss": value['rss'],
            "link": value['link'],
            "articles": []
        }
        for entry in d.entries:
            # if published date is not provided, the article will be skipped.
              if hasattr(entry, 'published'):
                if count > LIMIT:
                    break
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    # If the download for some reason fails (ex. 404) the script will continue downloading
                    # the next article.
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text
                article['authors'] = content.authors
                article['top_image'] =  content.top_image
                article['movies'] = content.movies
                newsPaper['articles'].append(article)
                articles_array.append(article)
                print(count, "articles downloaded from", newsnetwork, ", url: ", entry.link)
                count = count + 1
    else:
        # This is the fallback method if a RSS-feed link is not provided.
        # It uses the python newspaper library to extract articles
        print("Building site for ", company)
        paper = newspaper.build(value['link'], memoize_articles=False)
        newsPaper = {
            "link": value['link'],
            "articles": []
        }
        noneTypeCount = 0
        for content in paper.articles:
            if count > LIMIT:
                break
            try:
                content.download()
                content.parse()
            except Exception as e:
                print(e)
                print("continuing...")
                continue                       #if there is no found publish date the article will be skipped.
            article = {}
            article['title'] = content.title
            article['authors'] = content.authors
            article['text'] = content.text
            article['top_image'] =  content.top_image
            article['movies'] = content.movies
            article['link'] = content.url
            article['published'] = content.publish_date
            newsPaper['articles'].append(article)
            articles_array.append(article)
            #collection.insert_one(article)
            print(count, "Articles downloaded from", newsnetwork, " using newspaper, url: ", content.url)
            count = count + 1
    count = 1
    #insert articles into mongodb collections
    collection.insert_many(articles_array)