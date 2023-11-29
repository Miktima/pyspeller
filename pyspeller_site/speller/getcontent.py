from html.parser import HTMLParser

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
            self.result += data + " "
    