import requests, bs4, re, time, fake_useragent
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

print("Enter an artist and an album to analyze: ")
inartist, inalbum = input().split(', ')
outartist, outalbum = inartist.lower().replace(' ',''), inalbum.lower()
#case in which the artist's name starts with a number (e.g. 50 cent)
if re.match('\d', outartist[0]):
    link = "https://www.azlyrics.com/{}/{}.html".format('19', outartist)
#case in which the artists name starts with a letter
else: 
    link = "https://www.azlyrics.com/{}/{}.html".format(outartist[0], outartist)

ua = UserAgent()
headers = {'User-Agent':str(ua.safari)}
res = requests.get(link, headers=headers)
res.raise_for_status()
albums = []

#finding the names of all albums
for alb in bs4.BeautifulSoup(res.text, 'html.parser').findAll("b"):
    albums.append(alb.get_text().strip("\"").lower())

#checks to see if the album entered matches an album that was found
for alb in albums:
    if alb==outalbum: 
        print("Album", inalbum, "exists in the artists discography")
        print("\n")

listsongs, counter = [], 1
for divlistalb in bs4.BeautifulSoup(res.text, 'html.parser').findAll("div", class_="listalbum-item"): #iterating through the songs in the album
    if outalbum in (divlistalb.find_previous_sibling("div", class_="album").get_text().lower()):
        listsongs.append(divlistalb.a['href'].replace("..", "https://azlyrics.com"))
        print("Song", counter, ":", divlistalb.a.get_text())
        counter+=1

lyrics_all = []
#getting the lyrics of each song
for song in listsongs: 
    uavar = UserAgent()
    headersvar = {'User-Agent':str(uavar.safari)}
    res2 = requests.get(song, headers=headersvar)
    res2.raise_for_status()
    lyrics = bs4.BeautifulSoup(res2.text, 'html.parser').find("div", class_="ringtone").find_next("div").get_text()
    lyrics_all.append(lyrics)
    time.sleep(.2)

#regex to strip away unwanted information (e.g. change in speaker, etc..)
for song in lyrics_all: 
    song = re.sub('\[(.)+\]', "", song, 0)
    song = song.replace("\n",  " ")

with open('./myfile.txt','w') as myfile:
    if not lyrics_all:
        myfile.write("ERROR")
    for line in lyrics_all:
        myfile.write(line)

print("Program finished.")
