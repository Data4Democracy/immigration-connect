#!/usr/bin/env bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/ubuntu/uscis-processing-time

#this runs the uscis-processing-time-api.py scraper, and prints to a csv output file.

today=`date '+%Y%m%d'`; #define today's date

scrape=$(python3 /home/ubuntu/uscis-processing-time/uscis-processing-time-api.py > /home/ubuntu/uscis-processing-time/uscis-processing-time-api_$today.csv) #define command-line function

echo $scrape
