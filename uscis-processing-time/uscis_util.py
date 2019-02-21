import urllib.request
import json

from bs4 import BeautifulSoup

def wget(url):
  response = urllib.request.urlopen(url)

  data = response.read()
  text = data.decode('utf-8')

  return text

def wget_json(url):
    return json.loads(wget(url))

def wget_soup(url):
    return BeautifulSoup(wget(url), 'html.parser')
