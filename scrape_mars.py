from flask import Flask, jsonify
import pandas as pd
from bs4 import BeautifulSoup
import requests

def scrape():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find('div',class_="slide")
    news_title = results.find('div', class_="content_title").text
    news_p = results.find('div', class_="rollover_description_inner").text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    ft_image = soup.find('a', class_='button fancybox').get('data-fancybox-href')
    featured_image_url = 'https://www.jpl.nasa.gov' + ft_image

    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    df = pd.DataFrame(table[0])
    html_table = df.to_html()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)    
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find_all('a', class_='itemLink product-item')

    hemisphere_image_urls = []
    for result in results:
    # Error handling
    try:
        # Identify and return title of listing
        title = result.h3.text
        # Identify and return price of listing
        img_url = result.img.get('src')

        # Print results only if title, price, and link are available
        if (title and img_url):
            print('-------------')
            print(title)
            print('https://astrogeology.usgs.gov' + img_url)
            hemisphere_image_urls1 = {
                                    'title': title,
                                    'img_url': 'https://astrogeology.usgs.gov' + img_url
                                }
            hemisphere_image_urls.append(hemisphere_image_urls1)
            
    except AttributeError as e:
        print(e)

app = Flask(__name__)

@app.route("/")
def home():
    return()


@app.route("/scrape")
def scrape():
    return ()

if __name__ == "__main__":
    app.run(debug=True)