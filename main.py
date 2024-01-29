from webscraper import scrape_website, HeadlineScraper


# Vytvoření instance scraperu a spuštění
def test():
    url = 'https://www.sspu-opava.cz/zpravy'  # Nahraďte skutečnou URL
    # TODO: Najdi chybu na dalších řádcích
    scraper = HeadlineScraper()
    scrape_website()
    save_to_json()
    # TODO: Proveď testovací download libovolných souborů ze školního webu
    # TODO: Proveď testovací download fotek ze školních zpráv

    for obj in scraper.data:
        print(obj)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
