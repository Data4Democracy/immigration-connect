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
forms = [o.text for o in typer.options]
for form in forms[1:3]:
    typer.select_by_visible_text(form)
    browser.implicitly_wait(10)
    typer2 = Select(browser.find_element_by_id('officeOrCenter'))
    centers = [o.text for o in typer2.options]
    for center in centers[1:]:
        print(center)
        #print([o.text for o in typer.options][1:], file=open('test.txt', 'w'))
        typer2.select_by_visible_text(center)
        #typer.select_by_visible_text('center')
        button = browser.find_element_by_id('getProcTimes')
        button.click()
browser.close()
