from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import gc
from article_parsers import tobhma_article_parser, save_articles_in_parts


def tobhma_article_links() -> list:

    article_links = []

    # hardcoded value, we want to keep only data for the past year
    for page_id in tqdm(range(360), total=360):

        try:
            news_link = 'https://www.tovima.gr/category/politics/page/' + str(page_id)
            response = get(news_link)

            if response.status_code == 200:
                news_soup = BeautifulSoup(response.text, 'html.parser')
                article_links += [link['href'] for link in news_soup.find_all('a', class_='zonabold twenty black-c article-main', href=True)]
            
            else:
                break

        except Exception as e:
                print(e)

    return article_links


if __name__ == "__main__":

    article_links = tobhma_article_links()
    links_df = pd.DataFrame(article_links)
    links_df.to_csv('data/tobhma_links.csv', index=False)

    save_articles_in_parts(links_df, article_parser=tobhma_article_parser, media_name='tobhma')
