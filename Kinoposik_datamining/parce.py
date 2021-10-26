import requests
import bs4
import time

class Parce_kinopoisk:
    start_url = 'https://www.kinopoisk.ru/lists/api/top500/?exclude_viewed=0&page=1&quick_filters=&sort&tab=all'
    headers = {
        'Host': 'www.kinopoisk.ru',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.kinopoisk.ru/lists/top500/?page=2&tab=all',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'x-request-id': '1635246856472658-9739950981332801865',
        'uber-trace-id': '3bf392c59737e037:953925d60323357e:0:1',
        'Connection': 'keep-alive',
        'Cookie': 'user-geo-region-id=53; user-geo-country-id=2; desktop_session_key=a1f81a7a59dcbd71ce0fd13f9f283875ba3d82980d674c15e46ca8c8c5c6ac7cf36fc758aa92cf423a4d40e657318f86b67ca56178f719716ec3c5b67b54fe8fe3754d72d8ad38075d1a6023678809bbc7b53b49aabdefd95af7aa37e3440bbd; desktop_session_key.sig=S6pA5mO7Ydqq5jnKLk3e_cnokHg; i=ve5TWXK4YElfnRtc9PkutC8bVQqF9GcpRQRy/FOmVVi1qR3Lyq046iKP/5HCs/Mxo6sKg0IZiiQdPQsFoS92+9YKHts=; mda_exp_enabled=1; gdpr=0; _ym_uid=1635242718971899368; _ym_d=1635246858; _ym_isad=2; cycada=GLukYClOVGi7KT/v/FOWwgV2hnjxKHol2l9mSC4j9H0=; ya_sess_id=noauth:1635242780; yandex_login=; ys=c_chck.1720205667; yandexuid=8539613471635242710; mda2_beacon=1635242780909; sso_status=sso.passport.yandex.ru:synchronized; _ym_visorc=b; spravka=dD0xNjM1MjQ1NDY5O2k9MzcuMTEzLjY2Ljk2O0Q9MTZDRUVCNDQzOEVBMjgxNDdFODQ0MzI3Q0M3MTk3MUZBOUEzNDQ5MTg5QzhENEY4Q0RCMkVERjlERkY2NEZGN0E4Rjk7dT0xNjM1MjQ1NDY5ODA5MjAzOTYyO2g9NmM2MTMzZjljOTNkMjNkMDUxZTY2MjczYTIyY2Y5NjU=; yandex_plus_metrika_cookie=true',
        'TE': 'Trailers'
    }
    def __init__(self,
                 start_url='https://www.kinopoisk.ru/lists/top500/tab=all',
                 domen='https://www.kinopoisk.ru/'):
        self.start_url = start_url
        self.domen = domen
        self.links.add(start_url)

    def _response(self, url, n=0):

        try:
            time.sleep(1)
            response = requests.get(url=url, headers=self.headers)
            return response.text
        except:
            if n > 5:
                print('The number of request attempts has been exceeded. The program terminated abnormally.')
            time.sleep(5)
            print(f'Error response.\n'
                  f'URL:{url}\n'
                  f'Status code{requests.get(url=url, headers=self.headers).status_code}')
            self._response(url, n=n+1)
    def _soup(self, url):
        soup = bs4.BeautifulSoup(self._response(url=url))
        return soup

    def _get_all_films_in_page(self, url):
        soup = self._soup(url=url)
        films_list = soup.find_all(name="div", attrs={'data-tid':'af76fbb3'})
        return films_list

    def _get_film_data(self, stock_data):
        link = self.domen + stock_data.find(name="a",  attrs={"class":"selection-film-item-meta__link"}).get("href")
        rus_name = stock_data.find(name="p",  attrs={"class":"selection-film-item-meta__name"}).text
        original_name = stock_data.find(name="p",  attrs={"class":"selection-film-item-meta__original-name"}).text.split(',')[0]
        years = int(stock_data.find(name="p",  attrs={"class":"selection-film-item-meta__original-name"}).text.split(',')[-1])
        contry_contry = stock_data.find_all(name="span",  attrs={"class":"selection-film-item-meta__meta-additional-item"})
        contry = contry_contry[0].text
        genres = contry_contry[1].text
        rating = stock_data.find(name="span",  attrs={"class":"rating__value rating__value_positive"}).text
        return link, rus_name, original_name, years, contry, genres, rating

    def _iter_films_in_page(self, url):
        all_films = self._get_all_films_in_page(url)
        for film in all_films:
            print(self._get_film_data(film))

    def run(self):
        self._iter_films_in_page(self.start_url)






parce = Parce_kinopoisk()
x = parce.run()