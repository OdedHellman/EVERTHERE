# Web Crawler #
## Overview  ##
This crawler is tasked  with the partnership classification process for thousands of companies.
It takes a CSV file containing organizations' domains and creates a new CSV file that includes a list of partner's domain for each organization.
 
## Running the Crawler ##
 
The web crawler gets from the user one arguments:
An input CSV file contains:
* Organization Name - The name of the organization that the crawler will crawl.
* Website - The domain of 'Organization Name.'

An example of an input file called 'Input.csv' locates at this repo.
 

 
 
## Output ##

The crawler outputs a CSV file that contains two columns:
 
* Organization's Web Page - The domain of the website that has been crawled.
* Partner's Web Page - domains of the partner's companies of the appropriate organization.
 
The output file will be generated/saved in the same directory in which the app is running at.
 
## Remarks ##
 
* This script was created by me in Summer 2019.
* It was created as part of a summer internship at EVERTHERE, and I was guided by the CTO & Co-Founder Gabriel Amram and Lead Architect Sofi Vasserman.
* Thank you EVERTHER for letting me this opportunity. It was a great experience to learn from you guys!

