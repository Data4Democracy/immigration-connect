# Scraping comments from regulationsgov

This is an initial attempt to contribute to 
[data for democracy - public charge project](https://github.com/Data4Democracy/immigration-connect/tree/master/public-charge).

The regulations site is rendered using javascript. As such, simple scrapping
tools will fail and thus the use of selenium in this project.

Comments are organized using an ID of the type `USCIS-*`.
To minimize the amount of request done to the site, we are proposing to get
all USCIS IDs and then use this to get the url for each individual comment.
The url for each comment is of the type `{baseURL}/document?D=USCIS-XXXXXX`.
To get all the USCIS IDs and use them to form urls for the comments directly,
one can use the [`Scraper.get_comments_urls_on_page(page_number)`](./main.py) 
method.


Using the scraper, one can output all the pertinent information for each
comment for all comments on the first page by doing something like this:
```python
# Start a scraper and set a page laod delay of 4 seconds.
scraper = Scraper(delay=4)                                                 

# Get comment urls on first page.                                           
urls = scraper.get_comments_urls_on_page(1)

for url in urls:
    print(scraper.scrape_comment(comment_url=url))

scraper.shut_down()
```

## Setup instructions
You can use the Docker container to run the scrpaer.
The [container](./Dockerfile) downloads chrome, chrome driver, and install all
python dependencies.

We recommed you use the [Makefile](./Makefile) to build and run the
container.
Running,
```
$ make shell
```

will put you inside the container in an interactive session.


## Resources
Some reference material concerning xpath:
* [xpath tutorial](https://www.w3schools.com/xml/xpath_intro.asp)

* [XPath in Selenium WebDriver: Complete Tutorial](https://www.guru99.com/xpath-selenium.html)

* [How to Setup Selenium with ChromeDriver on Ubuntu 18.04 & 16.04](https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/)
