#!/usr/bin/env python
#coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pandas as pd

# Function to initiate splinter
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

#define a scrape function that takes 
def scrape_sites():
    
    # Create a dictionary for all of the scraped data
    mars_data = {}

    # ----------------------------------------------------------- #
    # -------------------------  NEWS --------------------------- #
    # ----------------------------------------------------------- #

    # URL of mars news page to scrape
    url = 'https://mars.nasa.gov/news/'
    # Use Requests to retreive the page
    response = requests.get(url)

    # BeautifulSoup object to parse with html.parser 
    soup = BeautifulSoup(response.text, 'html.parser')

    # Examine the soup to determine which elements needed (News Title & Paragraph)
    # Use chrome inspector to find tag and class to 'find_all' elements
    #print(soup.prettify())

    # Assign variable for results- this is a list of each slide which can be iterate through
    news_results = soup.find_all('div', class_="slide")
    #len(news_results)
    #news_results

    # lists to hold results
    news_title = []
    news_para = []


    # iterate through the list of slides
    for result in news_results:
        title = result.find('div', class_= 'content_title').find('a').text
        news_title.append(title)
        
        paragraph = result.find('div', class_='rollover_description_inner').text
        paragraph = paragraph.replace("\n", "")
        news_para.append(paragraph)

    # append to mars dictionary (only need the first-- most recent item)
    mars_data['news_title'] = news_title[0]
    mars_data['summary'] = news_para[0]


    # print(news_title)
    # print('------------------------')
    # print(news_para)

# ----------------------------------------------------------- #
# ----------------  JPL Featured Space Image ---------------- #
# ----------------------------------------------------------- #

    # Use splinter to go to browser and click through to scrape
    browser = init_browser()


    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    # Click image on landing page
    button = browser.find_by_id('full_image')
    button.click()

    # Click more info to go to full size image
    button_2 = browser.find_by_text('more info     ')
    button_2.click()

    # click on the main image to open in it's own browser
    # find_by_css function uses .class_name
    button_3 = browser.find_by_css('.main_image')
    button_3.click()


    # Find .jpg link with soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_page = soup.find_all('img')


    for image in image_page:
        #print(image['src'])
        featured_image_url = image['src']
    
    browser.quit()
    # add to dictionary
    mars_data['featured_image_url']= featured_image_url

    
    # ----------------------------------------------------------- #
    # ----------------------  Mars Weather ---------------------- #
    # ----------------------------------------------------------- #
    #scrape the latest Mars weather tweet 

    url3 = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url3)

    # BeautifulSoup object to parse with html.parser 
    soup = BeautifulSoup(response.text, 'html.parser')
    tweets = soup.select("div.js-tweet-text-container")
    recent_tweet= tweets[0]
    mars_weather = recent_tweet.find('p', class_='TweetTextSize').text

    #add to mars_data
    mars_data['mars_weather'] = mars_weather

    # ----------------------------------------------------------- #
    # --------------------- Mars Data Table --------------------- #
    # ----------------------------------------------------------- #
    url4 = 'https://space-facts.com/mars/'
    response = requests.get(url4)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Use read_html to get all tables from url
    table=pd.read_html(url4)
    # First table is where information is held
    mars_df=table[0]
    mars_df.rename(columns={
    0: 'Facts',
    1: 'Value'  
    })

    # to_html writes table back to html table code
    mars_html=mars_df.to_html
    
    mars_data['Mars_table'] = mars_html


    # ----------------------------------------------------------- #
    # --------------------Mars Hemispheres----------------------- #
    # ----------------------------------------------------------- #

    #Empty list to hold dictionary for each hemisphere 
    hemisphere_image_urls= []

    # Iterate through entire webpage to scrape data from each of 4 images
    for x in range(0,4):

        # Use splinter to click on each image link and store in empty dictionary
        browser = init_browser()
        url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url5)

        # BS to parse through webpage
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Click on image reate list to hold all images to click
        hemispheres = browser.find_by_css('.thumb')
        hemispheres[x].click()


        #On new page scrape title and image
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        #Use BS to find text from title and href from image 
        title = soup.find('h2','title').text
        img_url = soup.find('div','downloads').find_all('a')[1]['href']

        #{"title": "Valles Marineris Hemisphere", "img_url": "..."}
        dictionary = {'title':title,'img_url':img_url}
        hemisphere_image_urls.append(dictionary)
        print(f'Complete ({x+1}/4)')

        

        browser.quit()
    #append to dictionary (list of dictionary is the value)
    mars_data['Hemispheres'] = hemisphere_image_urls

    #return the dictionary in the end
    return mars_data
    

scrape_sites()


#DICTIONARY:
#NEWS: 
    #'news_title' = news_title[0]
    #'summary' = news_para[0]

#JPL IMG:
    # {featured_image_url: 'url'}

#TWEET WEATHER:
    #{mars_weather: mars_weather tweet}

# MARS DATA TABLE
    # {Mars_table: mars_html}

#HEMISPHERES:
    #{Hemsipheres: [{title, img_url}]}






