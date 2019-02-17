#!/usr/bin/env python3

import glob
import re
import textract
import csv
import dateparser

DOWNLOAD_DIR = 'aila-processing-time-reports/'

files = glob.glob(DOWNLOAD_DIR+"*.pdf")

r_form = '[A-Z][-­]\d\d\w*'
r_date = '(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w* \d\d?,\s(?:199|200|201)\d'
r_duration = '\d+.?\d* (?:Months|Years|Days)'

def posted_date(text, basename):
    matches = re.findall(f'(?:as of:?|Posted) ({r_date})', text)

    date_str = ''
    if len(matches) > 0:
        date_str = matches[0]
    else: # if the date isn't found in the text, extract it from the filename
        match = re.match('.*_(\d\d-\d\d-\d\d)', basename)
        if match:
            group = match.group(1)
            if group[0] in ['0', '1']:
                date_str = '20'+group
            else:
                date_str = '19'+group

    return date_str

def sanitize(text):
    #starts = ['Processing Cases As Of Date:', 'Processing\s?Timeframe']
    #ends = ['Contact Us']

    removals = [f'Last Updated: {r_date}', f'Form {r_form}']

    sanitized = text
    for removal in removals:
        sanitized = re.sub(removal, 'XXXXXXXX_REMOVED_XXXXXXXX', sanitized)

    return sanitized

def parse_table(text):
    proc_line_regex = re.compile(f"(({r_form})\s.*?(?:\s)({r_date}|{r_duration}))", re.MULTILINE | re.DOTALL)

    lines = []
    for match in proc_line_regex.findall(text):
        lines.append({'form': match[1], 'time': match[2], 'capture_size': len(match[0])})

    return lines

def read_pdf(filename):
    try:
        return textract.process(filename).decode('utf-8')
    except KeyboardInterrupt:
        raise
    except:
        print('Exception processing', filename)
        return ''

with open('aila-pdf-times.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow(['form', 'wait_days', 'ahead_of_schedule', 'processing_date', 'file', 'posted_date', 'capture_size'])

    i = 0
    for filename in [DOWNLOAD_DIR+'tsc_13-04-03.pdf']:
    #for filename in files:
        i += 1
        if i % 100 == 1:
            print("Parsing pdf %d of %d"%(i, len(files)))

        basename = re.match('.*/(.*).pdf', filename).group(1)

        text = read_pdf(filename)

        raw_posted = posted_date(text, basename)
        posted = dateparser.parse(raw_posted)
        now = dateparser.parse('now')

        #print('posted', posted)

        sanitized = sanitize(text)

        lines = parse_table(sanitized)

        for line in lines:
            normed_date = dateparser.parse(line['time'])

            is_relative = re.match(r_duration, line['time']) != None
            if is_relative:
                time_delta = (now - normed_date)
                date_res = posted - time_delta
                wait_time = time_delta
            else:
                date_res = normed_date
                wait_time = posted - normed_date


            #print('date', date_res, is_relative, line['time'])

            csv_writer.writerow([line['form'], wait_time.days, is_relative, date_res.strftime("%Y-%m-%d"), basename, posted.strftime("%Y-%m-%d"), line['capture_size']])

print('Done parsing pdfs')


