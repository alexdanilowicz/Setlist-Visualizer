# Author of original setlistfm scraping: ryanleewatts
# Github: https://github.com/ryanleewatts
# Original script: https://github.com/ryanleewatts/coding-project/blob/master/scraper/SetlistScript.py
#
# Example Usage:
#	python3 visualizeSongs.py
#
# Author: Alex Danilowicz
# 	Wrote for fun as a summer personal project.
#	Started as just a way to see what Radiohead songs would be played...
#
# First run it with scrape(), then once the file is created, run it with visualize()

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import random
from collections import defaultdict
from pathlib import Path

# THINGS YOU MUST CHANGE
ARTIST = "The National"
UNIQUE = "the-national-53d69b79.html" # MAKE SURE TO INCLUDE .html part


URL_TO_STOP_AT = "/baluarte-pamplona-spain-33b4b0a9.html" # Note: get rid of HTTPS part
URL_TO_START_AT = "html" # this url will be the first one to be scraped. If you want first one, put in nothing or html
CUSTOM = True # if true, be sure to define returnCustomAlbumDict

# OPTIONAL THINGS TO CHANGE
YEAR = "2022"
SORT_ALBUM = False # toggle if you want to sort by album or not. if false, sorts by count
FILE = ARTIST + "-Data" + "-" + YEAR +".xlsx" # filename
TITLE = "The National's 2022 Summer Tour "
SONGS_TO_IGNORE = ["I Can't Forget"]
MAX_PAGES = 10000 # max to scrape, not used if URL_TO_STOP set properly
FONT_SIZE_TICKS = 8
FONT_Y = 10 # for labels
color_album_dict = {}

def scrape():
	if ('.html' not in UNIQUE):
		raise Exception("You must add .html to the unique var otherwise you will stuck in an infinite loop")

	UNIQUE_URL = "https://www.setlist.fm/setlists/" + UNIQUE + "?page="
	SONG_URL = "https://www.setlist.fm/stats/songs/" + UNIQUE + "?song="  # notice difference: /stats/
	visited = {} # key song, album is value
	links = []
	dm = []
	my_file = Path("./" + FILE)
	if not my_file.is_file(): # only do scraping if file doesn't exist already
		break_bool = False
		start = False
		for i in range(MAX_PAGES):
			if break_bool:
				break
			url = UNIQUE_URL + str(i + 1)
			print('🎉 Page ', url)
			r = requests.get(url)
			soup = bs(r.content, "lxml")
			#print('🍲 Soup', soup)
			for link in soup.find_all('a', class_='summary url'):
				setlist = (link.get('href'))
				completeurl = 'http://www.setlists.fm' + setlist[2:]
				if URL_TO_START_AT in completeurl:
					start = True
				if start:
					print("Considering url: ", completeurl)
					if completeurl not in links:
						if "/setlist/the-national/2022" in completeurl:
							print("ℹ️ Getting url: " + completeurl) # print the output
							links.append(completeurl)
				# stop at this url
				if URL_TO_STOP_AT in completeurl:
					break_bool = True
					break # stop at this setlist

		# Scrape every url in that list
		for item in links:
			print('🎹 Looking at setlist for: ', item)
			# 1. Scrape the date
			r = requests.get(item)
			soup = bs(r.content, "lxml")
			for datehtml in soup.find_all('em', class_='link', text=True):
				date = datehtml.text[:-7]
				date = date.partition(",")[0]
				date = date.replace(" ", "")

			# 2. Scrape the setlist
			songs = []
			for songHTML in soup.find_all('div', class_='songPart'):
				songstext = songHTML.text
				# hardcoded these, cause too lazy to put into list
				# skip the intro/outro songs that are always there
				thesong = songstext.encode('utf-8').rstrip().strip().decode("utf-8")
				if thesong not in SONGS_TO_IGNORE:
					songs.append(thesong)

			#3. Scrape the album
			for song in songs:
				if str(song) not in visited:
					print('Getting the song 🎵', song)
					# hardcoded this one for Radiohead cause url format is wonky, can fix later
					if "2 + 2 = 5" in song:
						r = requests.get("https://www.setlist.fm/stats/songs/radiohead-bd6bd12.html?song=" + "2+%2B+2+%3D+5")
					else:
						r = requests.get(SONG_URL + song)
					soup = bs(r.content, "lxml")

					thenext = False
					for album in soup.find_all('span'):
						if thenext:
							thealbum = album.text
							thealbum = thealbum.replace("(Album)", "")
							thealbum = thealbum.replace("(Single)", "")
							thealbum = thealbum.strip("'")
							thealbum = thealbum.rstrip()
							# harcoded but you could just see if the key is in th
							# if thealbum not in returnCustomAlbumDict(color_album_dict):
							# 	thealbum = "Other"
							if (str(song) == "This Isn't Helping"):
								visited[str(song)] = "New Album"
							if (str(song) == "Moon Drop Light"):
								visited[str(song)] = "New Album"
							if (str(song) == "Tropic Morning News (Haversham)"):
								visited[str(song)] = "New Album"							
							else:
								visited[str(song)] = thealbum
							break
						if album.text == "From the release": # album name falls under this span
							thenext = True
				else:
					thealbum = visited[str(song)]

				try:
					dm.append([date, song, thealbum])
				except:
					print("skipping over this song")

		df = pd.DataFrame(dm, columns=['Date', 'Track', 'Album'])

		df.to_excel(FILE, index=False)
	else:
		visualize_album()
