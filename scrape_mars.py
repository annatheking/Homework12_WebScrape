from flask import Flask, jsonify
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
#from browser4 import BeautifulSoup
import requests
import time

# @NOTE: Replace the path with your actual path to the chromedriver
executable_path = {'executable_path': '/Users/shuashua/Documents/Data_Analytic_Boot_Camp/Web/chromedriver.exe'}    
browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    #browser = init_browser()

    ## NASA Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(3)    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find('div',class_="slide")
    news_title = results.find('div', class_="content_title").text
    news_p = results.find('div', class_="rollover_description_inner").text

    ## JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    ft_image = soup.find('a', class_='button fancybox').get('data-fancybox-href')
    featured_image_url = 'https://www.jpl.nasa.gov' + ft_image

    ## Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(3)    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    ## Mars Facts
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    df = pd.DataFrame(table[0])
    df.columns = (['Description', 'Value'])
    html_table = df.to_html()

    ## Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(3)    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('a', class_='itemLink product-item')

    hemisphere_image_urls = []
    for result in results:
    # Error handling
        try:
            # Identify and return title of listing
            if result.h3:
                title = result.h3.text
                #print(title)
            # Identify and return price of listing
                browser.click_link_by_partial_text(title)
                time.sleep(1)
                html = browser.html
                soup = BeautifulSoup(html, 'lxml')
                img_url = soup.find('div', class_='downloads').a['href']
                browser.click_link_by_partial_text('Back')
    
                if (title and img_url):
                    #print('-------------')
                    #print(title)
                    #print(img_url)
                    hemisphere_image_urls1 = {
                                            'title': title,
                                            'img_url': img_url
                                        }
                    hemisphere_image_urls.append(hemisphere_image_urls1)

        except AttributeError as e:
            print(e)
        
    mars_data = {
        'news_title':news_title,
        'news_p':news_p,
        'featured_image_url':featured_image_url,
        'mars_weather':mars_weather,
        'html_table':html_table,
        'hemisphere_image_urls':hemisphere_image_urls
    }
    browser.quit()

    return mars_data
