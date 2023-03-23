
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import requests 
import time

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://redplanetscience.com'
browser.visit(url)

#create the beautiful soup object to parse the webpage

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

print(soup)

# look for the first article of the webpage 

article = soup.find('div', class_='list_text')

print(article)

#find the title of the article

title_article = article.find('div', class_= 'content_title').text

print (title_article)

#find the article text

paragraph = article.find('div', class_ = 'article_teaser_body').text

print(paragraph)

# url for the mars facts page

url_mars_facts = 'https://galaxyfacts-mars.com'

# reading the html 

mars_facts = pd.read_html(url_mars_facts)
mars_facts

# getting the first item from the list mars_facts

mars_facts_df = pd.DataFrame(mars_facts[0])

mars_facts_df

# assigning the first row of the df as column labels for the DataFrame.

mars_facts_df.columns = mars_facts_df.loc[0]

mars_facts_df.columns 

# setting the index 

mars_facts_df.set_index('Mars - Earth Comparison', inplace=True)

mars_facts_df

# drop the not needed column

mars_facts_df.drop('Mars - Earth Comparison', inplace=True)
mars_facts_df

# save the mars_facts_df to html

mars_facts_df.to_html('mars_facts_table.html')

#navigate to the main page

url_images = 'https://spaceimages-mars.com/'

browser.visit(url_images)

# find the all images button then click on

browser.find_by_text(' FULL IMAGE').first.click()

img = browser.find_by_css('img.fancybox-image')

print(img)

#find the url image 

featured_image_url = img['src']

featured_image_url

#Mars Hemispheres

#main page navigation

hemisphere_page = 'https://marshemispheres.com'

browser.visit(hemisphere_page)

#option1

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

items = soup.find_all('div', class_ = 'item')

#create a beautifulSoup object to access to hemisphere webpage
hemisphere_title_url = []
# loop throup each item
for item in items:
# get the title for the webpage
    title = item.find('h3').text
# find the url for the small resolution image
    image = item.find('img', class_='thumb')['src']
#     append the dict to the list
    
    hemisphere_title_url.append({'Title':title, 'Image_url':image})

print(hemisphere_title_url)

# option 2 full resolution when clich on the  image

# find all items in hemisphere webpage

items = soup.find_all('div', class_= item)

browser.visit('https://marshemispheres.com')

# Create a list to hold the images and titles.
hemisphere_image_urls = []

# Get a list of all of the hemispheres
links = browser.find_by_css('a.product-item img')


for i in range(len(links)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css('a.product-item img')[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()
# close the browser
browser.quit()

hemisphere_image_urls

# create a dictionnairy call marcs_info

mars_info_dict = {
    
    "title": title_article,
    "paragraph":paragraph,
    "featured_image":featured_image_url,
    "mars_facts":mars_facts_df,
    "hemisphere_image":hemisphere_image_urls
}


print(mars_info_dict)
