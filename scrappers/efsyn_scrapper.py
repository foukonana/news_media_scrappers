from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
from tqdm import tqdm 
import re
import gc
from article_parsers import efsyn_article_parser, save_articles_in_parts


def efsyn_article_links() -> list:

    article_links = []

    # hardcoded value, we want to keep only data for the past year
    for page_id in range(600):
        
        print(page_id)

        try:
            tanea_news_link = 'https://www.efsyn.gr/politiki?page=' + str(page_id)
            response = get(tanea_news_link)

            if response.status_code == 200:
                news_soup = BeautifulSoup(response.text, 'html.parser')
                article_links += ['https://www.efsyn.gr' + link['href'] for link in news_soup.find_all('a', class_='full-link', href=True)[:12]]
            
            else:
                break

        except Exception as e:
                print(e)

    return article_links


if __name__ == "__main__":

    article_links = efsyn_article_links()
    links_df = pd.DataFrame(article_links)
    links_df.to_csv('data/efsyn_links.csv', index=False)

    save_articles_in_parts(links_df, article_parser=efsyn_article_parser, media_name='efsyn')
