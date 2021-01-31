from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import gc
from article_parsers import kontra_article_parser, save_articles_in_parts


def kontra_article_links() -> list:
    article_links = []

    # searching in a predefined range, to get links of up to a year back
    for page_id in tqdm(range(360), total=360):

        try:

            news_link = 'https://kontranews.gr/politiki?page=' + str(page_id)
            response = get(news_link)

            if response.status_code == 200:
                news_soup = BeautifulSoup(response.text, 'html.parser')
                article_links += ['https://kontranews.gr/' + str(link).split('href=')[1].split('"')[1] 
                            for link in news_soup.find_all('div', class_='post-link hidden')]
            
            else:
                break

        except Exception as e:
                print(e)

    return article_links


if __name__ == "__main__":

    article_links = kontra_article_links()
    links_df = pd.DataFrame(article_links)
    links_df.to_csv('data/kontra_links.csv', index=False)

    save_articles_in_parts(links_df, article_parser=kontra_article_parser, media_name='kontra')
