#-*- coding: UTF-8 -*-
class Movie(object):
    def __init__(self,rate,cover_x,is_beetle_subject,title,url,playable,cover,id,cover_y,is_new):
        self.rate=rate
        self.cover_x=cover_x
        self.is_beetle_subject=is_beetle_subject
        self.title=title
        self.url=url
        self.playable=playable
        self.cover=cover
        self.id=id
        self.cover_y=cover_y
        self.is_new=is_new
    def __init__(self):
        pass
    def __lt__(self, other):
         return self.score >other.score
