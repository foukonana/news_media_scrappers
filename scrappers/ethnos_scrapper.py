from requests import get
from bs4 import BeautifulSoup
import numpy as np 
import pandas as pd 
from tqdm import tqdm
import re
import gc
from article_parsers import ethnos_article_parser, save_articles_in_parts


def ethnos_article_links() -> (list, list):
    article_links = []
    broken_pages = []

    page_id = 0

    while True:
        print(page_id)
        page_id += 1
        ethnos_news_by_page = 'https://www.ethnos.gr/politiki?page=' + str(page_id)

        try:
            response = get(ethnos_news_by_page)
            if response.status_code == 503:
                print(f'Broken page: {page_id}')
                # the page is broken 
                broken_pages += [page_id]
                continue
            news_soup = BeautifulSoup(response.text, 'html.parser')
            ethnos_links = ['https://www.ethnos.gr' + link['href'] for link in news_soup.find_all('a', class_='full-link', href=True)[1:]]

            if ethnos_links != []:
                article_links += ethnos_links
            else:
                break
        except Exception as e:
            print(e)
        
    return article_links, broken_pages


if __name__ == "__main__":
    article_links, _ = ethnos_article_links()
    links_df = pd.DataFrame(article_links)
    links_df.to_csv('data/ethnos_links.csv', index=False)

    save_articles_in_parts(links_df, article_parser=ethnos_article_parser, media_name='ethnos')
