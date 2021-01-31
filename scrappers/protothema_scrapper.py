from selenium import webdriver
from bs4 import BeautifulSoup
from requests import get
import time
from tqdm import tqdm 
import pandas as pd 
import numpy as np
import re
import json
import gc
from article_parsers import protothema_article_parser, save_articles_in_parts


def protothema_article_links() -> list:

    # Web scrapper for infinite scrolling page 
    driver = webdriver.Chrome(executable_path=r"C:/Users/anast/Downloads/chromedriver_win32/chromedriver.exe")
    # search for articles inside a search bar, because otherwise not all are loaded
    driver.get("https://www.protothema.gr/anazitisi/?q=%CF%80%CE%BF%CE%BB%CE%B9%CF%84%CE%B9%CE%BA%CE%AE&Category=2&Order=Recent")
    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

    try:
        
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        # scroll_height = driver.execute_script("return document.body.scrollHeight;")  

    # pracrtically scroll until no more scroll is possible
    except Exception as e:
        print(f'Exception {e} \noccured when loading more articles in the politics section in ProtoThema.')  
        continue
    
    # create a beautifoul soup from the articles loaded in the page
    news_soup = BeautifulSoup(driver.page_source, 'html.parser')

    article_links = [str(link).split('href="')[1].split('">')[0] 
            for link in news_soup.find_all('span', class_='update_well') 
                if '2020' in str(link).split('" title="')[1].split(',')[0] and 'href' in str(link)]

    return article_links


if __name__ == "__main__":

    article_links = protothema_article_links()
    links_df = pd.DataFrame(article_links)
    links_df.to_csv('data/protothema_links.csv', index=False)

    save_articles_in_parts(links_df, article_parser=protothema_article_parser, media_name='protothema')
    