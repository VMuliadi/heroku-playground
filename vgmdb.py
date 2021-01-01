#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

class VGMDB:
  def get_tracklist(self, vgmdb_url, vgmdb_filters=None):
    try:
      tracklists = []
      filter_enums = {"number": 0, "title": 1, "duration": 2}
      bsoup = BeautifulSoup(requests.get(vgmdb_url).text, "html.parser")
      for track in bsoup.findAll("table", {"class": "role"})[0].findAll("tr"):
        tracklist = {}
        track_detail = track.findAll("td", {"class": "smallfont"})
        if vgmdb_filters == None: 
          tracklist["number"] = track_detail[0].text.strip()
          tracklist["title"] = track_detail[1].text.strip()
          tracklist["duration"] = track_detail[2].text.strip()
        else:
          vgmdb_filters = vgmdb_filters.replace(" ", "")
          print(vgmdb_filters)
          if all(all_key in list(filter_enums.keys()) for all_key in vgmdb_filters.split(",")):
            for vgmdb_filter in vgmdb_filters.split(","):
              tracklist[vgmdb_filter] = track_detail[filter_enums[vgmdb_filter]].text.strip()
        tracklists.append(tracklist)
      return tracklists
    except Exception as exception: 
      print(exception)
      return []