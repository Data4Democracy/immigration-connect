from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil
import json

def start_driver():
	return webdriver.Firefox()

def get_page_links(driver, rootUrl='https://en.wikipedia.org/wiki/List_of_terrorist_incidents', all_years=map(str, range(1970, 2018))):
	driver.get(rootUrl)
	list_links = driver.find_elements_by_css_selector("div.column-count-3 li a")
	print len(list_links)
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
			f.write(year + ', ' + link + ', ' + text + ('\n' if i != len(links)-1 else ''))

def read_page_links(fn) :
	f = open(fn, 'r')
	data = f.read().split("\n")
	f.close()
	page_links = []
	for val in data:
		val = val.split(", ")
		year = val[0]
		link = val[1]
		text = val[2]
		val_tuple = (year, link, text)
		page_links.append(val_tuple)
	return page_links


def get_all_incidents(driver, page_links):
	all_incidents = {}
	for j, (year, link, text) in enumerate(page_links):
		print 'GETTING PAGE:', j, 'OF', len(page_links)
		driver.get(link)
		all_incidents[text] = get_incidents(driver, link)
		write_all_incidents(all_incidents)
	return all_incidents

def get_incidents(driver, url):
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
				incident[header] = val
			incidents.append(incident)
	return incidents

def write_all_incidents(incidents, outfile='./data/incidents.json'):
	try:
		shutil.rmtree('./data')
	except Exception as e:
		pass
	os.mkdir('./data')
	with open(outfile, 'w') as f:
		json.dump(incidents, f, indent=2)

def main(links_outfile='page-links.txt'):
	driver = start_driver()
	if not os.path.exists(links_outfile):
		page_links = get_page_links(driver)
		write_page_links(page_links, links_outfile)
	page_links = read_page_links(links_outfile)
	incidents = get_all_incidents(driver, page_links)
	write_all_incidents(incidents)
	driver.close()

if __name__ == "__main__" :
	main()