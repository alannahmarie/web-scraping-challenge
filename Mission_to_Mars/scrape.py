import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    scraped_data = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    news = soup.find("li", class_="slide")

    news_title = news.find("div", class_="content_title").text
    news_paragraph = news.find("div", class_="article_teaser_body").text

    scraped_data["news_title"] = news_title
    scraped_data["news_paragraph"] = news_paragraph

    browser.quit()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    img_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(img_url)

    html = browser.html
    soup = bs(html, 'html.parser')
    img_src = soup.find(class_='headerimage fade-in')['src']
    crop_img_url = img_url[:-10]

    featured_image_url = (f'{crop_img_url}{img_src}')

    scraped_data["featured_image"] = featured_image_url

    browser.quit()

    facts_url = "https://space-facts.com/mars/"

    tables = pd.read_html(facts_url)

    mars_facts = tables[0]

    facts_html = mars_facts.to_html(header=False)

    scraped_data["mars_facts_table"] = facts_html

    browser.quit()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    crop_hemi_url = hemi_url.split("/search")[0]

    hemisphere_image_urls = []

    for x in range(0,4):
        
        browser.visit(hemi_url)
        
        hemi = browser.find_by_tag("h3")
        hemi[x].click()
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        title = soup.find("h2", class_="title").text
        title = title[:-9]
        hem_img_url = soup.find("img", class_="wide-image")["src"]
        
        hemisphere_image_urls.append({
        "title": title,
        "image_url": (f"{crop_hemi_url}{hem_img_url}")
        })

    scraped_data["mars_hemisperes"] = hemisphere_image_urls

    browser.quit()
    print(scraped_data)
    return scraped_data


