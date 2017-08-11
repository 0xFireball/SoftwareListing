
import re

class StacheProcessor:
    def __init__(self, content):
        self.stache = '(?:{{)\s?(WORD)\s?(?:}})'
        self.cont = content
    
    def put(self, name, value):
        self.cont = re.sub(self.stache.replace('WORD', name), value, self.cont)

    def clean(self, value = ''):
        self.cont = re.sub(self.stache.replace('WORD', '[\w\.]+'), value, self.cont)

    def read(self):
        return self.cont
