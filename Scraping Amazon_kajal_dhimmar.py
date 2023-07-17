


# Scraping data from Amazon

# This is just a code for scraping from amazon




# Import Libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


# Function to extract Product Title

def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})

        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


# Function to extract Product Price

def get_price(soup):
    try:
        # Search for the regular price
        price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

    except AttributeError:

        # If the regular price is not found, set the price to an empty string
        price = ""

    return price


# Function to extract Product Rating


def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating

# Function to extract Number of User Reviews

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count

# Function to extract Availability Status

def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"

    return available

# Function to extract Primary color

def get_product_color(soup):
    try:
        color_div = soup.find("div", attrs={'id': 'inline-twister-dim-title-color_name'})
        color_name = color_div.find("span", class_='a-size-base a-color-secondary').find_next_sibling("span").text.strip()
    except AttributeError:
        color_name = "Color Not Found"
    return color_name



''' 

This function didn't work as I planned, so I just commented out for now.


# Function to extract brand name

def get_brand(soup):
    try:
        brand_div = soup.find("div", attrs={'data-cel-widget': 'bylineInfo_feature_div'})
        brand_name = brand_div.find("a").text.strip()
    except AttributeError:
        brand_name = "Brand Not Found"
    return brand_name

#Function to extract color name



def get_date_first_available(soup):
    try:
        date_span = soup.find("span", text="Date First Available")
        date = date_span.find_next_sibling("span").text.strip()
    except AttributeError:
        date = "Date Not Found"
    return date

'''

if __name__ == '__main__':

    # add your user agent
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://www.amazon.com/s?k=summer+fashion+for+women&crid=3GVQBIO11TW7A&sprefix=summer+fashion+%2Caps%2C182&ref=nb_sb_ss_ts-doa-p_2_15"

    # Store the links
    links_list = []
    
    for page in range(0, 20):                 # you can change this page number
        # HTTP Request
        webpage = requests.get(URL + f"&page={page}", headers=HEADERS)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

        # Loop for extracting links from Tag Objects
        for link in links:
            links_list.append(link.get('href'))
    

    print(links_list)

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[], "color":[]}

    # Loop for extracting product details from each link
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))
        d['color'].append(get_product_color(new_soup))
        
        

    
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("summer_fashion.csv", header=True, index=False) # store a csv name as you like
amazon_df
