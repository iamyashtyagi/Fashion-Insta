import csv
import sys
import constants
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver


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

        print(image_list)
        if no_of_posts > 12:  # 12 posts loads up when we open the profile
            no_of_scrolls = 1  # extra scrolls if any error occurs while scrolling.

            # Loading all the posts
            print('Loading all the posts...')
            for __ in range(no_of_scrolls):

                # Every time the page scrolls down we need to get the source code as it is dynamic
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(2)  # introduce sleep time as per your internet connection as to give the time to posts to load

                soup = BeautifulSoup(driver.page_source, 'lxml')
                all_images = soup.find_all('img')
                type(all_images)
                new_images=[]
                all_images_text=[str(img).split('src')[1].split('style')[0] for img in all_images]

                for img in all_images_text:
                    new_images.append((img.split("src")[1].split("style")[0]))
                print(new_images)


                for img in all_images:
                    if img not in image_list:
                        image_list.append(img)
    except Exception:
        print('Some error occurred while scrolling down and trying to load all posts.')
        sys.exit()

    return image_list


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

    l= load_fetch_post(driver)
    with open("out.csv","w") as f:
        wr = csv.writer(f,delimiter="\n")
        wr.writerow(l)


def get_hashtags_posts(query):
    userLogin()
    return "posts"


if __name__ == "__main__":
    hashtag = "hrithik"
    posts = get_hashtags_posts(hashtag)

    print(posts)