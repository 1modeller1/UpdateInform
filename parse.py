import requests
from bs4 import BeautifulSoup
# import lxml
import sys
import os
import json
from time import localtime

D = ""

# Прикольная жуть чтобы поместить файл txt или подобный ему прямо в исполняемый файл при компиляции,
# но его изменения сохраняться больше не будут
def path(relative_path):
  if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
  else:
    base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)

def getTime ():
  d = str(localtime().tm_mday)
  m = str(localtime().tm_mon)
  y = str(localtime().tm_year)

  if len(d) == 1:
    d = "0" + d
  if len(m) == 1:
    m = "0" + m

  h = str(localtime().tm_hour)
  if len(h) == 1:
    h = "0" + h
  min = str(localtime().tm_min)
  if len(min) == 1:
    min = "0" + min
  return h + ":" + min + "  " + d + "." + m + "." + y

def clearSoupText (soup):
  text = ""
  check = True
  for c in soup.text:
    if check and c == '\n':
      check = False
    elif c == '\n':
      continue
    else:
      check = True
    text += c
  return text

def parseRanobe_MangaLib (url, rawUrl, name, title):
  req = requests.get(url)
  data = json.loads(req.text)
  found = False; remChapters = False; ll = 0
  chNames = []
  outPlus = ""

  l = len(data["data"])

  save = open("memRanobe_MangaLib.json", "r")
  d = json.load(save)
  for n in d["data"]:
    if n["name"] == name:
      if title != "":
        n.update({"title" : title})
        outPlus = "Title was edited"
      if rawUrl != n["rawUrl"]: # Зайти можно как с главной страницы сайта, так и со списка глав. Это нужно для изменения способа входа
        n.update({"rawUrl" : title})
        outPlus = "rawUrl was edited"
      if l > n["chapters_count"]:
        ll = n["chapters_count"]
        n.update({"chapters_count" : l })
        for t in range(ll, l):
          chNames.append(data["data"][t]["name"])
        n.update({"time" : getTime()})
      if l < n["chapters_count"]:
        remChapters = True
        ll = n["chapters_count"]
        n.update({"chapters_count": l})
        n.update({"time": getTime()})
      found = True
      break

  if not found:
    d["data"].append({"name" : name, "chapters_count" : l, "title" : title, "rawUrl" : rawUrl, "time" : getTime()})

  save.close()
  save = open("memRanobe_MangaLib.json", "w")
  json.dump(d, save, indent=4)
  save.close()

  if len(chNames) > 0:
    if l-ll == 1:
      return f"Chapter '{chNames[0]}' was added"
    else:
      out = "New chapters was added:"
      for line in chNames:
        out += line
      return out
  elif remChapters:
    if abs(l-ll) == 1:
      return "One chapter was removed. For what?"
    else:
      return f"{abs(l-ll)} chapters was removed. For what?"
  elif not found:
    return f"{name} was added"
  elif outPlus != "":
    return outPlus
  else:
    return "Nothing was added"

def parseRawWithArgs (url, title, args=[]):
  global  D
  req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
  soup = BeautifulSoup(req.text, "lxml")

  for arg in args:
    if len(arg) == 1:
      soup = soup.find(arg[0])
    else:
      soup = soup.find(arg[0], {arg[1] : arg[2]})

  D = clearSoupText(soup)

  pack = soup.text
  found = False; message = "Nothing was added"

  save = open("memRawWithArgs.json", "r")
  d = json.load(save)
  for n in d["data"]:
    if url == n["rawUrl"]:
      if title != "":
        n.update({"title" : title})
        message = "Title was edited"
      if args != n["args"]:
        n.update({"args" : args})
        message = "Args were edited"
      if soup.text != n["package"]:
        message = "There is something new!"
        n.update({"package" : soup.text})
        n.update({"time" : getTime()})
      found = True

  if not found:
    d["data"].append({"rawUrl" : url, "package" : pack, "title" : title, "time" : getTime(), "args" : args})
    message = "Data was added"

  save.close()
  save = open("memRawWithArgs.json", "w")
  json.dump(d, save, indent=4)
  save.close()

  return message

# def makeJsonViewable (file):
#   get = open(file, "r")
#   d = json.load(get)
#   get.close()
#
#   set = open(file, "w")
#   json.dump(d, set, indent=4)
#   set.close()

def parseUrl(url, title, args=[]):
  global D
  out = ""

  if len(args) > 0:
    out = parseRawWithArgs(url, title, args)
  elif "ranobelib.me" in url:
    indexSt = url.find("/book/")
    indexEnd = url.find("?")
    name = url[indexSt + 6: indexEnd]

    url2 = "https://api2.mangalib.me/api/manga/" + name + "/chapters"
    out = parseRanobe_MangaLib(url2, url, name, title)

  elif "mangalib.me" in url:
    indexSt = url.find("/manga/")
    indexEnd = url.find("?")
    name = url[indexSt + 7: indexEnd]

    url2 = "https://api2.mangalib.me/api/manga/" + name + "/chapters"
    out = parseRanobe_MangaLib(url2, url, name, title)
  else:
    out = parseRawWithArgs(url, title, args)

  print("Done")
  return [out, D]

def lookParse (url, args=[]):
  req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
  soup = BeautifulSoup(req.text, "lxml")

  for arg in args:
    if len(arg) == 1:
      soup = soup.find(arg[0])
    else:
      soup = soup.find(arg[0], {arg[1]: arg[2]})

  # file = open("htmlFile.html", "w")
  # file.write(soup.text)

  text = clearSoupText(soup)

  print("Done")
  return text

def parseAll ():
  list = ["memRanobe_MangaLib.json", "memRawWithArgs.json"]
  output = getTime() + "\n\n"
  changed = ""

  for a in list:
    f = open(a, "r")
    j = json.load(f)

    for book in j["data"]:
      try:
        args = book["args"]
      except:
        args = []
      out = parseUrl(book["rawUrl"], "", args)
      output += book["title"] + ": " + out[0] + "\n"
      if out[0] != "Nothing was added":
        changed += book["title"] + ": " + out[0] + "\n"
    f.close()
  return [output, changed]