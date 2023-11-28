from django.shortcuts import render
from django.conf import settings
from .getcontent import getContent
import requests
import xml.etree.ElementTree as ET
import urllib3
from spellchecker import SpellChecker
import re
import string

def index(request):
    urllib3.disable_warnings()
    xmlUrl = "https://ria.ru/export/rss2/archive/index.xml"
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"

    headers = {
        'user-agent': userAgent
        }

    xmlResponse = requests.get(xmlUrl, headers=headers, verify=False)

    spell = SpellChecker(language=None)
    spell.word_frequency.load_text_file(str(settings.BASE_DIR) + '/ru.txt')

    root = ET.fromstring(xmlResponse.content)

    i = 0
    parser = getContent("div", [("class", "article__text")])
    result_list = []
    mask = string.digits + string.punctuation
    repl = " " * len(mask)
    trTable = str.maketrans(mask, repl)
    for item in root.iter('item'):
        ierr = []
        if i < 5:
            link = item.find("link").text
            htmlResponse = requests.get(link, headers=headers, verify=False)
            parser.feed((htmlResponse.content).decode('utf-8'))
            print (parser.result)
            article = re.sub(r'([.,;:!?])([^\d\s])', r'\1 \2', parser.result)
            words = article.split()
            nw = 0
            for w in words:
                testw = (w.translate(trTable)).strip()
                if len(testw) > 0:
                        if testw not in spell:
                            ierr.append(nw)
                nw += 1
            result_list.append({
                "link": link,
                "error": ierr,
                "article": words
            })
        i += 1
    context = {
        "results": result_list
    }

    return render(request, 'speller/index.html', context)