from bs4 import BeautifulSoup
import urllib3
import certifi
import re
import sys
import logging


TOP_PAGE_URL = 'https://sota-of-medicalai-test-preview.firebaseapp.com'
ARTICLES_PAGE_URL = 'https://sota-of-medicalai-test-preview.firebaseapp.com/articles'
HEADER = { "User-Agent" :  "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)" }

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where(),
    headers=HEADER)

r = http.request('GET', ARTICLES_PAGE_URL)

soup = BeautifulSoup(r.data, 'html.parser')

links = soup.findAll('a', href=re.compile(r'\/articles\/.+'))
error_counter = 0

for link in links:
    url = TOP_PAGE_URL + link['href']
    r = http.request('GET', url)
    
    soup = BeautifulSoup(r.data, 'html.parser')

    pdflink = soup.find('a', href=re.compile(r'https:\/\/arxiv.org\/.+'))
    pdfurl = pdflink['href']
    r = http.request('GET', pdfurl)
    if (r.status != 200):
        print(r.status)
        error_counter += 1
        logging.error('url %s is invalid!' % pdfurl)

logging.info('%d links are checked' % (len(links) - error_counter))
logging.info('%d links are invalid' % error_counter)

if error_counter > 1:
    sys.exit(1)
