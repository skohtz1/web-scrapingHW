from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    url_nasa = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # Retrieve page with the requests module
    response_nasa = requests.get(url_nasa)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup_nasa = BeautifulSoup(response_nasa.text, 'html.parser')
    
    ##finding the title and summary of first article
    results_titles = soup_nasa.find_all('div', class_='content_title')
    summaries = soup_nasa.find_all("div", class_ = "rollover_description_inner")
    title_first = results_titles[0].text.strip()
    summaries_first = summaries[0].text.strip()
    
    ##finding feature image url
    url_mars_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_mars_img)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    browser.click_link_by_partial_href('spaceimages/images')
    feature_image_url = browser.url
    time.sleep(5)
    
    ##getting the twitter weather
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    # Retrieve page with the requests module
    response_twitter = requests.get(url_twitter)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup3 = BeautifulSoup(response_twitter.text, 'html.parser')
    mars_weather = soup3.find_all("p",class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text
    
    ##scraping Mars facts
    url_facts = "https://space-facts.com/mars/"
    tables = pd.read_html(url_facts)
    df = tables[0]
    df.columns = ["Parameter", "Values"]
    mars_data_df = df.set_index(["Parameter"])
    mars_data_df.to_html("mars_facts.html")
    mars_data_html = mars_data_df.to_html()
    mars_data_html = mars_data_html.replace("\n", "")
    
    
    ##hemisphere
    url_hemis = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemis)
    time.sleep(5)
    html4 = browser.html
    soup4 = BeautifulSoup(html4, 'html.parser')
    
    links = []

    for link in soup4.find_all('a'):
        finds = link.get("href")
        if ("/search/map/Mars" in finds):
            links.append(finds)
            
    links = list(set(links))
    
    hemisphere_image_urls = []
    
    for i in range(len(links)):
        dicts1 = {}
        dicts1["title"] = soup4.find_all("h3")[i].text
        browser.click_link_by_partial_text(soup4.find_all("h3")[i].text)
        time.sleep(5)
        n_html = browser.html
        soup5 = BeautifulSoup(n_html, "html.parser")
        for link in soup5.find_all("a"):
            finds = link.get("href")
            if ("/full.jpg" in finds):
                dicts1["img_url"] = finds
                
        hemisphere_image_urls.append(dicts1)
        browser.back()
    
    
    print(hemisphere_image_urls)
        
    
    mars_data_dict = {"weather":mars_weather,"mars_facts":mars_data_html,"hemisphere":hemisphere_image_urls,"feature_image": feature_image_url,"title_feature":title_first,"summary_feature":summaries_first}
    
    return mars_data_dict
    
    

    
    
    
    

