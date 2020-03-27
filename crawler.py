import requests
from bs4 import BeautifulSoup
import re
from seed_urls import seed_url_queue_init
from nltk.tokenize import word_tokenize

from inverted_index import reducer, mapper

invertedIndex = {};

def stripTags(soup):
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()

def crawl():
    urls = seed_url_queue_init();
    counter  = 0;
    visited_links = [];
    while counter < 47:
        url = urls[counter];
        if url not in visited_links:
            r = requests.get(url);
            soup = BeautifulSoup(r.content.lower(), 'html.parser');
            containers = soup.find_all('a', attrs={'href': re.compile("^http://")});
            for link in containers:
                urls.append(link.get('href'));
            stripTags(soup);
            text = soup.get_text();
            tokens = word_tokenize(text);
            words_dictionary = mapper('websites',tokens);
            reducer(words_dictionary,invertedIndex,str(url));
            visited_links.append(url);
            counter += 1;
    return [invertedIndex,counter];
