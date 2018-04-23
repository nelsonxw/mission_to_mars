# import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser

def scrape():
    # set up executable path for chromedriver
    executable_path = {'executable_path':'chromedriver'}

    # URL of page to be scraped for news, images, weather and facts
    url_news = 'https://mars.nasa.gov/news/'
    url_featured_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    url_facts = 'http://space-facts.com/mars/'
    url_hemisperes_images = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # use splinter module to retrieve data from websites
    browser = Browser('chrome', **executable_path,headless = True)
    browser.visit(url_news)
    html = browser.html
    # create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html,'html.parser')
    # save news title and paragraph to variables
    news_title = soup.find('div',class_="content_title").a.text.strip()
    news_p = soup.find('div',class_="rollover_description_inner").text.strip()

    browser.visit(url_featured_images)
    html = browser.html
    # create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html,'html.parser')
    # retrieve the data link to the website which has full size image
    url_imagelink = soup.find('footer').a['data-link']
    url_imagelink = 'https://www.jpl.nasa.gov' + url_imagelink

    # visit the linked website and retrieve the url of full size image
    browser.visit(url_imagelink)
    html = browser.html
    # create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html,'html.parser')
    # save the url of featured image to variables
    featured_image_url = soup.find('figure',class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url

    browser.visit(url_weather)
    html = browser.html
    # create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html,'html.parser')
    # save mars weather to variables
    mars_weather = soup.find('div',class_='js-tweet-text-container').p.text.strip()

    # retrieve Mars fact table and read into pandas dataframe
    df = pd.read_html(url_facts)
    facts_table = df[0]
    # add column headers and set index
    facts_table.columns = ['description','value']
    facts_table.set_index('description',inplace=True)
    # save to html tables
    mars_fact = facts_table.to_html(justify='left')

    # retrieve Mars hemisperes images and save to a list of dictionaries
    browser.visit(url_hemisperes_images)
    html = browser.html
    # create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html,'html.parser')
    # create list and dictionary to capture titles and image urls
    img_list = []
    img_dict = {}
    results = soup.find_all('div',class_='item')
    # loop through all scraped items and add them to the dictionary, then add to the list
    for result in results:
        title = result.find('div',class_='description').a.text.strip()
        img_link = 'https://astrogeology.usgs.gov' + result.find('div',class_='description').a['href']
        browser.visit(img_link)
        html = browser.html
        soup = bs(html,'html.parser')
        hemisperes_images_url = 'https://astrogeology.usgs.gov' + soup.find('img',class_='wide-image')['src']
        img_dict = {'title':title,'img_url':hemisperes_images_url}
        img_list.append(img_dict)

    # save all scraped data to a dictionary and return results
    scrape_result = {
    'news_title':news_title,
    'news_p':news_p,
    'featured_image_url':featured_image_url,
    'mars_weather':mars_weather,
    'mars_fact':mars_fact,
    'img_list':img_list
    }
    
    return scrape_result