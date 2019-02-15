#!/usr/bin/env python3

import csv
import sys

from uscis_util import wget_json

forms = wget_json('https://egov.uscis.gov/processing-times/api/forms')

form_names = [form['form_name'] for form in forms['data']['forms']['forms']]

form_offices = {name: wget_json('https://egov.uscis.gov/processing-times/api/formoffices/'+name) for name in form_names}

form_office_pairs = [(form, offices['office_code'])
                     for form in form_offices
                     for offices in form_offices[form]['data']['form_offices']['offices']]

processing_times_res = {(form, office): wget_json('https://egov.uscis.gov/processing-times/api/processingtime/%s/%s'%(form, office)) for (form, office) in form_office_pairs}

processing_times_res[('N-400', 'WIC')]['data']['processing_time']['range'][0]['value']

processing_times = {}
for key in processing_times_res:
    ranges = processing_times_res[key]['data']['processing_time']['range']

    if ranges:
        processing_times[key] = sorted([rng['value'] for rng in ranges])


csv_writer = csv.writer(sys.stdout)
csv_header = ['form', 'office', 'min_time', 'max_time']
csv_lines = [[k[0], k[1], processing_times[k][0], processing_times[k][1]] for k in processing_times]

csv_writer.writerows([csv_header] + csv_lines)
