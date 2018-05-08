import re
import urllib.request as ur
import os
import re
from uuid import uuid4


class Parser:
    """
    This class takes a link to the photo in the instagram,
    and returns a link for downloading this photo.
    """

    def __init__(self, image_url='https://www.instagram.com/p/BhIEHxFBYKX/?taken-by=instagram'):
        """
        Class initialization.

        :param image_url: user instagram image link
        """
        if not isinstance(image_url, str):
            raise ValueError('image url must be str')
        self._url = image_url
        self._bin_site = None

    def _file_opens(self):
        """
        File manipulation from site.

        :return: bytes string
        """
        html = ur.urlopen(self._url).read()  # open html code
        with open('site.html', 'wb') as siteHTML:  # write html code to file
            siteHTML.write(html)
        with open('site.html', 'rb') as site:  # open html code from file
            self._bin_site = site.read()

    def parse(self):
        """
        Parsing image.

        :return: download image url
        """
        self._file_opens()
        str_site = self._bin_site.decode()
        pattern = '"og:image" content="((.)+)"'
        result_url = re.search(pattern, str_site)
        return result_url.group(1)


class Downloader:
    """
    Image downloader.

    Is able to save images in different locations with different name formats.

    param:
        link - direct image URL
        location - save location (defaults to current working directory)
        nameformat - file name format (defaults to numbers)
    """

    def __init__(self, link, location=os.getcwd(), nameformat=str(uuid4().hex) + '.jpg'):
        self.__link = link
        self.__location = location
        self.__iter = 0
        self.__nameformat = nameformat

    @property
    def iter(self):
        return self.__iter

    @iter.setter
    def iter(self, value):
        self.__iter = value

    def download(self):
        """
        Downloads an image
        """
        return ur.urlretrieve(self.__link, self.__location + '\\'
                              + self.__nameformat)


# parser = Parser()
# link = parser.parse()
# print(link)
# load = Downloader(link)
# load.download()