import os
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup


# Abstraktní třída WebScraper
class WebScraper(ABC):

    def __init__(self, url):
        self.url = url
        self._data = None

    @property
    def data(self):
        return self._data

    def fetch_content(self):
        # TODO: Aktivuj další dva řádky, pokud nelze načíst data z uvedené URL adresy
        # response = requests.get(self.url, headers={
        #     'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
        response = requests.get(self.url)
        return BeautifulSoup(response.content, 'html.parser')

    @abstractmethod
    def parse_content(self, soup):
        pass

    def scrape(self):
        soup = self.fetch_content()
        self.parse_content(soup)
        return self.data

    def save_to_json(self, file_name):
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            print(f"Data successfully saved to {file_name}")
        except IOError as e:
            print(f"An IOError occurred: {e.strerror}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # TODO: Vytvoř analogickou funkci pro uložení dat do CSV souboru

    @staticmethod
    def download_files(file_urls, folder_path='downloads'):
        # Zkontrolujte, zda složka existuje, a pokud ne, vytvořte ji
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for file_url in file_urls:
            try:
                # Získání obsahu obrázku
                response = requests.get(file_url)
                response.raise_for_status()  # Zkontroluje, zda nedošlo k chybě při stahování

                # Vytvoření názvu souboru z poslední části URL a případné úpravy pro unikátnost
                # TODO: Najdi logickou chybu v následujícím řádku
                file_name = os.path.join(folder_path, file_url.split('/'))

                # Uložení obrázku do souboru
                with open(file_name, 'wb') as f:
                    f.write(response.content)

                print(f"Image successfully downloaded: {file_name}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download image {file_url}: {e}")


# Konkrétní třída pro scraping titulků z příkladové novinové stránky
class HeadlineScraper(WebScraper):

    def parse_content(self, soup):
        headlines = soup.find_all('h1')  # Předpokládáme, že titulky jsou v tagu <h1>
        self._data = [headline.text.strip() for headline in headlines]
        return


class NewsScraper(WebScraper):

    def parse_content(self, soup):
        articles = []
        # Vyhledání všech bloků článků
        for blog_post in soup.find_all('div', class_='single-blog-post pb-0'):
            # Extrahování titulku
            title = blog_post.find('h3').text.strip()
            # Extrahování URL odkazu
            link = blog_post.find('h3').find('a')['href'].strip()
            # Extrahování autora
            author = blog_post.find('div', class_='post-meta').find('a').text.strip()
            # Extrahování data
            date = blog_post.find('div', class_='post-meta').find('p').contents[0].strip(' ,\n')
            # Extrahování obsahu článku
            content = blog_post.find('div', class_='text-justify').text.strip()
            # Extrahování adresy fotek
            # TODO: Extrahuj adresy fotek, které jsou v záhlaví školních zpráv
            # Přidání slovníku do seznamu článků
            articles.append({
                'title': title,
                'author': author,
                'date': date,
                'url': link,
                'content': content,
                # TODO: Přidej adresy fotek, které jsou v záhlaví školních zpráv
            })
        self._data = articles
        return


# TODO: Získej data TOP 100 filmů na stránce https://www.csfd.cz/zebricky/filmy/nejlepsi/

# Použití polymorfismu
def scrape_website(scraper):
    return scraper.scrape()


