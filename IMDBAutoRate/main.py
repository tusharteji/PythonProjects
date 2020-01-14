import random
from selenium import webdriver
import time

url = "https://www.imdb.com/registration/signin?u=/"
movie_name = "#Movie-name-goes-here"
count = 0

with open('names.txt', 'r') as f:
    for name in f:
        name = name.strip()
        print("Processing " + str(count+1) + ': ' + name)
        driver = webdriver.Chrome(r'chromedriver.exe')
        driver.get(url)
        driver.find_element_by_link_text('Create a New Account').click()
        time.sleep(2)
        driver.find_element_by_id('ap_customer_name').send_keys(name)
        time.sleep(1)
        driver.find_element_by_id('ap_email').send_keys(name + '_' + str(random.randrange(10000, 99999)) + '@gmail.com')
        time.sleep(1)
        driver.find_element_by_id('ap_password').send_keys('test' + name + '123!')
        time.sleep(1)
        driver.find_element_by_id('ap_password_check').send_keys('test' + name + '123!')
        time.sleep(1)
        driver.find_element_by_class_name('a-button-input').click()
        time.sleep(1)
        driver.find_element_by_id('suggestion-search').send_keys(movie_name)
        time.sleep(1)
        driver.find_element_by_id('suggestion-search-button').click()
        time.sleep(2)
        driver.find_element_by_link_text(movie_name).click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="star-rating-widget"]/div/button/span[1]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="star-rating-widget"]/div/div/span[1]/span/a[10]').click()
        time.sleep(1)
        driver.close()
        count += 1
driver.quit()
print("Count: " + count)
print("Last name processed: " + name)
