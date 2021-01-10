from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    #Open broswer
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #Navigating to NASA Mars News.
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')
    
    #Scrapping the title and passage
    news_title = nasa_soup.find("li", class_="slide").find("div", class_="content_title").a.text
    news_p = nasa_soup.find("li", class_="slide").find("div", class_="article_teaser_body").text
    
    #Navigate to JPL Image website.
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    
    #Scrapping the image url link.
    browser.find_by_css('.articles').find_by_css('.fancybox').first.click()
    featured_image_url = browser.find_by_css('.fancybox-image')['src']
    
    #Use pandas to scrape table.
    mf_url = 'https://space-facts.com/mars'
    tables = pd.read_html(mf_url)
    raw_table = tables[0]
    
    #Modify table.
    raw_table.replace(':','', regex=True, inplace=True)
    raw_table.rename(columns={0: "Characteristics", 1: "Values"}, inplace=True)
    raw_table.set_index('Characteristics', inplace=True)
    
    #Convert table to html format.
    html_table = raw_table.to_html(classes='table table-striped table-bordered', justify='center')
    
    #Scrape Mars Hemisphere Photos.
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    
    hemisphere_image_urls = []
    for x in range(4):
        browser.find_by_css('.item')[x].find_by_css('.thumb').click()
        hemi_url = browser.links.find_by_partial_text('Sample')['href']
        title = browser.title
        hemi_title = ' '.join(title.split()[0:title.split().index('Hemisphere')+1])
        hemi_dict = {"title": hemi_title, "img_url": hemi_url}
        hemisphere_image_urls.append(hemi_dict)
        browser.back()
        x += 1
    
    #Storing everything into a big chunk dictionary.
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    
    browser.quit()
    
    return mars_data

