from selenium import webdriver
import os
from bs4 import BeautifulSoup
from time import sleep
import sqlite3
import re

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('''CREATE TABLE if not exists bookstore
         (class text, book text, price real, condition text, retailer text)''')
conn.commit()

browser = webdriver.Chrome(os.getcwd() + "/chromedriver.exe")
url = "https://ucsd.verbacompare.com/comparison?id=68066"
browser.get(url)
sleep(2)
innerHTML = browser.execute_script("return document.body.innerHTML")
page_soup = BeautifulSoup(innerHTML, "html.parser")

sql_list = []
sql_tuple = ()
class_name = page_soup.find("div",{"class":"in_section"}).span.text.strip()

items = page_soup.findAll("div",{"class":"item_details"})
for indivItem in items:
    name = indivItem.find("td",{"class":"title"}).text.strip()
    price = indivItem.findAll("div",{"class":"price"})
    condition = indivItem.findAll("div",{"class":"condition"})
    retailer = indivItem.findAll("div",{"class":"retailer"})
    for count, indivPrice in enumerate(price):
        price_list = []
        for n in indivPrice.text.strip().replace("$",""):
            try:
                price_list.append(float(n))
            except ValueError:
                pass
        sql_tuple = (class_name, name, price_list[0], condition[count].text.strip(), retailer[count].text.strip())
        sql_list.append(sql_tuple)
print(sql_list)
c.executemany('INSERT OR REPLACE INTO bookstore VALUES (?,?,?,?,?)', sql_list)
c.close()
browser.close()
