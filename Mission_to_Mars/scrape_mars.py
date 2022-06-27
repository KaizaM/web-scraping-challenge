# Dependencies
#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html 
    soup = bs(html, 'html.parser') 

    results = soup.find('div', class_="list_text")
    title = results.find_all('div', class_='content_title')[0].text
    blurb = results.find_all('div', class_='article_teaser_body')[0].text

    print(f'News_Title = {title}')
    print(f'News_P = {blurb}')

    # JPL Mars Space Images - Featured Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    #name of the featured image
    floating_txt_area = soup.find_all('div', class_='floating_text_area')

    for featured_img in floating_txt_area:
        a = featured_img.find('a')
        image = a['href']
        print(image)
    featured_image_url = 'https://spaceimages-mars.com/' + image
    print (f"Featured_image_url = {featured_image_url}")

    # Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    tables = pd.read_html(url)
    tables

    table = tables[0]
    table.columns = ['Fact', 'Mars', 'Earth']
    table = table.set_index('Fact')
    table

    html_convert = table.to_html()
    html_convert

    html_convert = html_convert.replace('\n', '')
    html_convert

    # Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere = soup.find_all('div', class_='description')
    hemisphere

    url_list = []

    for line in hemisphere:
        title = line.find('h3').text

        partial_href = line.find('a')['href']
        full_href = url + partial_href

        browser.visit(full_href)
        html = browser.html
        soup = bs(html, 'html.parser')
        result = soup.find_all('div', class_="wide-image-wrapper")
        link = result[0].find('img', class_="wide-image")
        href = link['src']
        full_url = url + href

        url_list.append({"title":title, "img_url":full_url})
    url_list

    browser.quit()