# NewsScrapy

# 

# Run newsscrapy.py to collect the news articles from news websites

	python newsscrapy.py

# call newssearchapi to search for article using 'key'


	from newssearchapi import Newsearchapi

	key = 'Mr Trump'
	search = Newsearchapi.search_news(key)
	print (search)
