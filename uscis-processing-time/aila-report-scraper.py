#!/usr/bin/env python3

import urllib
import re
import datetime
import os.path

from uscis_util import wget, wget_soup

DOWNLOAD_DIR = 'aila-processing-time-reports/'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

forms = ['CSC', 'NBC', 'NSC', 'TSC', 'VSC', 'YSC', 'AAO', 'EB-5']

aila_prefix = 'https://www.aila.org'
form_index_prefix = aila_prefix + '/infonet/processing-time-reports/'

print('Retrieving overview indexes for each office...')
form_index_soups = [wget_soup(form_index_prefix + form) for form in forms]
print('Found', len(form_index_soups), "\n")

year_index_paths = [link['href'] for soup in form_index_soups
                                 for link in soup.select('#leftnav li a')]

print('Retrieving yearly indexes for each office...')
year_index_soups = [wget_soup(aila_prefix + path) for path in year_index_paths]
print('Found', len(year_index_soups), "\n")

report_paths = [link['href'] for soup in year_index_soups
                             for link in soup.select('.child h3 a')]

print('Retrieving report pages for each office/date...')
report_urls = [(path, aila_prefix + path) for path in report_paths]
report_soups = []
n_report_soups = 0
for (path, report_url) in report_urls:
    report_soups.append((path, wget_soup(report_url)))
    n_report_soups += 1
    if n_report_soups % 50 == 1:
        print('... [%s] retrieved %d of %d report pages...' % (datetime.datetime.now(), n_report_soups, len(report_urls)))

pdf_paths = [(path, soup.select('.postinfo a.bluebtn')[0]['href']) for (path, soup) in report_soups if len(soup.select('.postinfo a.bluebtn')) > 0]
print('Found', len(pdf_paths), "with pdfs\n")

print('Retrieving reports pdfs for each office/date ', datetime.datetime.now(),'...')
n_pdfs = 0
for (report_path, pdf_path) in pdf_paths:
  sections = report_path.split('/')
  office = sections[3]
  date_match = re.search('(\d\d?)-(\d\d?)-(\d\d?)(.*)', sections[-1])
  if date_match:
    date_ints = tuple([int(x) for x in [date_match.group(3), date_match.group(1), date_match.group(2)]])
  else:
    date_ints = (n_pdfs, n_pdfs, n_pdfs)
  filename = office+'_%02d-%02d-%02d.pdf'%date_ints
  pdf_url = aila_prefix + pdf_path
  n_pdfs += 1
  if not os.path.isfile(DOWNLOAD_DIR+filename):
    print("[%04d/%04d] Downloading %s => %s" % (n_pdfs, len(pdf_paths), pdf_url, filename))
    urllib.request.urlretrieve(pdf_url, DOWNLOAD_DIR+filename)
print("Finished downloading pdfs", datetime.datetime.now())

