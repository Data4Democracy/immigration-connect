from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil
import re
import json
import argparse
from jsonschema import validate

'''
========================
	DATA SCHEMA
========================

{
	"Injured: 
	"Dead": 
	"Location":  
	"Date":  
	"Perpetrators": 
	"Type": 
	"Details": 
}

If any of the data does not fit the schema, an integer entry is given None, 
and a string entry is given "Not Applicable"

'''
def start_driver():
	return webdriver.Firefox()

def get_page_links(driver, ROOT_URL, years, list_links):
	all_years = map(str, years)
	driver.get(ROOT_URL)
	list_links = driver.find_elements_by_css_selector(list_links)
	page_links = []
	for j, link in enumerate(list_links):
		for year in all_years:
			if year in link.text and 'List of terrorist incidents in' in link.text:
				link_tuple = (year, link.get_attribute("href").encode('ascii', 'ignore'), link.text.encode("ascii", "ignore"))
				page_links.append(link_tuple)
				continue
	return page_links

def write_page_links(links, outfile):
	with open(outfile, 'w') as f:
		for i, (year, link, text) in enumerate(links):
			line = '{},{},{}\n'.format(year, link, text)
			f.write(line)

def read_page_links(filename) :
	page_links = []
	with open(filename, 'r') as f:
		for line in f:
			data = line.split(',')
			link = data[1]
			text = data[2]
			page_links.append((link, text))
	return page_links

def get_all_incidents(driver, page_links, outfile, data_keys):
	all_incidents = {}
	for i, (link, text) in enumerate(page_links):
		print 'GETTING PAGE #{} OF {}'.format(i+1, len(page_links))
		all_incidents[text] = get_incidents(driver, link, data_keys)
		write_all_incidents(all_incidents, outfile)
	return all_incidents

def get_incidents(driver, url, data_keys):
	driver.get(url)
	tables = driver.find_elements_by_css_selector('table.wikitable')
	incidents = []
	for table in tables:
		## need to sort out edge case where table has no header
		try:
			headerRow = table.find_element_by_css_selector("thead")
		except Exception as e:
			continue
		headers = headerRow.find_elements_by_css_selector("th")
		headerVals = []
		for header in headers:
			headerVals.append(header.text)
		tableBody = table.find_element_by_css_selector("tbody")
		tableRows = tableBody.find_elements_by_css_selector("tr")
		tableVals = []
		for row in tableRows:
			tableRow = []
			for entry in row.find_elements_by_css_selector("td"):
				tableRow.append(entry.text)
			tableVals.append(tableRow)
		for row in tableVals:
			incident = {}
			for val, header in zip(row, headerVals):
				if header in data_keys:
					incident[header] = val
			## make the empty values equal to "Not Available"
			for key in data_keys:
				if key not in incident:
					incident[key] = "Not Available"
			incidents.append(incident)
	return incidents

def write_all_incidents(incidents, outfile):
	try:
		shutil.rmtree('./data')
	except Exception as e:
		pass
	os.mkdir('./data')
	with open(outfile, 'w') as f:
		json.dump(incidents, f, indent=2)

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--root-url', help='Specify the base url for which to gather links.\n Default for Terrorism Scrape is https://en.wikipedia.org/wiki/List_of_terrorist_incidents', type=str, required=False)
	parser.add_argument('-o', '--outfile', help='Specify the outpath for the data to be written to', type=str, required=True)
	parser.add_argument('-y', '--years', nargs='+', help='Specify the years for which to get the data (multiple arguments accepted)', type=int, required=True)
	parser.add_argument('-l', '--list-links', help='Specify the css selector for which the page links are gathered\n Default is "div.column-count-3 li a"', type=str, required=False)
	parser.add_argument('-k', '--data-keys', help='Specify the data keys to gather, from the list [Injured, Dead, Location, Date, Perpetrators, Type, Details]', type=str, required=False, nargs='+')
	return parser.parse_args()

def write_incidents_to_csv(incidents, outfile, data_keys):
	headers = ['Dataset'] + sorted(data_keys)
	with open(outfile, 'w') as f:
		f.write(', '.join(headers))
		for dataset, data_values in incidents.iteritems():
			for data in data_values:
				assert(sorted(data.keys()) == sorted(data_keys))
				row_values = [re.sub('\n', '', dataset)]
				for header in headers[1:]:
					row_values.append(re.sub('\n', '', data[header].encode('ascii', 'ignore')))
				f.write(', '.join(row_values)+'\n')
			
def main():
	args = parse_arguments()
	links_outfile = args.outfile.split(".json")[0]+'.txt'
	csv_outfile = args.outfile.split(".json")[0]+'.csv' 
	driver = start_driver()
	if args.root_url is None:
		ROOT_URL = 'https://en.wikipedia.org/wiki/List_of_terrorist_incidents'
	else:
		ROOT_URL = args.root_url 
	if args.list_links is None:
		list_links = "div.column-count-3 li a"
	else:
		list_links = args.list_links
	page_links = get_page_links(driver, ROOT_URL, args.years, list_links)
	write_page_links(page_links, links_outfile)
	page_links = read_page_links(links_outfile)
	if args.data_keys is None:
		data_keys = ['Injured', 'Dead', 'Location', 'Date', 'Perpetrators', 'Type', 'Details']
	else:
		data_keys = args.data_keys
	incidents = get_all_incidents(driver, page_links, args.outfile, data_keys)
	write_all_incidents(incidents, args.outfile)
	write_incidents_to_csv(incidents, csv_outfile, data_keys)
	driver.close()

if __name__ == "__main__" :
	main()