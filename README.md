# ![logo](./img/bear.JPG) Setlist Visualizer

This was one my first personal projects. There's a lot of cool functionality here that could be improved upon. I'd like to make a web app. I come back to it about every few years after my favorite artists go on tour.

## Support

<a href="https://www.buymeacoffee.com/leftonread" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

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

3. URL_TO_STOP_AT

- the concert you want to stop at
- Example: "interpol/2018/sexto-nplugged-sesto-al-reghena-italy"
- _Note: make sure to get rid of HTTPS part_

## Quickstart:

```
mkdir p3_env; python3 -m venv p3_env; source p3_env/bin/activate; pip3 install -r requirements.txt
```

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
