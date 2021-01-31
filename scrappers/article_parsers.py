from bs4 import BeautifulSoup
from requests import get
import numpy as np 
import pandas as pd
import bs4
import re 
from tqdm import tqdm 
import json
import gc


def efsyn_article_parser(article_soup: bs4.BeautifulSoup) -> dict:

    article_main = str(article_soup.find_all('div', 'article__body js-resizable')).split('"article__body js-resizable">')[1].split('<div class="adv adv--full" id="article_end">')[0]
    # clear the HTML tags
    article_main = re.sub('\s+', ' ', re.sub('\xa0|\n', ' ', re.compile(r'<[^>]+>').sub(' ', article_main))).strip()

    article_title = str(article_soup.find_all('meta', property="og:title")).split('"')[1]
    article_subtitle = str(article_soup.find_all('meta', property="og:description")).split('"')[1]

    article_main_tags = [tag.split('>')[1].split('<')[0] for 
                            tag in str(article_soup.find_all('div', class_="article__tags")).split('<li>')[1:]]

    # these data can be loaded into a dictionary 
    json_dict = json.loads(''.join(article_soup.find('script', {'type':'application/ld+json'}).contents))['@graph'][0]
    article_upl_time = json_dict['datePublished']
    article_upd_time = json_dict['dateModified']
    
    author = article_soup.find_all('div', class_='article__author')
    if author != []:
        # sometimes authors have a link for their name
        article_author = str(author).split('<span>')[1].split('</span>')[0].strip()
        article_author = re.compile(r'<[^>]+>').sub(' ', article_author).strip()
    else:
        article_author = np.nan
    
    parsed_article_dict = {'title': article_title,
                           'subtitle': article_subtitle,
                           'main_text': article_main,
                           'tags': article_main_tags,
                           'author': article_author,
                           'upload_time': article_upl_time,
                           'update_time': article_upd_time,
                            }
    
    return parsed_article_dict


def ethnos_article_parser(article_soup: bs4.BeautifulSoup) -> dict:

    article_main = article_soup.find_all('div', class_ = 'article__main')
    # remove HTML tags and link to the ETHNOS app
    # some images have source, that should be removed
    if 'figcaption' in article_main:
        article_main_txt = BeautifulSoup(article_main)
        article_main_txt.figcaption.clear()
        article_main = str(article_main_txt)
    article_main = re.sub('\s+', ' ', re.sub('ΚΑΤΕΒΑΣΤΕ ΤΟ ΝΕΟ APP ΤΟΥ ΕΘΝΟΥΣ', '', re.sub('\xa0', ' ', re.compile(r'<[^>]+>').sub(' ', str(article_main))))).strip()
    
    article_title = str(article_soup.find_all('meta',  property="og:title")).split('"')[1]
    article_subtitle = str(article_soup.find_all('meta', property="og:description")).split('"')[1]

    article_main_tags = [str(x).split('"')[1] for x in article_soup.find_all('meta', property='article:tag')]

    article_upl_time = str(article_soup.find_all('time', class_ = 'article__date')).split('"')[3]
    article_upd_time = article_soup.find_all('time', class_ = 'article__update-time')
    # update time of the article is not always available
    if article_upd_time != []:
        article_upd_time = str(article_upd_time).split('"')[3]
    else:
        article_upd_time = np.nan
    
    article_author = str(article_soup.find_all('a', class_ = 'article__author')).split('<span>')[1].split('<')[0]
    if article_author == 'Newsroom':
        article_author = np.nan
    
    parsed_article_dict = {'title': article_title,
                           'subtitle': article_subtitle,
                           'main_text': article_main,
                           'tags': article_main_tags,
                           'author': article_author,
                           'upload_time': article_upl_time,
                           'update_time': article_upd_time,
                            }
    
    return parsed_article_dict


def kathimerini_article_parser(article_soup: bs4.BeautifulSoup) -> dict:

    s = article_soup.find_all('script', {'type':'application/ld+json'})
    json_dict = json.loads(''.join(s[np.argmax([len(str(x)) for x in s])].contents))

    article_main = json_dict['articleBody']
    # Remove any tags
    article_main = re.sub('\xa0|\r|\n', ' ', article_main).strip()

    article_title = json_dict['headline']
    article_subtitle = json_dict['description']

    article_main_tags = [json_dict['keywords']]

    article_upl_time = json_dict['datePublished']
    article_upd_time = json_dict['dateModified']

    article_author = json_dict['author'][0]['name']
    if article_author == 'Newsroom':
        article_author = np.nan

    parsed_article_dict = {'title': article_title,
                           'subtitle': article_subtitle,
                           'main_text': article_main,
                           'tags': article_main_tags,
                           'author': article_author,
                           'upload_time': article_upl_time,
                           'update_time': article_upd_time,
                            }
    
    return parsed_article_dict


