from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm
import json
import re
import gc
from article_parsers import skai_article_parser, save_articles_in_parts


def skai_article_links() -> list:
    article_links = []

    # hardcoded value, we want to keep only data for the past year
    for page_id in tqdm(range(650), total=650):

        try:
            # the link is for search window
            news_link = 'https://www.skai.gr/s/%CE%A0%CE%9F%CE%9B%CE%99%CE%A4%CE%99%CE%9A%CE%97?page=' + str(page_id)
            response = get(news_link)

            if response.status_code == 200:
                news_soup = BeautifulSoup(response.text, 'html.parser')
                
                # not all articles returned are for politics, we keep only those
                article_links += [link['href'] for link in news_soup.find_all('a', class_='title mainLink', href=True)
                                    if 'politics' in link['href']]
            
            else:
                break

        except Exception as e:
                print(e)

    return article_links


if __name__ == "__main__":

    article_links = skai_article_links()
    links_df = pd.DataFrame(article_links)
    links_df.to_csv('data/skai_links.csv', index=False)

    save_articles_in_parts(links_df, article_parser=skai_article_parser, media_name='skai')
    
