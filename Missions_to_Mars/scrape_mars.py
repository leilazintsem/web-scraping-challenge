#Import dependencies and setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd


def scrape():
    #Chrome driver set up

    executable_path = {"executable_path":"driver\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    #Connecting to NASA site
    url = "https://redplanetscience.com"
    browser.visit(url)

    # Parse Results HTML with BeautifulSoup

    html = browser.html
    news = BeautifulSoup(html, "html.parser")

    # let's get the news title and paragraph 
    news_title = news.select_one('.col-md-8 .content_title').get_text()
    news_p = news.select_one('.col-md-8 .article_teaser_body').get_text()


    # get the feature image
    url = "https://spaceimages-mars.com"
    browser.visit(url)

    html = browser.html
    images = BeautifulSoup(html, "html.parser")

    featured_image = url+"/"+ images.select_one('.headerimage')["src"]



    #Use Pandas to convert the data to a HTML table string
    url = "https://galaxyfacts-mars.com"
    df_list = pd.read_html(url)
    table_string = df_list[0].to_html().strip()
        
        #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    data = []

    url = "https://marshemispheres.com"
    browser.visit(url)
    html = browser.html
    bs = BeautifulSoup(html, "html.parser")
    links = bs.select('.description>a')
    for link in links:
        title = link.get_text()
        href=link["href"]
        browser.visit(url+"/"+ href)
        html1 = browser.html
        details_page = BeautifulSoup(html1, "html.parser")
        full_image = details_page.select_one('img.wide-image')
        data.append({
            "title": title, 
            "img_url": url + "/" + full_image["src"]
    
        })
    return {
        "latest_news": {
            "news_title": news_title, 
            "news_p": news_p
        },
        "featured_image": featured_image,
        "facts":  table_string,
        "hemispheres": data
    }
