# DocketSync
Download and synchronize comments from dockets on https://regulations.gov

`docketsync` is a Python 3.6+ script that allows users to download comment
metadata, text, and attachments from the https://regulations.gov website. With
command line flags, users can specify the docket ID from which comments should
be downloaded, filter by the date range that comments were posted to the
website, and the file format that downloaded comments should be save to on
local disk (SQLite database or CSV file).

## Getting Started

The `docketsync` script can either be run from a local Python3 installation on
your computer or from a Python3 installation in a Docker container running on
your computer. The details below outline the steps necessary to get
`docketsync` running using either of these two options. Before running the
script, you will need to have an API key for the https://regulations.gov
website and a local copy of this GitHub repository.

### Setting up the API Key

Save your https://regulations.gov API key to an environment variable named
`REGULATIONS_GOV_API_KEY`.  See the [Getting an API Key](#Getting-an-API-Key)
section for more details on how to get an API key.

```
export REGULATIONS_GOV_API_KEY="1234567890"
```

### Cloning the repository

Make sure you also have a copy of this repository. You can get a copy by
executing the following commands in your terminal.

```
git clone https://github.com/Data4Democracy/immigration-connect immigration-connect
cd immigration-connect/public-charge;
```

Ensure file permissions are properly set. Sometimes after doing a `git clone`,
executable files don't have the proper file permissions. Use the following
command to make sure the `docketsync` and `docketsync-run` scripts are
executable.

```
chmod 755 docketsync docketsync-run
```

### Option 1: Running `docketsync` with a local Python3 installation

You will need to following commands and resources available on your system to
run `docketsync` in your local Python3 installation:

* bash
* python 3.6+
* pipenv
* API key from https://regulations.gov

Use `pipenv` to setup a virtual environment with dependency Python packages and
enter into the environment's shell.

```
# setup the virtual environment
pipenv install

# enter the virual environment
pipenv shell
```

Run `docketsync` from the command line:

```
./docketsync \
  --save-db comments_2018-11-06.db \
  --save-csv comments_2018-11-06.csv \
  --posted-date 11/06/18
```

This command will produce 3 files and a directory:

1. comments_2018-11-06.db - an SQLite database file with comment metadata and text
2. comments_2018-11-06.csv - a comma separated value file with comment metadata and text
3. comments.log - a docketsync log file
4. attachments - a directory with files that were attached to the comment records.


### Option 2: Running `docketsync` in a Docker container with `docketsync-run`

You will need to following commands and resources available on your system to
run `docketsync` in the `d4d/docketsync` Docker container:

* bash
* docker
* API key from https://regulations.gov

The `d4d/docketsync` Docker image has a pre-installed Python 3.6+ interpreter
and all of the packages necessary to run `docketsync`. The image also
includes a copy of the `docketsync` program. You can build the Docker image
by either using the `build` target in the Makefile:

```
make build
```

Or with the `docker build` command:

```
docker build -t d4d/docketsync .
```

The `docketsync-run` script contains all of the settings and commands necessary
to run `docketsync` inside of the Docker image that was just built. The script
accepts the same command line arguments as `docketsync`.

Run `docketsync` inside of a Docker container with the following command:

```
./docketsync-run \
  --save-db comments_2018-11-06.db \
  --save-csv comments_2018-11-06.csv \
  --posted-date 11/06/18
```

This command will produce 3 files and a directory:

1. comments_2018-11-06.db - an SQLite database file with comment metadata and text
2. comments_2018-11-06.csv - a comma separated value file with comment metadata and text
3. comments.log - a docketsync log file
4. attachments - a directory with files that were attached to the comment records.


## Getting an API Key

https://regulations.gov API keys allow users to access the website's HTTP API
to retrieve data. At the time of writing, the API keys are based on
https://data.gov API keys that have been authorized for use on the
https://regulations.gov website. The authorization process involves:

1. Registering for a https://data.gov website key, at
   https://api.data.gov/signup/, with a business or education email address.
   Gmail, Yahoo, and Outlook email addresses are not accepted by
   https://regulations.gov.

2. Send your API key to regulations@erulemakinghelpdesk.com asking for them to
   authorize your API key for use on the https://regulations.gov website.


## Common Usage Scenarios

The scenarios listed below demonstrate common tasks that can be performed with
the `docketsync` or `docketsync-run` commands. In the examples, the
`docketsync` command will be used, for simplicity, but can just as easily be
substituted with the `docketsync-run` command. Both commands accept the same
flags.

The default action of `docketsync` is to download comments, for docket id
`USCIS-2010-0012`, that were posted to the website yesterday. There is no
default save option, so either the `--save-db` or `--save-csv` flags will need
to be set. If neither save flag is set, the results will not be saved.

### List the `docketsync` help message and all of the flags

```
./docketsync --help
```

### Download comments posted yesterday, save to SQLite database

Download comments, from docket id `USCIS-2010-0012` (the default docket id),
posted to the website yesterday. Save comment metadata and text to an SQLite
database named `comments.db`.

```
./docketsync --save-db comments.db
```

### Download comments from a specific docket id

Download comments from docket id `CFTC-2018-0079-0001`, posted to the website
yesterday. Save comment metadata and text to an SQLite database named
`comments.db`.

```
./docketsync --docket CFTC-2018-0079-0001 --save-db comments.db
```

### Download comments posted yesterday, save to a comma separated value file

Download comments posted to the website yesterday. Save comment metadata and
text to a comma separated value file named `comments.csv`.

```
./docketsync --save-csv comments.csv
```

### Download comments posted on a specific date

Download comments posted to the website on November 06, 2018. Save comment
metadata and text to an SQLite database named `comments.db`.

```
./docketsync --save-db comments.db --posted-date 11/06/18
```

### Download comments posted within a specific date range

Download comments posted to the website from November 01, 2018 through November
30, 2018. Save comment metadata and text to an SQLite database named
`comments.db`.

```
./docketsync --save-db comments.db --posted-date 11/01/18-11/30/18
```

### Load previously downloaded comments and download new comments

Load an SQLite database file, named `comments_2018-11-01_2018-11-05.db`, that
holds previously downloaded comment metadata and text, and download new
comments posted to the website on November 06, 2018. Save the old and new
comment metadata and text to an SQLite database named
`comments_2018-11-01_2018-11-06.db`.

```
./docketsync \
  --load-db comments_2018-11-01_2018-11-05.db \
  --save-db comments_2018-11-01_2018-11-06.db \
  --posted-date 11/06/18
```

### Load previously downloaded comments and check for missed comments

Load an SQLite database file, named `comments_2018-11-01_2018-11-30.db`, that
holds previously downloaded comment metadata and text, and check that all
comments posted to the website from November 01, 2018 through November 30, 2018
are captured in the database. Download only the comments missing from the
database. Save the old and new comment metadata and text to an SQLite database
named `comments_2018-11-01_2018-11-30.db`.

```
./docketsync \
  --load-db comments_2018-11-01_2018-11-30.db \
  --save-db comments_2018-11-01_2018-11-30.db \
  --posted-date 11/01/18-11/30/18
```


