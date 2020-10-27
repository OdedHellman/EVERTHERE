# Web Crawler #
## Overview  ##
The purpose of this crawler is to take a CSV file contains domains of organizations and create a new CSV file that contains for each organization a list of partners domain.


## Running the Crawler ##

The web crawler gets from the user one arguments:
The full path of the input CSV file that contains Two columns: 'Organization Name' and 'Website' (There is an example of an input file called 'Input.csv' at this repo).

* Organization Name - The name of the Company that the crawler will crawl.
* Website - The URL of the home page of 'Organization Name'


## Output ##

The crawler outputs a CSV file.
The output file contains two columns: 'Organization Web Page' and 'Partners Web Page'.

* Organization Web Page - The domain of the website that has been crawled.
* Partners Web Page - domains of the partner’s companies of the appropriate organization.

The output file will be generated/saved in the same directory the app running at. 

## Remarks ##

* This script was created by me in Summer 2019.
* It was created as part of a summer internship at EVERTHERE and I was guided by the CTO & Co-Founder Gabriel Amram and Lead Architect Sofi Vasserman.
* Thank you EVERTHER for letting me this opportunity. It was a great experience to learn from you guys!