def kontra_article_parser(article_soup: bs4.BeautifulSoup) -> dict:

    article_main = str(article_soup.find_all('div', property='schema:text')[0])
    # remove HTML from text
    article_main = re.sub('\xa0|\n', ' ', re.compile(r'<[^>]+>').sub(' ', article_main)).strip()

    article_title = str(article_soup.find_all('title')).split('<title>')[1].split('|')[0].rstrip()
    article_subtitle = article_main.split('.')[0]

    article_main_tags = [str(tag).split('>')[1].split('<')[0] for tag in article_soup.find_all('a', property='schema:about')]

    article_upl_time = str(article_soup.find_all('span', property='schema:dateCreated')).split('"')[3]
    # there is no update/ modification time for articles in Kontra 
    article_upd_time = np.nan

    # there is no way to extract the author of kontra articles, it is incorporated in the main text
    article_author=np.nan

    parsed_article_dict = {'title': article_title,
                           'subtitle': article_subtitle,
                           'main_text': article_main,
                           'tags': article_main_tags,
                           'author': article_author,
                           'upload_time': article_upl_time,
                           'update_time': article_upd_time,
                            }
    
    return parsed_article_dict


def protothema_article_parser(article_soup: bs4.BeautifulSoup) -> dict:

    json_dict = json.loads(''.join(article_soup.find('script', {'type':'application/ld+json'}).contents))

    article_main = re.sub('  ', ' ', re.sub('\r|\n|\xa0', ' ', json_dict['articleBody'])).strip()

    article_title = json_dict['alternativeHeadline']
    article_subtitle = json_dict['description'].split('|')[0].strip()

    article_main_tags = [dict['name'] for dict in json_dict['about']][:-1]

    article_upl_time = json_dict['dateCreated']
    article_upd_time = json_dict['dateModified']

    # not all articles have author (when they don't, author does not appear in the dictionary)
    try:
        article_author = json_dict['editor'][0]['name']
    except KeyError:
        article_author = np.nan

    parsed_article_dict = {'title': article_title,
                           'subtitle': article_subtitle,
                           'main_text': article_main,
                           'tags': article_main_tags,
                           'author': article_author,
                           'upload_time': article_upl_time,
                           'update_time': article_upd_time,
                            }
    
    return parsed_article_dict


def skai_article_parser(article_soup: bs4.BeautifulSoup) -> dict:

    s = article_soup.find_all('script', {'type':'application/ld+json'})
    json_dict = json.loads(''.join(s[np.argmax([len(str(x)) for x in s])].contents))

    article_main = json_dict['articleBody']
    # clean the text
    article_main = re.sub('\xa0|\r|\n', ' ', article_main).strip()

    article_title = json_dict['headline']
    article_subtitle = json_dict['description']

    tags = article_soup.find_all('div', class_="tags")
    if tags != []:
        article_main_tags = [tag.split('>')[1].split('<')[0] for tag in str(tags).split('hreflang')[1:]]
    else:
        article_main_tags = np.nan

    article_upl_time = json_dict['datePublished']
    article_upd_time = json_dict['dateModified']
    
    article_author = json_dict['author']['name']
    if article_author == 'ΣΚΑΪ':
        article_author = np.nan

    parsed_article_dict = {'title': article_title,
                           'subtitle': article_subtitle,
                           'main_text': article_main,
                           'tags': article_main_tags,
                           'author': article_author,
                           'upload_time': article_upl_time,
                           'update_time': article_upd_time,
                            }
    
    return parsed_article_dict


