#! /usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def get_soup(link):
    wbdata = requests.get(link).text
    soup = BeautifulSoup(wbdata, 'lxml')
    return soup

def AVdataFinder(av_id, mosaic_flag):
    if mosaic_flag == 0:
        url = "https://javpee.com/cn/search/%s" % av_id
    if mosaic_flag == 1:
        url = "https://javhip.com/cn/search/%s" % av_id
    soup = get_soup(url)
    items = soup.select("div.item")
    if items.__len__() > 1:
        for i,item in enumerate(items):
            print('%d. %s' % (i, item.get_text().strip()))
        while True:
            which_one = int(input("选择哪一个："))
            if which_one >= items.__len__():
                print("输入无效！")
            else:
                break
        for href in items[which_one].find_all('a'):
            link = href.attrs['href']
    else:
        for href in items[0].find_all('a'):
            link = href.attrs['href']
    return link

def AVdataDownloader(link, mosaic_flag):
    soup = get_soup(link)
    if mosaic_flag == 0:
        for screencap in soup.select("div.col-md-9")[0].find_all('img'):
            IMG_URL = screencap.get('src')
            title = screencap.get('title')
    if mosaic_flag == 1:
        for screencap in soup.select("div.col-md-9")[0].find_all('a'):
            for IMG_URLs in screencap.find_all('img'):
                IMG_URL = IMG_URLs.get('src')
            title = screencap.get('title')

    Actors = []
    for avatar in soup.select("#avatar-waterfall")[0].find_all('a'):
        Actors.append(avatar.text.strip())

    p_count = 0
    if mosaic_flag == 0:
        for info in soup.select("div.col-md-3")[0].find_all('p'):
            p_count += 1
            if p_count == 1:
                ID = info.get_text()[5:]
            if p_count == 2:
                Release_Date = info.get_text()[6:]
            if p_count == 3:
                Length_time = info.get_text()[3:]
                Length_time = Length_time[:-2].strip()
            if p_count == 5:
                Studio = info.get_text()
            if p_count == 6:
                if info.get_text() == "系列:":
                    Series_flag = 1
                else:
                    Series_flag = 0
            if p_count == 7:
                if Series_flag == 1:
                    Series = info.get_text()
                else:
                    Series = "None"
                    Genres = []
                    for key_word in info.find_all('a'):
                        Genres.append(key_word.get_text())
            if p_count == 9 and Series_flag == 1:
                Genres = []
                for key_word in info.find_all('a'):
                    Genres.append(key_word.get_text())
    if mosaic_flag == 1:
        for info in soup.select("div.col-md-3")[0].find_all('p'):
            p_count += 1
            if p_count == 1:
                ID = info.get_text()[5:]
            if p_count == 2:
                Release_Date = info.get_text()[6:]
            if p_count == 3:
                Length_time = info.get_text()[3:]
                Length_time = Length_time[:-2].strip()
            if p_count == 8:
                Studio = info.get_text()
            if p_count == 9:
                if info.get_text() == "系列:":
                    Series_flag = 1
                else:
                    Series_flag = 0
            if p_count == 10:
                if Series_flag == 1:
                    Series = info.get_text()
                else:
                    Series = "None"
                    Genres = []
                    for key_word in info.find_all('a'):
                        Genres.append(key_word.get_text())
            if p_count == 12 and Series_flag == 1:
                Genres = []
                for key_word in info.find_all('a'):
                    Genres.append(key_word.get_text())

    Title = title[ID.__len__():].strip()

    return IMG_URL, ID, Title, Actors, Release_Date, Length_time, Studio, Series, Genres

def IMGDownloader(IMG_URL, filename):
    with open('%s.jpg' % filename, 'wb') as file:
        file.write(requests.get(IMG_URL).content)

def filenameGenerator(ID, Title, Actors, Studio):
    if Actors.__len__() == 1:
        filename = "%s - [%s]%s - [%s]" % (Actors[0], Studio, Title, ID)
    else:
        filename = "%s 等. - [%s]%s - [%s]" % (Actors[0], Studio, Title, ID)

    return filename.replace( ":" , " ")

if __name__ == '__main__':
    av_id = input("输入番号：")

    while True:
        mosaic_flag = int(input("0. 步兵\n1. 骑兵\n输入0或1："))
        if mosaic_flag != 0 and mosaic_flag != 1:
            print("输入无效！")
        else:
            break
    link = AVdataFinder(av_id, mosaic_flag)
    IMG_URL, ID, Title, Actors, Release_Date, Length_time, Studio, Series, Genres = AVdataDownloader(link, mosaic_flag)
    filename = filenameGenerator(ID, Title, Actors, Studio)
    IMGDownloader(IMG_URL, filename)

    print("====输出====")
    print(filename)
    print("封面：%s\n番号：%s\n标题：%s\n演员：%s\n发行日期：%s\n长度：%s分钟\n发行商：%s\n系列：%s\n类别：%s\n" % (IMG_URL, ID, Title, Actors, Release_Date, Length_time, Studio, Series, Genres))