def return_original_df():
	return pd.read_excel(FILE, sheet_name="Sheet1")

def create_clean_df():
	df = return_original_df()
	total_df = df.copy()
	count = len(total_df['Track'].unique())
	print(count)
	total = len(total_df['Date'].unique())

	albums = df[['Track', 'Album']]
	# put track as index, date in row
	unique_df = df.groupby(df['Track']).nunique() # get count
	# clean up and rename
	del unique_df['Album']
	unique_df = unique_df.rename(columns={'Date': 'Count_Played'})

	# merge with albums df, I assume there's a better way...
	albums = albums.set_index('Track')
	albums = albums[~albums.index.duplicated(keep='first')]
	unique_df = pd.merge(unique_df, albums, left_index=True, right_index=True)

	return (total, unique_df)

def visualize_album():
	(total, unique_df) = create_clean_df()
	album_df = unique_df.copy()
	color_album_dict = return_color_album_dict(album_df['Album'].unique().tolist())

	unique_df['Album'] = pd.Categorical(unique_df['Album'], color_album_dict.keys()) # order it by dictionary

	if SORT_ALBUM: # sort by album, then count
		unique_df = unique_df.sort_values(['Album', 'Count_Played'], ascending=True)
		ORDERCOUNT = ""
	else:
		ORDERCOUNT = "-OrderedByCount"
		unique_df = unique_df.sort_values(['Count_Played', 'Album'], ascending=True)

	# convert to percentages
	unique_df['Frequency'] = unique_df['Count_Played'].div(total).multiply(100)

	c = []
	l = unique_df['Album'].tolist()
	for val in l:
		c.append(color_album_dict[val])
	# https://github.com/pandas-dev/pandas/issues/16822#issuecomment-1257284602
	ax = unique_df.plot.barh(y='Frequency', color=c)


	format(ax, color_album_dict, total, unique_df)

	plt.savefig("./Visual-" + ARTIST + ORDERCOUNT + YEAR + ".png", format='png', dpi=1200)
	plt.show()

def format(ax, color_dict, total, df):
	plt.rcParams["font.family"] = "Helvetica"
	hfont = {'fontname':'Helvetica'}

	# The following two lines generate custom fake lines that will be used as legend entries:
	markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in color_dict.values()]
	plt.legend(markers, color_dict.keys(), numpoints=1, fontsize='7')

	# formatting labels
	ax.set_xlabel("Frequency" + " (" + str(total) + " concerts)", **hfont)
	fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
	xticks = mtick.FormatStrFormatter(fmt)
	ax.xaxis.set_major_formatter(xticks)

	plt.xticks(fontname='Helvetica')


	ax.set_ylabel("Track (" + str(len(df.index)) + ")", **hfont)
	plt.yticks(fontsize=FONT_Y, fontname='Helvetica')
	plt.title(TITLE, fontsize=16, **hfont)
	plt.figtext(0.5, 0.01, 'Created by github.com/alexdanilowicz/Setlist-Visualizer', wrap=True, horizontalalignment='center', fontsize=7, **hfont)


	for i in ax.patches:
		ax.text(i.get_width()+.3, i.get_y()+.38, str(round((i.get_width()*total/100), 1)).replace(".0", ""), fontsize=FONT_SIZE_TICKS, color='dimgrey', **hfont)

	ax.invert_yaxis()
	plt.tight_layout()


# helper function to sort by date
def sorting(date):
	string = ''.join(x for x in date if x.isdigit())
	return int(string)

def return_color_album_dict(albums_list):
	color_album_dict = {}

	# HERE YOU CAN SPECIFY ALBUM COLORS SO THEY FIT YOUR ARTIST's ALBUM ARTWORK
	# Make sure you catch everything, or it will not map properly
	if CUSTOM:
		color_album_dict = returnCustomAlbumDict(color_album_dict)

	else: # otherwise, just get random ugly hex colors
		number_of_colors = len(albums_list)
		random_hex_list = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
		for i in range(number_of_colors)]

		i = 0
		for album in albums_list:
			color_album_dict[album] = str(random_hex_list[i])
			i += 1

	return color_album_dict

def returnCustomAlbumDict(color_album_dict):
	color_album_dict["Boxer"] = '#79B791' #lime green
	color_album_dict["Trouble Will Find Me"] = '#96C9DC' #sky blue
	color_album_dict["Alligator"] = '#F06C9B' # dark pink
	color_album_dict["Cherry Tree"] = '#F5D491' # yellow
	color_album_dict["High Violet"] = '#666A86' # purplish
	color_album_dict["Sleep Well Beast"] = '#333333' # grey
	color_album_dict["I Am Easy to Find"] = '#61A0AF' # dark blue
	color_album_dict["New Album"] = '#E6AA9F' # pink

	return color_album_dict

if __name__ == "__main__":
	scrape()
