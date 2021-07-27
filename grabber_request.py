from bs4 import BeautifulSoup
import urllib.request as ur
import requests
import re
import time 
import random

REVIEW_NUMBER_CLASS = 'css-1h1j0y3'
REVIEW_USERNAME_CLASS = 'css-166la90'
REVIEW_RATING_CLASS = 'i-stars__373c0___sZu0'
REVIEW_DATETIME_CLASS = 'css-e81eai'
REVIEW_CONTENT_CLASS = 'raw__373c0__tQAx6'
REVIEW_BLOCK_CLASS = 'review__373c0__3MsBX'

# get all the review pages url from the main page url
def get_reivew_pages (main_page_url, interval, proxy):
  # make a GET request to the target URL to get the raw HTML data

  proxies_used = None
  if proxy != '':
      proxies_used = {'http': "http://" + proxy, 'https': "https://" + proxy}

  res = ur.urlopen(main_page_url)
  finalurl = res.geturl()
  time.sleep (random.randint(interval-5, interval+5)) # random sleep to avoid getting banned by Yelp 
  response = requests.get(finalurl, proxies=proxies_used, timeout=5).text
  # use BeautifulSoup to parse HTML
  soup = BeautifulSoup(response,'html.parser')
  number_reviews = soup.find (class_=REVIEW_NUMBER_CLASS).text
  # use rex to extract the numbers from a string 
  number_reviews = int(re.findall('\d+', number_reviews)[0])
  #print (str(number_reviews) + ' found for this business: ' + business_id)
  # create a list for all reviews url of this business
  url_list = []
  for i in range (0, number_reviews, 10):
    url_list.append(main_page_url + '?start='+str(i))
  return number_reviews, url_list 

def scrap_pg_reivews(business_id, request_url, proxy):
# retrieve all html texts of each review block, inspect showing a unique li class
# output 10 reviews with all html components

  proxies_used = None
  if proxy != '':
      proxies_used = {'http': "http://" + proxy, 'https': "https://" + proxy}

  response = requests.get(request_url, proxies=proxies_used, timeout=5).text
  soup = BeautifulSoup(response,'html.parser')
  # inspect one review, li class, first div class is unique
  results = soup.findAll (class_=REVIEW_BLOCK_CLASS)
  # n_result = len(results)
  # print(str(n_result) + ' results are found')
  single_page_review = []
  for review in results:
    # retrieve user name
    username = review.find (class_=REVIEW_USERNAME_CLASS).text
    # print('username: ' + username)
    # extract attribute value using the key aria-label for star ratings. 
    rating = review.find (class_=REVIEW_RATING_CLASS)['aria-label']
    # \d+ is a rgular exression pattern to extract numbers from a string
    rating = float (re.findall('\d+', rating)[0])
    # extract date of review; same use inspect to find that it is a span class
    review_date = review.find (class_=REVIEW_DATETIME_CLASS).text
    # retrieve all review content
    review_content = review.find(class_=REVIEW_CONTENT_CLASS, attrs={'lang':'en'}).text
    single_review =[business_id, username, rating, review_date, review_content]
    single_page_review.append (single_review)
  return single_page_review

def get_business_reviews(business_id, url, interval, proxy):
    results = get_reivew_pages(url, interval, proxy)
    num_reviews = results[0]
    review_pages = results[1]
    print ('total ', num_reviews, ' reviews in ', len(review_pages), ' review pages were found')
    all_reviews = []
    for index, url in enumerate(review_pages):
      all_reviews = all_reviews + scrap_pg_reivews (business_id, url, proxy)     
      time.sleep (random.randint(interval-5, interval+5)) # random sleep to avoid getting banned by Yelp 
      print ('finished page ',(index+1), '/', len(review_pages)) # display the progress
    return num_reviews, all_reviews