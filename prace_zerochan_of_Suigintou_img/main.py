from pathlib import Path
import urllib.request
import requests
import time
import bs4
import itertools


class Zerochan_parce:

    def __init__(self, search_object: str = 'Suigintou', limit_search: int = 1000):
        self.search_object = search_object
        self.limit_search = limit_search
        self.start_url = f'https://www.zerochan.net/search?q={search_object}'
        self.base_headers = {
            'Host': 'www.zerochan.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.zerochan.net/Suigintou',
            'Cookie': 'PHPSESSID=rgdsq2dv6k7j4lj539mmc4df3r; v3=0; z_theme=1; cookienotice=1; __utma=7894585.1325381327.1635266487.1635266487.1635266487.1; __utmb=7894585.5.10.1635266487; __utmc=7894585; __utmz=7894585.1635266487.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __gads=ID=55c46e3eb86dcff0-22fa16a6ffca00ab:T=1635266489:RT=1635266489:S=ALNI_MalsqeKAjkf-ZTPqxpEpYZk1Jvrcw',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers'
        }
        self.iters = itertools.count(1)
        self.current_url = ''

    def _response(self, url: str, headers: dict, n=1):
        if n > 5:
            print("Can't get a response from the server")
            return "Error"
        try:
            response = requests.get(url=url, headers=headers)
            return response.text
        except:
            time.sleep(2)
            headers[
                'Cookie'] = 'PHPSESSID=rgdsq2dv6k7j4lj539mmc4df3r; v3=0; z_theme=1; cookienotice=1; __utma=7894585.1325381327.1635266487.1635266487.1635266487.1; __utmb=7894585.5.10.1635266487; __utmc=7894585; __utmz=7894585.1635266487.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __gads=ID=55c46e3eb86dcff0-22fa16a6ffca00ab:T=1635266489:RT=1635266489:S=ALNI_MalsqeKAjkf-ZTPqxpEpYZk1Jvrcw'
            self._response(url=url, headers=headers, n=n + 1)

    def _soup(self, url: str, headers: dict):
        try:
            soup = bs4.BeautifulSoup(self._response(url=url, headers=headers))
            if soup is not None:
                return soup
            else:
                print("Error getting data from BeautifulSoup")
                return "Error"
        except:
            print("Error getting data from BeautifulSoup")

    def _get_number_of_pages(self):
        soup = self._soup(url=self.start_url, headers=self.base_headers)
        try:
            number_of_pages = soup.find(name="p", attrs={'class': "pagination"}).text.split("\t")[1].split()[-1]
            if number_of_pages is not None:
                return number_of_pages
            else:
                print("Error getting the number of pages")
                return "Error"
        except:
            print("Error getting the number of pages")

    def _save_image(self, url: str):
        path = Path(Path.cwd() / "images")
        if not path.is_dir():
            path.mkdir()
        path = Path(path / f'{self.search_object}')
        if not path.is_dir():
            path.mkdir()
        n = next(self.iters)
        try:
            resource = urllib.request.urlopen(url)
        except:
            try:
                time.sleep(5)
                resource = urllib.request.urlopen(url)
            except:
                return
        img = open(path / f'{self.search_object}_{n}.jpg', 'wb')
        img.write(resource.read())
        img.close()

    def _get_images_links(self, url: str, headers: dict):
        soup = self._soup(url=url, headers=headers)
        try:
            all_images = soup.find(name="ul", attrs={'id': "thumbs2"}).find_all(name="li")
        except AttributeError:
            return
        for image in all_images:
            try:
                link = image.find("p").find("a").get("href")
                self._save_image(link)
            except AttributeError:
                continue

    def run(self):
        number_of_pages = int(self._get_number_of_pages())
        for page_number in range(1, number_of_pages + 1):
            if page_number == 1:
                self.current_url = self._soup(url=self.start_url, headers=self.base_headers).find(name="link", attrs={
                    "rel": "canonical"}).get("href")
                self._get_images_links(url=self.start_url, headers=self.base_headers)
            else:
                url = f'{self.current_url}?p={page_number}'
                ref = f'{self.current_url}?p={page_number - 1}'
                ref = ref.replace("(", "%28")
                ref = ref.replace(")", "%29")
                sub_headers = {
                    'Accept': 'image/avif,image/webp,*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Connection': 'keep-alive',
                    'Cookie': 'z_theme=1; cookienotice=1; __utma=7894585.1325381327.1635266487.1635329517.1635333910.4; __utmz=7894585.1635266487.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=55c46e3eb86dcff0-22fa16a6ffca00ab:T=1635266489:RT=1635266489:S=ALNI_MalsqeKAjkf-ZTPqxpEpYZk1Jvrcw; PHPSESSID=ftakjbubargblui6qqrd6egeec; v3=0; __utmc=7894585; __utmb=7894585.40.10.1635333910',
                    'Host': 'www.zerochan.net',
                    'Referer': f'{ref}',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'TE': 'trailers',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
                }
                self._get_images_links(url=url, headers=sub_headers)


test = Zerochan_parce()
test.run()
