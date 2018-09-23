from selenium import webdriver
import os
from bs4 import BeautifulSoup
browser = webdriver.Chrome(os.getcwd() + "/chromedriver.exe")
url = "https://ucsd.verbacompare.com/comparison?id=68066"
browser.get(url)
innerHTML = browser.execute_script("return document.body.innerHTML")
#htmlElem = html.document_fromstring(innerHTML)
page_soup = BeautifulSoup(innerHTML, "html.parser")

#divElems = htmlElem.cssselect("[class=item_details]")
items = page_soup.findAll("div",{"class":"item_details"})
name = items[0].find("td",{"class":"title"})
print(name.text.strip())
price = items[0].findAll("div",{"class":"price"})
for indivPrice in price:
    print (indivPrice.text.strip())
