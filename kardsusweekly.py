#!/usr/bin/env python
import csv
import datetime
from dateutil import parser
import urllib2
from bs4 import BeautifulSoup



ARTICLE_CSV = 'usweekly-articles.csv'
TEXT_CSV = 'usweekly-text.csv'

def download_url (article_url):
    """Download article_url and return the title, date, and text."""

    soup = BeautifulSoup(urllib2.urlopen(article_url).read(),'html.parser')

    title = soup.h1.contents[0]


    article_date = soup.time.contents[0]
    try:
        article_date = parser.parse(article_date, fuzzy=True)
    except:
        print('ERROR ON', article_date)
        raise


    article_text = soup.main
    for aside in article_text.find_all("aside"):
        aside.extract()


    return (title, article_date, article_text.get_text())

with open (ARTICLE_CSV, 'rU') as file_in:
    with open (TEXT_CSV, 'w') as file_out:
        reader = csv.reader (file_in)
        writer =csv.writer (file_out)

        writer.writerow (['url', 'title', 'date', 'text'])
        reader.next()
        for row in reader:
            url = row [1]
            print (url)
            title, date, text = download_url (url)
            writer.writerow ([
                url,
                title.encode ('utf8'),
                date,
                text.encode ('utf8'),
                ])
