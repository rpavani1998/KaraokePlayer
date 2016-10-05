import sys
#import eyed3
import requests
from bs4 import BeautifulSoup
from lxml import html
#import urllib



def getlink(name) :
	print ((name))
	req = requests.get("http://www.google.com/search?q=" + name.replace(' ', '+') + '+lyrics')
	encodedQuery = req.text.encode('ascii', 'ignore')
	req.close()
	soup = BeautifulSoup(encodedQuery,"lxml")
	songLink = ''
	elemAttr = soup.select("h3 a")
	for link in elemAttr:
	    if str(link.attrs["href"]).find('lyricsmint') > 0:
	        songLink = str(link.attrs["href"])
	        songLink = songLink[songLink.find('http'):(songLink.find('html') + len('html'))]
		#lyrics(songLink)
	    if not songLink:
                if str(link.attrs["href"]).find('metrolyrics') > 0:
                    songLink = str(link.attrs["href"])
                    songLink = songLink[songLink.find('http'):(songLink.find('html') + len('html'))]
	return(songLink)

def lyrics(name) :
	songLink = getlink(name)
	print(songLink)
	req = requests.get(songLink)
	encodedQuery = req.text.encode('ascii', 'ignore')
	req.close()
	soup = BeautifulSoup(encodedQuery,"lxml") 
	lyrics = soup.findAll('div', {'style': 'margin-left:10px;margin-right:10px;'})
	lyrics= (soup.findAll('p', attrs={'class' : 'verse'}))
	lyrics = str.join(u'\n',map(str,lyrics))
	lyrics = (lyrics.replace('<p class="verse">','\n'))
	lyrics = (lyrics.replace('<br/>',' '))
	lyrics = lyrics.replace('</p>',' ')
	loc = '/Documents/Karaoke_player/lyrics'        
	filename = loc + '/' + name + '.txt'
	with open(filename, "w") as text_file:
		print("{}".format(lyrics), file=text_file)
	print (lyrics)
		  
