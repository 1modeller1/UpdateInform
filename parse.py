import requests
from bs4 import BeautifulSoup
import lxml
import sys
import json

def parseRanobe_MangaLib (url, name):
  # req = requests.get(url)
  # data = json.loads(req.text)
  data = json.load(open("get.json", "r"))
  found = False; remChapters = False; ll = 0
  chNames = []

  l = len(data["data"])

  save = open("save.json", "r")
  d = json.load(save)
  for n in d["data"]:
    if n["name"] == name:
      if l > n["chapters_count"]:
        ll = n["chapters_count"]
        n.update({"chapters_count" : l })
        for t in range(ll, l):
          chNames.append(data["data"][t]["name"])
      if l < n["chapters_count"]:
        remChapters = True
        ll = n["chapters_count"]
        n.update({"chapters_count": l})
      found = True
      break

  if not found:
    d["data"].append({"name" : name, "chapters_count" : l})

  save.close()
  save = open("save.json", "w")
  json.dump(d, save, indent=4)
  save.close()

  if len(chNames) > 0:
    return [l-ll, chNames]
  elif remChapters:
    return [l-ll, "Rem"]
  elif not found:
    return [l, "Add"]
  else:
    return [0, "None"]

def makeJsonViewable (file):
  get = open(file, "r")
  d = json.load(get)
  get.close()

  set = open(file, "w")
  json.dump(d, set, indent=4)
  set.close()

if __name__ == "__main__":
  args = sys.argv[1:]
  # args = ["div", ""]
  url = "https://ranobelib.me/ru/book/6689--ascendance-of-a-bookworm-novel?ysclid=m7obtjmi1q156785609"
  ans = []

  if "ranobelib.me" in url:
    indexSt = url.find("/book/")
    indexEnd = url.find("?")
    name = url[indexSt + 6: indexEnd]

    url2 = "https://api2.mangalib.me/api/manga/" + name + "/chapters"
    ans = parseRanobe_MangaLib(url2, name)

  if "mangalib.me" in url:
    indexSt = url.find("/manga/")
    indexEnd = url.find("?")
    name = url[indexSt + 6: indexEnd]

    url2 = "https://api2.mangalib.me/api/manga/" + name + "/chapters"
    ans = parseRanobe_MangaLib(url2, name)

  if ans[1] == "Add":
    print(f"{name} was added")
  elif ans[0] > 0:
    if ans[0] == 1:
      print(f"Chapter '{ans[1][0]}' was added")
    else:
      print("New chapters was added:")
      for line in ans[1]:
        print(line)
  elif ans[0] < 0:
    if abs(ans[0]) == 1:
      print("One chapter was removed. For what?")
    else:
      print(f"{abs(ans[0])} chapters was removed. For what?")
  else:
    print("Nothing was added")