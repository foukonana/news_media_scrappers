from selenium import webdriver
from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
import pandas as pd 
import numpy as np
import json
import re
import gc 
from article_parsers import kathimerini_article_parser, save_articles_in_parts


def kathimerini_article_links() -> list:

    # change the location of the driver to your own
    driver = webdriver.Chrome('C:/Users/anast/Downloads/chromedriver_win32/chromedriver')

    try:
        kathimerini_news_url = 'https://www.kathimerini.gr/category/politics/'
        driver.get(kathimerini_news_url)
        # wait before starting to click the botton, so that the page is loaded
        driver.implicitly_wait(10)
    
    except Exception as e:
        print(f'Exception: {e} \noccured when trying to open a chrome driver for the politics section in Kathimerini.')

    # different try to click the page for more articles
    try:
        for n in tqdm(range(8, 1494, 6)): 
            #the xpath here is from the load more button
            clicker = driver.find_element_by_xpath(f'//*[@id="content-wrap"]/main/div[3]/div[2]/div/div[{n}]/div/a').click()
            # let it wait in-between clicks
            # driver.implicitly_wait(2)

    except Exception as e:
        print(f'Exception {e} \noccured when loading more articles in the politics section in Kathimerini.')
    
        continue
    
    news_soup = BeautifulSoup(driver.page_source, 'html.parser')

    article_links = [link.split(">")[0] for link 
                in str(news_soup.find_all('div', class_='article_thumbnail_wrapper')).split('href="')[1:]]

    return article_links


if __name__ == "__main__":

    article_links = kathimerini_article_links()
    links_df = pd.DataFrame(article_links)
    links_df.to_csv('data/kathimerini_links.csv', index=False)

    save_articles_in_parts(links_df, article_parser=kathimerini_article_parser, media_name='kathimerini')
