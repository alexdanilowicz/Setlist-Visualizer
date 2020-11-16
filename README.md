# ![logo](./img/bear.JPG) Setlist Visualizer

## NOTE:

This was one my first personal projects. It got some attention on Reddit, so leaving it as is. There's a lot of cool functionality here that could be improved upon.

## Summary

Python script that scrapes setlistfm for any band you want. Turns the frequency of the songs they play into a pretty graph.

Can be used with any band and date range. You only need to change 3 constants at top of script.

![graph](./img/example.jpeg)

### Run:

`python3 visualizeSongs.py`

### Usage:

At the top of the script, change:

1. ARTIST
	- note: this is used for titles

2. UNIQUE
	- the unique setlistfm string
	- Example: "interpol-2bd6982e.html", which is taken from the URL: [https://www.setlist.fm/setlists/interpol-2bd6982e.html](https://www.setlist.fm/setlists/interpol-2bd6982e.html)

3. URL\_TO\_STOP_AT
 - the concert you want to stop at
 - Example: "interpol/2018/sexto-nplugged-sesto-al-reghena-italy"
 - *Note: make sure to get rid of HTTPS part*

### To install:

Run in root of the project:

`mkdir p3_env`

`python3 -m venv p3_env`

to set up the enviroment.


### Already see the bin folder? Then:

Run:

`source p3_env/bin/activate`

Then, to install dependencies, run:

`pip3 install -r requirements.txt`

Then, to run the file:

`python3 [filename].py`

### Acknowledgements:

Author of original setlist.fm scraping: the talented **Ryan Lee Watts**

Github: https://github.com/ryanleewatts

Script: https://github.com/ryanleewatts/coding-project/blob/master/scraper/SetlistScript.py
