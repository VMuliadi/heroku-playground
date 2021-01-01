#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

class VGMDB:
  def get_tracklist(self, vgmdb_album_id, vgmdb_filters=None):
    try:
      tracklists = []
      filter_enums = {"number": 0, "title": 1, "duration": 2}
      bsoup = BeautifulSoup(requests.get("https://vgmdb.net/album/" + vgmdb_album_id).text, "html.parser")
      for index, album_disc in enumerate(bsoup.\
          findAll("span", {"class": "tl"})[0].\
          findAll("table", {"class": "role"})):
        for album in album_disc.findAll("tr"):  # loop through each table to get the title
          tracklist = {}
          track_detail = album.findAll("td", {"class": "smallfont"})
          if vgmdb_filters == None: 
            tracklist["title"] = track_detail[1].text.strip()
            tracklist["duration"] = track_detail[2].text.strip()
            tracklist["number"] = str(index + 1) + track_detail[0].text.strip()
          else:
            vgmdb_filters = vgmdb_filters.replace(" ", "")
            if all(all_key in list(filter_enums.keys()) for all_key in vgmdb_filters.split(",")):
              for vgmdb_filter in vgmdb_filters.split(","):
                tracklist[vgmdb_filter] = track_detail[filter_enums[vgmdb_filter]].text.strip()
                if vgmdb_filter == "number":
                  tracklist[vgmdb_filter] = str(index + 1) + track_detail[filter_enums[vgmdb_filter]].text.strip()
          tracklists.append(tracklist)
      return tracklists
    except Exception as exception: 
      print(exception)
      return None
