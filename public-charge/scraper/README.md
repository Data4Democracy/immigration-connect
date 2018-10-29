# Scraping comments from regulationsgov

This is an initial attempt to contribute to 
[data for democracy - public charge project](https://github.com/Data4Democracy/immigration-connect/tree/master/public-charge).

The regulations site is rendered using javascript. As such, simple scrapping
tools will fail and thus the use of selenium in this project.

Comments are organized using an ID of the type `USCIS-*`.
To minimize the ammount of request done to the site, we are proposing to get
all USCIS IDs and then use this to get the url for each individual comment.

The url for each comment is of the type `{baseURL}/document?D=USCIS-XXXXXX`.

The current script will print the request uri for the first 50 comments on the
site.

## Installation instructions.
To use this script you will need to have the python 3.x dependencies installed
along with chrome and chrome driver.

To install the python dependencies do:
```
pip install -r requirements.txt
```

For sample chrome and chrome driverinstallation instructions, see 
[How to Setup Selenium with ChromeDriver on Ubuntu 18.04 & 16.04](https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/).

## Resources
Some reference material concerning xpath:
* [xpath tutorial](https://www.w3schools.com/xml/xpath_intro.asp)

* [XPath in Selenium WebDriver: Complete Tutorial](https://www.guru99.com/xpath-selenium.html)
