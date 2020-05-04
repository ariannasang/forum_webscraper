# Forum Webscraper
Collects comments, user information, and meta data from two specific online community forums that discuss new child protection laws. *(Site information is protected.)*

This webscraper was built to support faculty research at Wesleyan University within the [Science in Society Program Department](https://www.wesleyan.edu/sisp/). The collected text data will be leveraged to identify ambiguous language in recent child protection laws and to offer revisions to clarify legal documents. 


## Usage
Get all the auxillary links of the forum + download all text and meta data into a CSV file. 
```
git clone https://github.com/ariannasang/forum_webscraper.git
cd forum_webscraper
python main.py
```
To provide your username and password, change ./data/CRD.pw or type on terminal.

```
python main.py yourUsername yourPassword
```


## Toolkit 
* Selenium package 
* ChromeDriver
