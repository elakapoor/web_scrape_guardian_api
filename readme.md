<h1>Web scraping and case study using Guardian API</h1>
<p>The app is created in pycharm using python, pandas and plotly</p>
<h3>Table of Content</h3>

* [General Info](#general-info)
* [Requirements](#requirements)
* [Setup](#setup)
* [File Structure](#file-structure)
* [File Output](#file-output)
* [Automate Email](#automate-email)

## General info
The project uses the Guardian API for the web scraping of all articles related to Justin Trudeau.
It then store these articles in the csv format. The pandas library is used for the data
analysis and plotly is used for the data visualization.

### Web Scrapping the data
Guardian API is a very interactive API and helps to understand the API structure easily.
With the help of requests and python library it is easy to download the data for the search term.
The structure of the post helps you to select the required columns for the analysis. These
columns could be selected and then appended using the python functionalities.

### Data Analysis
When the articles are saved as a dataframe it is present locally and could be used for any
analysis purposes. With the help of plotly, interactive graphs are created.

### Automatic Email
As a step further, the application also provide you with the facility to automatically send 
the updated info to the users automatically. The email and mime functionality of 
internet data handling python library allows you to easily attach an image or send a html text
to the users automatically.
	
## Requirements
Project uses:
* backports.zoneinfo==0.2.1
* backports.zoneinfo==0.2.1
* certifi==2021.10.8
* chardet==4.0.0
* charset-normalizer==2.0.12
* crontab==0.23.0
* idna==3.3
* kaleido==0.2.1
* numpy==1.21.5
* pandas==1.3.5
* pip==21.1.2
* plotly==5.6.0
* python-dateutil==2.8.2
* pytz==2022.1
* pytz-deprecation-shim==0.1.0.post0
* requests==2.27.1
* setuptools==57.0.0
* six==1.16.0
* soupsieve==2.3.1	
* tenacity==8.0.1
* tzdata==2022.1
* tzlocal==4.1
* urllib3==1.26.9
	
## Setup
To run this project, download it and run python filename.py from the same directory

```
$ cd ../CaseStudy
$ python filename.py

```
## File structure
The repository consist of three .py files namely:
1. collect_article.py
2. automate_alert.py
3. full_automate.py
4. CaseStudy.ipynb

<b>collect_article.py: </b>  This file will collect all the data using API, analyze the data
and then save plots created in the same directory. It will also save the scrapped data.

<b>automate_alert.py: </b> This file will collect the saved file in the same directory and send the data to
the users in the receiving list. The data is sent as an attached image file as well as
html content.

<b>full_automate.py: </b> This file will collect the data and send it to receiver. It is the
combination of above two steps. But it will not go in detail analysis as done by the 
collect_article.py file. The objective of the file is to send the updated data to the users.

<b>CaseStudy.ipynb: </b> This file shows the step by step data collection process and analysis done.

## File Output
When the collect_article.py file is executed the outputs in form of csv files and jpeg images are created.
Following are the description of each output:
1. <b>articles_justin_trudeau 2022-04-03.csv:</b> csv file consist of data collected during web scraping.
2. <b>number_of_articles_published.csv: </b> The file tells about the number of articles published per day
3. <b>article_numbers_2022-04-03.jpeg: </b> The number of articles published over time.
4. <b>articles_more_than_mean.jpeg: </b> Graph shows mean of number article published.
5. <b>articles_with_outliers.jpeg: </b> Graph shows the distribution when number of articles published are different from normal.

## Automate Email
To automate sending e-mails at specific times, for example every day at 9 a.m, we can use Crontab.
```
-crontab -l # this command line will show you all running crons
- crontab -e # this command line will let you edit crons
# past this command line to run your python script every day at 9.am
- 0 9 * * * python3 filename.py
```
