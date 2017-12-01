from urllib.request import urlopen
import re


class Parser:
    """This class takes a link to the photo in the instagram,
    and returns a link for downloading this photo."""

    def __init__(self, image_url):
        """Class initialization.

        :param image_url: user instagram image link
        """
        if not isinstance(image_url, str):
            raise ValueError('image url must be str')
        self._url = image_url
        self._bin_site = None

    def _file_opens(self):
        """File manipulation from site.

        :return: bytes string
        """
        html = urlopen(self._url).read()  # open html code
        with open('site.html', 'wb') as siteHTML:  # write html code to file
            siteHTML.write(html)
        with open('site.html', 'rb') as site:  # open html code from file
            self._bin_site = site.read()

    def parse(self):
        """Parsing image.

        :return: download image url
        """
        self._file_opens()
        str_site = self._bin_site.decode()
        pattern = '"og:image" content="((.)+)"'
        result_url = re.search(pattern, str_site)
        return result_url.group(1)


if __name__ == '__main__':
    pass
