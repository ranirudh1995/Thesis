from bs4 import BeautifulSoup
import requests
import time
from time import sleep
url = 'https://en.wikipedia.org/wiki/Portal:Contents/Categories'
wikiurl = 'https://en.wikipedia.org'

allcategoryurls = []
''' get soup '''
def get_soup(url):
    # get contents from url

    try:
        content = requests.get(url).content
        return BeautifulSoup(content, 'lxml')  # choose lxml parser
    except:
        print("Connection refused by the server..")
        print("Let me sleep for 5 seconds")
        print("ZZzzzz...")
        time.sleep(5)
        print("Was a nice sleep, now let me continue...")
        content = requests.get(url).content
        return BeautifulSoup(content, 'lxml')  # choose lxml parser
    # get soup


def extract_articles(url,text):
    soup = get_soup(url)
    subcategorytag = soup.find('div',{'id':'mw-subcategories'})
    contentpagetag = soup.find('div', {'id': 'mw-pages'})
    sublinks = []
    contentpages = []
    #check whether current page has a subcategory
    if subcategorytag!=None:
        subtag = subcategorytag.find('div',{'class':'mw-content-ltr'})
        sublinks.append(subtag.findAll('a',href=True))
        for link in sublinks:
            for atag in link:
                print(text) #debugging purposes
                if atag['href'] not in allcategoryurls:
                    allcategoryurls.append(atag['href'])
                    extract_articles(wikiurl + atag['href'], text+'__'+atag.text+'__,')

    #check whether current page has a link to content page
    if contentpagetag!=None:
        contenttag = contentpagetag.find('div',{'class':'mw-content-ltr'})
        contentpages.append(contenttag.findAll('a',href=True))
        for link in contentpages:
            for atag in link:
                print(text) #debugging purposes
                extract_articles(wikiurl + atag['href'], text + '__'+atag.text+'__')

    #if current page does not have subcategory and links to content page
    # then it is the content page which is needed to be extracted
    if subcategorytag==None and contentpagetag==None:
        ptags = soup.findAll('p')
        content = text+': '
        for ptag in ptags:
            content = content + ptag.getText()
        content = content
        print(content) #debugging purposes
        file = open("textdata.txt","a",encoding="utf-8")
        file.write(content+"\n")
        file.close()


if __name__ == '__main__':

    # get soup
    soup = get_soup(url)  # choose lxml parser
    # find the tag : <div class="toc">
    tags = soup.findAll('div', {'class': 'hlist'})  # id="toc" also works
    # get all the links

    taglist = []

    #data on Applied Sciences and Technology
    taglist.append(tags.pop(-8))
    taglist.append(tags.pop(-7))

    links = []
    for tag in taglist:
        links.append(tag.findAll('a',href=True))  # <a href='/path/to/div'>topic</a>

    for link in links:
        for atag in link:
            extract_articles(wikiurl+atag['href'],'__'+atag.text+'__,')

    file = open("textdata.txt","w",encoding="utf-8")
    file.close()