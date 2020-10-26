# Web Crawler #
Oded Hellman
## 
The purpose of this crawler is to generate a CSV file that contains partners domain URLs from an input CSV file contains list of organizations domain URLs.

 
## Running the Crawler ##

The web crawler gets from the user one arguments:
Full path of the input CSV file that contain Two columns: 'Organization Name' and 'Website' (There is an example of input file call 'Input.csv' at this repo).

* Organization Name - The name of the Company that the crawler will crawel.
* Website - The URL of the home page of 'Organization Name'


## Output ##

The crawler outputs a CSV file.
The output file contains two columns: 'Organization Web Page' and 'Partners Web Page'.

* Organization Web Page - The URLs of the website that been crawled.
* Partners Web Page - URLs of the partners companys that been collected from 'Organization Web Page'.

The output file will be generated/saved in the same directory the app runing in. 

## Remarks ##

* This script was created by me in Summer 2018.
* It was created as part of summer internship at EVERTHERE and I was guided by the CTO & Co-Founder Gabriel Amram and Lead Architect Sofi Vasserman.
* It was absolutly great to learn from those Guys!
* Thank you EVERTHER for letting me this Oputionity of learning and develop.
