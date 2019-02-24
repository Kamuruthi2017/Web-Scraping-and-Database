
 # Dependencies
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pymongo
import requests

    
def scrape():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=True)

    mars_data={}
    # visit the NASA Mars News site and scrape headlines
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    # Creat BeautifulSoup object
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')
    news_list = nasa_soup.find('ul', class_='item_list')
    first_item = news_list.find('li', class_='slide')
    news_title = first_item.find('div', class_='content_title').text
    news_paragraph = first_item.find('div', class_='article_teaser_body').text
    mars_data["news_title"] =  news_title
    mars_data["news-paragraph"] =  news_paragraph

    # visit the JPL website and scrape the featured image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    html = browser.html
    soup2 = bs(html, 'html.parser')
    lede = soup2.find('figure', class_='lede')
    #print(lede)
    link=lede.a['href']
    featured_image_url='https://www.jpl.nasa.gov' + link
    #print(featured_img_url)
    mars_data['featured_image_url']=featured_image_url

    # visit the mars weather report twitter and scrape the latest tweet
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    time.sleep(1)
    mars_weather_html = browser.html
    mars_weather_soup = bs(mars_weather_html, 'html.parser')

    tweets = mars_weather_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    mars_data["weather_summary"] = mars_weather

    # visit space facts and scrap the mars facts table
    Facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(Facts_url)
    facts_df = table[0]
    facts_df.columns = ["Parameter", "Values"]
    mars_facts_html = facts_df.to_html(header=False, index=False, classes="table")
    mars_data["fact_table"] = mars_facts_html

    # scrape images of Mars' hemispheres from the USGS site
    base_hemisphere_url = "https://astrogeology.usgs.gov"
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html =browser.html
    soup =bs(html, 'html.parser')
    
    hemisphere_image_urls = []

    links = soup.find_all("div", class_="item")

    for link in links:
        img_dict = {}
        title = link.find("h3").text
        next_link = link.find("div", class_="description").a["href"]
        full_next_link = base_hemisphere_url + next_link
        
        browser.visit(full_next_link)
        
        pic_html = browser.html
        pic_soup = bs(pic_html, 'html.parser')
        
        url = pic_soup.find("img", class_="wide-image")["src"]

        img_dict["title"] = title
        img_dict["img_url"] = base_hemisphere_url + url
        
        hemisphere_image_urls.append(img_dict)

        mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data
