import csv
import os
import sys

import requests

import constants
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request

from api import curl


def load_fetch_post(driver):
    image_list = []  # to store the posts

    # get the no of posts
    try:
        no_of_posts = str(driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text).replace(',', '')
        no_of_posts = int(no_of_posts)
        print('{0} has {1} posts'.format("komal", no_of_posts))
    except Exception:
        print('Some exception occurred while trying to find the number of posts.')
        sys.exit()

    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        all_images = soup.find_all('img', attrs={'class': 'FFVAD'})
        print(len(all_images))
        for img in all_images:
            if img not in image_list:
                print(img)
                image_list.append(img)
        image_list_src=[]
        # print('---'+image_list+'----')
        for img in image_list:
            try:
                image_list_src.append(str(img).split('src')[1].split('style')[0].replace('amp;','').lstrip("'").lstrip('=').lstrip('"').rstrip(' ').rstrip('"'))
            except Exception:
                print('error in getting images')
        print('###################')
        print(image_list_src)
        print('##################')
        for i in range(len(image_list_src)):
            try:
                urllib.request.urlretrieve(image_list_src[i], "/Users/300073043/Desktop/hack/images/"+str(i)+".jpg")
                print('downloaded '+str(i))
            except Exception:
                print('Exception occured for '+str(i))
        print(image_list_src)
    except Exception:
        print('Some error occurred while scrolling down and trying to load all posts.')
        sys.exit()

    return image_list

def get_image_data(fileName):
    curl(fileName)

def userLogin():
    getdriver = constants.INSTAGRAM_LOGIN
    driver = webdriver.Chrome(constants.chromeDriver)
    driver.get(getdriver)
    sleep(3)
    driver.find_element_by_name('username').send_keys(constants.username)
    driver.find_element_by_name('password').send_keys(constants.password)
    driver.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button').click()
    sleep(7)
    driver.find_element_by_css_selector('#react-root > section > main > div > div > div > div > button').click()
    sleep(3)
    driver.find_element_by_css_selector(
        'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm').click()
    driver.get(constants.komalPandey)
    sleep(3)
    l= load_fetch_post(driver)
    with open("image_url.csv","w") as f:
        wr = csv.writer(f,delimiter="\n")
        wr.writerow(l)
    files = os.listdir('/Users/300073043/Desktop/hack/images/')
    for file in files:
        get_image_data(str(file))



def get_hashtags_posts():
    userLogin()
    return "data refreshed successfully"

