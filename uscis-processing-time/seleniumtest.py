#!/usr/bin/env python3

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('https://egov.uscis.gov/processing-times/')
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import os
import sys
import subprocess
import pyautogui
import pyperclip
import time

typer = Select(browser.find_element_by_id('selectForm'))
typer.select_by_visible_text('I-90 | Application to Replace Permanent Resident Card')
browser.implicitly_wait(10)
typer = Select(browser.find_element_by_id('officeOrCenter'))
typer.select_by_visible_text('Potomac Service Center')
print([o.text for o in typer.options][1:], file=open('test.txt', 'w'))
button = browser.find_element_by_id('getProcTimes')
button.click()
