from selenium import webdriver
import os
from bs4 import BeautifulSoup
from time import sleep
import sqlite3

#Create DataBase
conn = sqlite3.connect('UCSDprices.db')
c = conn.cursor()
c.execute('''CREATE TABLE if not exists bookstore
         (class text, book text, price real, condition text, retailer text)''')
conn.commit()
previous_class = ""
try:
    for i in range(57960, 57965):
        #Use Selenium and BeautifulSopu to scrape HTML
        browser = webdriver.Chrome(os.getcwd() + "/chromedriver.exe")
        url = "https://ucsd.verbacompare.com/comparison?id=" + str(i)
        browser.get(url)
        sleep(2)
        innerHTML = browser.execute_script("return document.body.innerHTML")
        page_soup = BeautifulSoup(innerHTML, "html.parser")

        #Create tuples and list to insert all data into DB
        sql_list = []
        sql_tuple = ()
        class_name = page_soup.find("div",{"class":"in_section"}).span.text.strip()
        if(previous_class[:10] == class_name[:10]):
            pass
        else:
             previous_class = class_name
        #Pull the different books from the HTML and loop over them and their prices
        items = page_soup.findAll("div",{"class":"item_details"})
        for indivItem in items:
            name = indivItem.find("td",{"class":"title"}).text.strip()
            price = indivItem.findAll("div",{"class":"price"})
            condition = indivItem.findAll("div",{"class":"condition"})
            retailer = indivItem.findAll("div",{"class":"retailer"})
            for count, indivPrice in enumerate(price):
                #place all data values into a tuple which is then appended into my list
                sql_tuple = (class_name, name, float(indivPrice.text.strip().replace("$","")), condition[count].text.strip(), retailer[count].text.strip())
                sql_list.append(sql_tuple)
        #Uplaod everything to the database
        c.executemany('INSERT OR REPLACE INTO bookstore VALUES (?,?,?,?,?)', sql_list)
        conn.commit()
        browser.close()
except Exception as e: print(e)
conn.close()
browser.quit()
