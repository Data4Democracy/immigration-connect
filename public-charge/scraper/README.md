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
### Developers
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

### Running container without Make

Build the container image:
```
docker build --force-rm \
    --build-arg USER=$USER --build-arg=$UID \
    -f Dockerfile -t regulationsgov .
```

Run the container:
```
docker run --rm -it \
    --net host \
    --security-opt seccomp=chrome.json \
    --shm-size=2g \
    -e DISPLAY=${DISPLAY} \
    -v $(CURDIR):/opt/app \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    regulationsgov bash
```

### Scraping comments
To start scraping comments you can run the `get_comments.py` script:
```
python get_comments.py
```

This will populate a sqlite database called `comments.sql`.
If you didn't set the same `UID` in the container as the one you are using in 
your host machine, then for the database to work, you'll have to set the 
permissions for your current working directory to be writen to by `others`:
```
cd ../
chmod o=u scraper/
```

Then you are all set.

#### Inspecting the database
To see whats in the database, you can do something like this:
```python
from get_comments import Base, Comment                                          
from sqlalchemy import create_engine                                            
from sqlalchemy.orm import sessionmaker                                         
                                                                                
engine = create_engine('sqlite:///comments.sqlite')                             
Base.metadata.bind = engine                                                     
DBSession = sessionmaker()                                                      
DBSession.bind = engine                                                         
session = DBSession()                                                           
                                                                                
session.query(Comment).filter(Comment.uscisid == "USCIS-2010-0012-7079").one()
```

## Resources
Some reference material concerning xpath:
* [xpath tutorial](https://www.w3schools.com/xml/xpath_intro.asp)

* [XPath in Selenium WebDriver: Complete Tutorial](https://www.guru99.com/xpath-selenium.html)

* [How to Setup Selenium with ChromeDriver on Ubuntu 18.04 & 16.04](https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/)

* [Introductory Tutorial of Python’s SQLAlchemy](https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/)
