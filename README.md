### Exploratory analysis of press bias in greek language

Press bias and fake news detection have been really hot topics that the NLP community has been trying to tackle in recent years. Especially in times that major political events are taking place, like the US elections, there is a lot of conversation going on, regarding the quality and authenticity of news. 

Finding quality data for a NLP task is a major obstacle in many research studies. Especially for underrepresented languages, such as Greek, there are not sufficient public datasets. For this project we created our own collection of articles, as we could not find a dataset that met our needs. 

This repo contains scrappers for the 8 major sites that Greeks use to get informed about politics. 

### Set up this project
You will need: 
* Python 3.6 or higher

Create a python virtual environment and activate it then install requirements:
```sh
python3 -m venv news_scrappers_env
source news_scrappers_env/bin/activate
pip install -r requirements.txt
```
