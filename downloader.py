# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 22:57 2017

@author: Diophantus_
"""

import urllib.request as ur
import os


class Downloader:
    """Image downloader

    Is able to save images in different locations with different name formats.

    param:
        link - direct image URL
        location - save location (defaults to current working directory)
        nameformat - file name format (defaults to numbers)
    """
    def __init__(self, link, location=os.getcwd(), nameformat='numbers'):
        self.__link = link
        self.__location = location
        self.__iter = 0
        self.__filenameformat = eval('self.'+nameformat)()

    def download(self):
        """Downloads an image"""
        return ur.urlretrieve(self.__link, self.__location + '\\'
                              + self.__filenameformat)

    def numbers(self):
        """Generates file names from 1 to n (where n is a number of images)"""
        self.__iter += 1
        return str(self.__iter) + '.jpg'
