# DocketSync
Download and synchronize comments from dockets on https://regulations.gov

## Quick Start

To run `docketsync`, you will need:

* Python 3.6+
* pipenv
* API key from https://regulations.gov

```
# setup your https://regulations.gov API key in an environment variable
export REGULATIONS_GOV_API_KEY="1234567890"

# setup the virtual environment
pipenv install

# enter the virual environment
pipenv shell

# run the code
./docketsync --save-db comments_2018-11-06_2018-11-06.db --save-csv comments_2018-11-06_2018-11-06.csv --posted_date 11/06/18
```
