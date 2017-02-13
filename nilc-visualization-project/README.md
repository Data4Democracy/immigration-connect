# National Immigration Law Center (NILC) Visualization Project

An interactive immigration-related arrest and detention map built for the NILC.

## Project Authors

* [Tyler Richards](https://github.com/tylerjrichards)
* [Scott Came](https://github.com/scottcame)

## Problem Statement

The NILC has been begun receiving reports of immigration-related arrests and detentions. In light of recent executive orders and the current political rhetoric regarding immigration, it is imperative that the NILC be able to track these incidents in real-time. Data for Democracy was recruited to build an interactive map which meets the following guidelines:

1. Shows the location of incidents on a interactive map.
2. Shows number of people impacted at that incident
3. Map is updated when new data is added
4. Maps also displays some basic statistics:
  * total number of incidents
  * incidents in last 24 hours

## Data

NILC staff receives and collects reports about incidents. The staff then inputs data about the incidents into a Google Sheet. Each incident is described as follows:

* ID
  * Unique identifier for each incident
* Date
* Local Time
* Name/Description
* Street Address
* Location (optional)
  * If no street address is available, a general description of the location (e.g. Downtown Atlanta)
* Min-Persons
  * The minimum number of persons affected by the incident
* Max-Persons
  * The maximum number of persons affected by the incident

## Solution

Data is processed and geocoded using R. The final visualization is built using the Leaflet package and saved as an HTML widget. A Domino run is triggered every 10 minutes, pulling new data from the NILC's Google Sheet and updating the live visualization on the website.

## Deployment

The final product is deployed at the [site-tbd]().


<img src="images/logos/r_logo.png" width="120">
<img src="images/logos/r_studio_logo.png" width="120">
<img src="images/logos/leaflet_logo.png" width="120">
