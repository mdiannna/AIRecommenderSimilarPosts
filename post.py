# python properties, setters: https://www.python-course.eu/python3_properties.php

class Post():
    def __init__(self, img, txt):
        self.__image = img
        self.__text = txt

    @property
    def image(self):
        return self.__image
    
    @property
    def text(self):
        return self.__text

    @image.setter
    def image(self, img):
        self.__image = img

    @text.setter
    def text(self, txt):
        self.__text = txt
