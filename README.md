# Web Crawler #
## Overview  ##
The purpose of this crawler is to generate a CSV file that contains partners domain URLs from an input CSV file contains a list of organizations domain URLs.

 
## Running the Crawler ##

The web crawler gets from the user one arguments:
The full path of the input CSV file that contains Two columns: 'Organization Name' and 'Website' (There is an example of an input file called 'Input.csv' at this repo).

* Organization Name - The name of the Company that the crawler will crawl.
* Website - The URL of the home page of 'Organization Name'


## Output ##

The crawler outputs a CSV file.
The output file contains two columns: 'Organization Web Page' and 'Partners Web Page'.

* Organization Web Page - The URLs of the website that been crawled.
* Partners Web Page - URLs of the partner’s companies that been collected from 'Organization Web Page'.

The output file will be generated/saved in the same directory the app running in. 

## Remarks ##

* This script was created by me in Summer 2019.
* It was created as part of a summer internship at EVERTHERE and I was guided by the CTO & Co-Founder Gabriel Amram and Lead Architect Sofi Vasserman.
* Thank you EVERTHER for letting me this opportunity.
* It was absolutely great to learn from those guys!



