### NOTES AND LINKS:

# NEED A TOOL TO NAVIGATE WEBPAGES (I.E. GO TO PAGE, TYPE IN NAME OF MOVIE, AND CLICK)
# SOME IDEAS: http://stackoverflow.com/questions/1292817/how-to-automate-browsing-using-python
# SEEMS PROMISING: http://docs.python-requests.org/en/latest/#
# also see this: https://github.com/vaidik/GoogleMovieShowtimesPythonParser

### GRACENOTE API: 
# http://developer.tmsapi.com/docs/read/data_v1_1/movies/Movie_showtimes
# API KEY: h7uzzzc93934fuaqydx9f7fb

### BEAUTIFUL SOUP EXAMPLE:
#f = urllib.urlopen("http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm") 
#soup = BeautifulSoup(f, 'html.parser')
#print(soup.prettify())


%autoindent
from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
import datetime as dt  
import pandas as pd
import re

# Use today's date and the zip code 11225

todays_date = dt.datetime.today().strftime("%Y-%m-%d")
zipcode = '&zip=11225'
api_key = '&api_key=h7uzzzc93934fuaqydx9f7fb'

url = 'http://data.tmsapi.com/v1.1/movies/showings?startDate='
url += todays_date
url += zipcode
url += api_key
response = urlopen(url)
data = response.read()


# Code to parse the text data

f = open("/Users/kobrosly/Desktop/test.txt","r")
data = f.read()


id_spots = []
for c in range(0,len(data)):
	if data[c-4] == 't' and data[c-3] == 'm' and data[c-2] == 's' and data[c-1] == 'I' and data[c] == 'd':
		id_spots.append(c-5)

unique_movies = []
for i in range(0,len(id_spots)):
	if i == (len(id_spots) - 1):
		spot1 = id_spots[i]
		spot2 = (len(data)-1)
		unique_movies.append(data[spot1:spot2])
	else:
		spot1 = id_spots[i]
		spot2 = id_spots[i+1]
		unique_movies.append(data[spot1:spot2])

unique_movies = pd.Series(unique_movies)


# Use regex to find expression between (title":") and (",")

titles = [] 
count = 0
for movie_entry in unique_movies:
	temp = re.findall(r"title...([\w\:\s\.\!\,\-\'\&]+)\"\,\"",  movie_entry)
	titles.append(temp[0])

titles = pd.Series(titles)

