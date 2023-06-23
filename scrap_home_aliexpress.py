# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import json

def get_html_content(url, pathChromedriver, scndToSleep=0) :
    driver = webdriver.Chrome(pathChromedriver)
    driver.get(url)
    sleep(scndToSleep)


    html_code = driver.page_source
    driver.quit
    return html_code

url = "https://best.aliexpress.com/"
path = "C:\\Users\\asus\\chromedriver.exe"
code = get_html_content(url, path, scndToSleep=3)

soup = BeautifulSoup(code, 'html.parser')
filecontent = soup.prettify()

with open("htmlcode.txt", "w", encoding="cp1252", errors="ignore") as f:
    f.write(filecontent)




def normalize_string(s):
    """
    Supprime les sauts de ligne et les espaces vides au début et à la fin d'une chaîne de caractères.
    """
    return s.strip().replace('\n', '').replace('\r', '')


def get_file_content(url) :
    filecontent = open(url, "r")
    return filecontent.read()


html_doc = get_file_content("htmlcode.txt")

soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.title.string)

product_code = soup.find('ul', { "class" : "_1TAEi"})
product_list = product_code.find_all('li', {"class": "_2usEB similarList"})
# print(len(product_list))

def extract_info(html_content) :
    id = 0
    lst = []
    for node in html_content :
        img = node.find("img", {"class": "smart-coverImage-standard"}).get("src")
        title = node.find("div", {"class": "smart-title-standard"}).find_next("span")
        price = node.find("div", {"class": "smart-price-doubleLinesWithPrice"}).find_next('span')
        my_dict = {
            "id" : id,
            "img" : img,
            "title": normalize_string(title.string),
            "price": normalize_string(price.string)
        }
        lst.append(my_dict)
        id += 1

    return lst

# print(extract_info(product_list)[0])
js = json.dumps(extract_info(product_list))
with open("prd.json", "w") as f :
    f.write(js)