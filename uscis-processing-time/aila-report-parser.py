#!/usr/bin/env python3

DOWNLOAD_DIR = 'aila-processing-time-reports/'

#ysc_17-03-14.pdf
#filename = DOWNLOAD_DIR+'vsc_14-12-23.pdf'
filename = DOWNLOAD_DIR+'tsc_09-01-27.pdf'


import re

#import tabula
#df = tabula.read_pdf(filename)
#df[['Form', 'Processing Cases As Of Date:']]

import textract
text = textract.process(filename).decode('utf-8')

# works for ysc_17-03-14.pdf
#proc_line_regex = re.compile(r"((I[-­]\d\d\w*)\s+(?:Petition|Application).*?(?:199|200|201)\d)", re.MULTILINE | re.DOTALL)

# works mostly for ysc_17-03-14.pdf and vsc_14-12-23.pdf, but screws up first row
#proc_line_regex = re.compile(r"((I[-­]\d\d\w*)\s+(?:Consideration|Petition|Application).*?(?:199\d|200\d|201\d|Months))", re.MULTILINE | re.DOTALL)

# works for ysc_17-03-14.pdf and vsc_14-12-23.pdf
#form = '[A-Z][-­]\d\d\w*'
#date = '(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w* \d\d?, (?:199|200|201)\d'
#duration = '\d+.?\d* (?:Months|Years|Days)'
#
#proc_line_regex = re.compile(f"(({form})\s.*?\s({date}|{duration}))", re.MULTILINE | re.DOTALL)

form = '[A-Z][-­]\d\d\w*'
date = '(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w* \d\d?, (?:199|200|201)\d'
duration = '\d+.?\d* (?:Months|Years|Days)'

proc_line_regex = re.compile(f"(({form})\s.*?\s({date}|{duration}))", re.MULTILINE | re.DOTALL)

[print(len(x[0]), " | ", x[1], " | ", x[2], ) for x in proc_line_regex.findall(text)]


print(text)


