import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

class Wine():

    def __init__(self):
        self.price = ""
        self.seller = ""
        self.monthlySale = ""
        self.commentNum = ""
        self.header = ""
        self.url = ""

    def __str__(self):
        return ("{}| {} |{} |{} |{} |{}".format(self.price,self.seller, self.monthlySale, self.commentNum,self.header,self.url))

def crawl (url):
    response = requests.get(url)
    return(response.content)

def parse(content):
    wines = []
    soup = BeautifulSoup(content,'html.parser')
    matches=soup.find_all('div',class_="product-iWrap")
    for match in matches:
        wine = Wine()
        wine.price = match.find("p",class_="productPrice").em["title"]
        wine.header = match.find('p',class_="productTitle").a["title"]
        wine.url = match.find('p',class_="productTitle").a["href"]
        wine.seller = match.find('div',class_="productShop").a.text.strip()
        _sale_and_comment = match.find('p',class_="productStatus").text
        if len(re.findall(r"[0-9]+.*[0-9]*",_sale_and_comment)) == 2:
            wine.monthlySale = re.findall(r"[0-9]+.*[0-9]*",_sale_and_comment)[0]
            wine.commentNum = re.findall(r"[0-9]+.*[0-9]*",_sale_and_comment)[1]
        else:
            print ("{} error, please check".format(_sale_and_comment))
        wines.append(wine)
        print(wine)

def parse_page(content):

    soup = BeautifulSoup(content, 'html.parser')
    _url_suffix = soup.find("a",class_="ui-page-next")["href"]
    next_page = r"https://list.tmall.com/search_product.htm{url_suffix}".format(url_suffix=_url_suffix)
    return next_page


url = r"https://list.tmall.com/search_product.htm?q=%BA%EC%BE%C6&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&xl=hongjiu_1&from=mallfp..pc_1_suggest"

for i in range(1,50):

    content = crawl(url)
    parse(content)
    url = parse_page(content)
