from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import gc
from article_parsers import tanea_article_parser, save_articles_in_parts


def tanea_article_links() -> list:
    
    politics_categories = ['parliament', 'government', 'antipoliteysi']

    article_links = []

    for politics_category in politics_categories:
        page_id = 1
        while True:
            print(politics_category, page_id)
            tanea_news_link = 'https://www.tanea.gr/category/politics/' + politics_category + '/page/' + str(page_id)

            try:
                response = get(tanea_news_link)
                if response.status_code == 200:                   
                    news_soup = BeautifulSoup(response.text, 'html.parser')
                    article_links += [link['href'] for link in news_soup.find_all('a', class_='article-title-18 dark-c firamedium nodecor', href=True)]

                    page_id += 1

                else:
                    break

            except Exception as e:
                print(e)
            
    return article_links


if __name__ == "__main__":
    article_links = tanea_article_links()
    links_df = pd.DataFrame(article_links)
    links_df.to_csv('data/tanea_links.csv', index=False)
    
    save_articles_in_parts(links_df, article_parser=tanea_article_parser, media_name='tanea')
