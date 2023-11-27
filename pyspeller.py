import requests
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import urllib3
from spellchecker import SpellChecker
import re

class getContent(HTMLParser):
    def __init__(self, tag:str, attrs:list):
        self.tag = tag
        self.attrs = attrs
        self.intag = 0
        self.result = ""
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        seta1 = set(self.attrs)
        seta2 = set(attrs)
        if tag == self.tag and seta1 == seta2:
            self.intag = 1
    
    def handle_endtag(self, tag):
        if tag == self.tag and self.intag == 1:
            self.intag = 0

    def handle_data(self, data):
        if self.intag == 1:
            self.result += data
    
urllib3.disable_warnings()
xmlUrl = "https://ria.ru/export/rss2/archive/index.xml"
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"

headers = {
    'user-agent': userAgent
    }

xmlResponse = requests.get(xmlUrl, headers=headers, verify=False)

spell = SpellChecker(language=None)
spell.word_frequency.load_text_file('ru.txt')

root = ET.fromstring(xmlResponse.content)

html_body = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1">\
		<meta http-equiv="X-UA-Compatible" content="IE=edge"> <title>Article errors</title> </head> <body>'

i = 0
parser = getContent("div", [("class", "article__text")])
for item in root.iter('item'):
    if i == 5:
        link = item.find("link").text
        article = ""
        htmlResponse = requests.get(link, headers=headers, verify=False)
        parser.feed((htmlResponse.content).decode('utf-8'))
        print ("Link: ", link)
        html_body += "<p>Link to the article: <a href='" + link + "'>" + link + "</a></p>"
        print ("---------------------")
        html_body += "<p>"
        # print (parser.result)
        words = parser.result.split()
        for w in words:
            testw = re.sub(r'[^\w]', '', w)
            if testw in spell:
                html_body += w
            else:
                print ("<mark>", w, "</mark>")
        html_body += "</p>"
    i += 1