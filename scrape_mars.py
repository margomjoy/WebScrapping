# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 09:36:43 2020

@author: Joisel
"""


#Imports & Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

#Site Navigation

executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)


# NASA Mars News Site Web Scraper
def mars_news(browser):
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    
    #browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    
    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")
        news_soup.find("h1", class_="article_title")
        
        news_title = slide_element.find("div", class_="content_title").get_text()

        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    
    print(news_title)
    print(news_paragraph)
    return news_title, news_paragraph



# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper
def featured_image(browser):
    
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None 
   
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    
    print('NASA JPL (Jet Propulsion Laboratory) Site Web Scraper DONE!')
    return img_url



# Mars Facts Web Scraper
def mars_facts():
    
    try:
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-striped")

def twitter2():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    html_weather=browser.html
    soup = BeautifulSoup(html_weather, 'html.parser')
    articles = soup.find_all('article', class_='css-1dbjc4n r-1loqt21 r-16y2uox r-1wbh5a2 r-1ny4l3l r-1udh08x r-1j3t67a r-o7ynqc r-6416eg')
    #getting weather tags
    weather = articles[0].find_all('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    #weather text
    for w in weather:  
        weather_text = w.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
    print(weather_text)
    return weather_text



# Mars Hemispheres Web Scraper
def hemisphere(browser):
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        
        browser.find_by_css("a.product-item h3")[item].click()
        
        
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        
        hemisphere_image_urls.append(hemisphere)
        
        
        browser.back()
    return hemisphere_image_urls

# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere



def scrape_all():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": twitter2(),
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())