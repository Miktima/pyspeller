from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .getcontent import getContent
import requests
import xml.etree.ElementTree as ET
import urllib3
from spellchecker import SpellChecker
import re
import string
from .models import Addwords

def index(request):
    urllib3.disable_warnings()
    xmlUrl = "https://ria.ru/export/rss2/archive/index.xml"
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"

    headers = {
        'user-agent': userAgent
        }

    xmlResponse = requests.get(xmlUrl, headers=headers, verify=False)

    spell_ru = SpellChecker(language=None)
    spell_ru.word_frequency.load_text_file(str(settings.BASE_DIR) + '/ru.txt')
    spell_en = SpellChecker()

    root = ET.fromstring(xmlResponse.content)

    result_list = []
    mask = string.punctuation
    repl = " " * len(mask)
    trTable = str.maketrans(mask, repl)
    i = 0
    for item in root.iter('item'):
        parser = getContent("div", [("class", "article__text")])
        ierr = []
        link = item.find("link").text
        htmlResponse = requests.get(link, headers=headers, verify=False)
        parser.feed((htmlResponse.content).decode('utf-8'))
        # print (parser.result)
        article = re.sub(r'([.,;:!?])([^\d\s])', r'\1 \2', parser.result)
        parser.close()
        # parser.reset()
        words = article.split()
        nw = 0
        for w in words:
            testw = (w.translate(trTable)).strip()
            if len(testw) > 0:
                    if testw not in spell_ru and testw not in spell_en and testw.isalpha():
                        ierr.append(nw)
            nw += 1
        result_list.append({
            "link": link,
            "error": ierr,
            "article": words
        })
        if i == 5:
            break
        i += 1
    context = {
        "results": result_list
    }

    return render(request, 'speller/index.html', context)

def save_word(request):
    print (request.POST)
    mask = string.punctuation
    repl = " " * len(mask)
    trTable = str.maketrans(mask, repl)
    if request.method == 'POST':
        word = request.POST['word']
        word = (word.translate(trTable)).strip()
        print (word)
        addWord = Addwords (word=word)
        addWord.save()
        return HttpResponse("OK")
    else:
        return render(request, 'speller/index.html')
         