def tanea_article_parser(article_soup: bs4.BeautifulSoup) -> dict:
    
    article_main = str(article_soup.find_all('meta')).split('var text = ')[1].split(' var tags')[0]
    # clean text specific occurencies
    article_main = re.sub('  ', ' ', re.sub('\n|\xa0|\';', ' ', article_main)).split('Πηγή:')[0].strip()

    article_title = str(article_soup.find_all('meta', itemprop="headline")).split('"')[1]
    article_subtitle = str(article_soup.find_all('meta', property='og:description')).split('"')[1]

    article_main_tags = [str(tag).split('"')[1] for tag in article_soup.find_all('meta', property='article:tag')]

    article_upl_time = str(article_soup.find_all('meta', property="article:published_time")).split('"')[1]
    article_upd_time = article_soup.find_all('meta', property="article:modified_time")
    if article_upd_time != []:
        article_upd_time = str(article_soup.find_all('meta', property="article:modified_time")).split('"')[1]
    else:
        article_upd_time = np.nan

    article_author = str(article_soup.find_all('meta', itemprop="author")).split('"')[1]
    if article_author == 'tanea.gr':
        article_author = np.nan
    
    parsed_article_dict = {'title': article_title,
                           'subtitle': article_subtitle,
                           'main_text': article_main,
                           'tags': article_main_tags,
                           'author': article_author,
                           'upload_time': article_upl_time,
                           'update_time': article_upd_time,
                            }
    
    return parsed_article_dict


def tobhma_article_parser(article_soup: bs4.BeautifulSoup) -> dict:
    
    article_main = str(article_soup.find_all('script')).split('var text =')[1].split('var tags')[0].strip()
    article_main = re.sub('\xa0|\';', ' ', article_main).split('Πηγή:')[0].strip()

    article_title = str(article_soup.find_all('meta', itemprop='headline')).split('"')[1]
    article_subtitle = str(article_soup.find_all('meta', property='og:description')).split('"')[1]

    # not all articles have tags
    tags = article_soup.find_all('ul', class_="nom urltags uppercase")
    if tags != []:
        article_main_tags = [tag.split('>')[1].split('</')[0] for tag in str(tags).split('<li>')[1:]]
    else:
        article_main_tags = np.nan

    article_upl_time = str(article_soup.find_all('meta', property = 'article:published_time')).split('"')[1]
    # not all articles have update time
    upd_time = article_soup.find_all('meta', property = 'article:modified_time')
    if upd_time != []:
        article_upd_time = str(upd_time).split('"')[1]
    else:
        article_upd_time = np.nan

    author = str(article_soup.find_all('span', class_='fn', itemprop='author'))
    # there are times that a link directs you to other articles of the author
    if 'href' in author:
        article_author = author.split('title="')[1].split('">')[0]
    else:
        article_author = author.split('"author">')[1].split('</span>')[0].strip()
        if article_author == 'ΤοΒΗΜΑ Team':
            article_author = np.nan

    parsed_article_dict = {'title': article_title,
                           'subtitle': article_subtitle,
                           'main_text': article_main,
                           'tags': article_main_tags,
                           'author': article_author,
                           'upload_time': article_upl_time,
                           'update_time': article_upd_time,
                            }
    
    return parsed_article_dict


def save_articles_in_parts(links_df: pd.DataFrame, article_parser: callable, media_name: str) -> None:
    
    # initiate with empty dictionary 
    dict_inputs = ['links', 'title', 'subtitle', 'main_text', 'tags', 'author', 'upload_time', 'update_time']
    data_dict = {name:[] for name in dict_inputs}

    save_part_index = 1

    for row_index, link in tqdm(links_df.iterrows(), total=links_df.shape[0]): 

        try:
            article_link = link.values[0]
            article_response = get(article_link)
        
            if article_response.status_code == 200:
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
            else:
                continue

            parsed_article_dict = article_parser(article_soup)
            parsed_article_dict['links'] = article_link
            
        except Exception as e:
            print(e)
        
        else:           
            # update the dictionary values
            for key in dict_inputs:
                data_dict[key].append(parsed_article_dict[key])

        # write the data into parts
        if ((row_index+1) % 1200 == 0) or (row_index == links_df.shape[0]-1):

            try:
                articles_df = pd.DataFrame(data=data_dict)
            except Exception as e:
                print(e)
            else:
                articles_df.to_csv(f'data/{media_name}_part_{save_part_index}.csv', index=False)

                save_part_index += 1

                # clear the dictionary to avoid memory issues
                data_dict = {name:[] for name in dict_inputs}
                articles_df = None

                gc.collect()
