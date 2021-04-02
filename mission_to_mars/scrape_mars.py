import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests


def scrape():
    ### NASA Mars News
    # setup splinter and bs4
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=True)

    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # scrape the Mars News Site and collect the latest News Title and Paragraph Text. 
    # assign the text to variables that you can reference later.
    news_title = soup.find('div', id='news').find('div', class_='content_title').text
    news_p = soup.find('div', id='news').find('div', class_='article_teaser_body').text

    ### JPL Mars Space Images - Featured Image
    # visit the url for the Featured Space Image site.
    # use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # make sure to find the image url to the full size .jpg image.
    # make sure to save a complete url string for this image.
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = url + soup.find('img', class_='headerimage fade-in')['src']

    ### Mars Facts
    # visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet
    # including Diameter, Mass, etc.
    # use Pandas to convert the data to a HTML table string.
    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = df.iloc[0]
    df = df[1:]
    df.columns = ['', 'Mars', 'Earth']
    table_string = df.to_html(index=False, classes='table table-striped table-hover')

    ### Mars Hemispheres
    # visit the astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    # you will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    url = "https://marshemispheres.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hemisphere_image_urls = []

    for i in range(4):
        items = soup.find_all('div', class_='description')
        title = items[i].h3.text
        link = title.split()[0].lower() + '.html'
        new_url = url + link
        response = requests.get(new_url)
        soup_new = BeautifulSoup(response.text, 'html.parser')
        img_url = url + soup_new.find('div', class_='downloads').a['href']
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})

    # Quit the browser
    browser.quit()

    # Store data in a dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "table_string": table_string,
        "hemisphere_1": hemisphere_image_urls[0],
        "hemisphere_2": hemisphere_image_urls[1],
        "hemisphere_3": hemisphere_image_urls[2],
        "hemisphere_4": hemisphere_image_urls[3],
    }

    return mars_dict
