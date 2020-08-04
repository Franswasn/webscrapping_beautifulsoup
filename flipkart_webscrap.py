import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
from xlsxwriter import Workbook
import xlsxwriter

# pages = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
#          '21']


pages = ['1']


def get_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    global onlystar, onlytitle, newprice, onlyprice
    try:
        titles = soup.find_all('div', class_='_3wU53n')
        titles_list = []
        price_list = []
        star_list = []
        link_list = []
        flip_dict = {'title': [], 'price': [], 'rating': [], 'link': []}

        for title in titles:
            newtitle = str(title)
            title_end = newtitle.find('</div')
            title_start = newtitle.find('>')
            onlytitle = newtitle[title_start + 1:title_end]
            titles_list.append(onlytitle)
            flip_dict['title'].append(onlytitle)

        prices = soup.find_all('div', class_='_1vC4OE _2rQ-NK')
        for price in prices:
            newprice = str(price)
            price_end = newprice.find('</di')
            onlyprice = newprice[29 + 1:price_end]
            price_list.append(onlyprice)
            flip_dict['price'].append(onlyprice)
        stars = soup.find_all('div', class_='hGSR34')
        for star in stars[:24]:
            newstar = str(star)
            star_end = newstar.find('<img')
            star_start = newstar.find('>')
            onlystar = newstar[star_start + 1:star_end].replace('.', ',')
            star_list.append(onlystar)
            flip_dict['rating'].append(onlystar)
        links = soup.find_all('a', class_='_31qSD5')
        for link in links:
            newlink = str(link)
            link_start = newlink.find('/')
            link_end = newlink.find('" rel')
            linkonly = ('https://www.flipkart.com{}'.format(newlink[link_start:link_end]))
            link_list.append(linkonly)
            flip_dict['link'].append(linkonly)
        print(price_list)
        df1 = pd.DataFrame(flip_dict)
        df1.to_csv('data4.csv', mode='a', header=False, index=False)

    except:
        titles = ''


def main():
    driver = webdriver.Chrome()
    for page in pages:
        url = 'https://www.flipkart.com/search?q=tablet&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={}'.format(
            page)
        driver.get(url)
        get_detail_data(get_page(url))


if __name__ == '__main__':
    main()