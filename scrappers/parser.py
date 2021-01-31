import gc
import re

import numpy as np

from tqdm import tqdm
from requests import get
from bs4 import BeautifulSoup

class base_parser():

    def __init__(self):
        self.article_links = []
        self.article_main_bodies = []
        self.article_titles = []
        self.article_subtitles = []
        self.article_tags = []
        self.article_upload_times = []
        self.article_update_times = []
        self.article_authors = []

    def _clear(self):

        # clear the lists again to avoid memory issues
        self.article_links = []
        self.article_main_bodies = []
        self.article_titles = []
        self.article_subtitles = []
        self.article_tags = []
        self.article_upload_times = []
        self.article_update_times = []
        self.article_authors = []
        self.data=None
        self.articles_df = None

        gc.collect()  


    def parse(self):
        raise NotImplementedError

    def save_articles(self, links_df, filename):
        i=1

        for row_index, link in tqdm(links_df.iterrows(), total=links_df.shape[0]): 
            try:
               if not self.parse():
                   continue
                    
            except Exception as e:
                print(e)
            
            else:

                self.article_links += [self.article_link]
                self.article_main_bodies += [self.article_main]
                self.article_titles += [self.article_title]
                self.article_subtitles += [self.article_subtitle]
                self.article_tags += [self.article_main_tags]
                self.article_upload_times += [self.article_upl_time]
                self.article_update_times += [self.article_upd_time]
                self.article_authors += [self.article_author]

            # write the data into parts
            if ((row_index+1) % 1200 == 0) or (row_index == links_df.shape[0]-1):
                data = {'links': self.article_links,
                        'title': self.article_titles,
                        'subtitle': self.article_subtitles,
                        'main_text': self.article_main_bodies,
                        'tags': self.article_tags,
                        'author': self.article_authors,
                        'upload_time': self.article_upload_times,
                        'update_time': self.article_update_times,
                        }
                try:
                    articles_df = pd.DataFrame(data=data)
                except Exception as e:
                    print(e)
                else:
                    articles_df.to_csv(filename, index=False)

                    i+=1

                    self._clear()



class kontra(base_parser):

    def parse(self, link):
        article_link = link.values[0]
        article_response = get(article_link)
    
        if article_response.status_code == 200:
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
        else:
            return False

        self.article_main = str(article_soup.find_all('div', property='schema:text')[0])
        # remove HTML from text
        self.article_main = re.sub('\xa0|\n', ' ', re.compile(r'<[^>]+>').sub('', self.article_main)).strip()

        self.article_title = str(article_soup.find_all('title')).split('<title>')[1].split('|')[0].rstrip()
        self.article_subtitle = self.article_main.split('.')[0]

        self.article_main_tags = [str(tag).split('>')[1].split('<')[0] for tag in article_soup.find_all('a', property='schema:about')]

        self.article_upl_time = str(article_soup.find_all('span', property='schema:dateCreated')).split('"')[3]
        # there is no update/ modification time for articles in Kontra 
        self.article_upd_time = np.nan

        self.article_author=np.nan

        return True


# example usage

#
# parser = kontra()
# kontra.save_articles(links_df = df, filename = f"data/kontra_part_{i}.csv")
#
