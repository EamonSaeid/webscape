import requests
import regex as re
from bs4 import BeautifulSoup
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

headers = {
    'user agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.34 Safari/537.36'    
}

def fibcounter(x):
    fib=[0,1]
    fib.extend(sum(fib[-2:]) for _ in range(x-1))
    output=[([int(i) for i in str(fib[-1])].count(j),j) for j in
    range(10) if [int(i) for i in str(fib[-1])].count(j)!=0]
    return sorted(sorted(output, key=lambda x: x[1], reverse=True),
    key=lambda x: x[0], reverse=True)

def extract(url):
    r=requests.get(url)
    return BeautifulSoup(r.content,'html.parser')

def spliceindex(url):
    url=url.split('&')
    url.insert(2,'index=0')
    url="&".join(url)
    return url

def getPropertyLinks(soup):
    return [f'https://www.rightmove.co.uk{i.get("href")}' for i in soup.find_all('a', {'class': 'propertyCard-img-link', 'data-test': 'property-img'})]

def getPropertyPrices(soup):
    return [int(re.sub('\D','',i.text)) for i in soup.find_all('div',{'class':'propertyCard-priceValue'})
            if (re.sub('\D','',i.text)).isnumeric()]
    
def scrape(url):
    url=spliceindex(url)
    soup=extract(url)
    resultsCount=int(soup.find('span',{'class':'searchHeader-resultCount'}).text.replace(',',''))
    pricedata=[]
    if resultsCount!=0:
        pricedata=getPropertyPrices(soup)
    else:
        pricedata='No data'
    
    
    if resultsCount>25:
        for i in range(24,((resultsCount//25))*24,24):
            print(f'index={i-24}',f'index={i}')
            url=url.replace(f'index={i-24}',f'index={i}')
            pricedata+=getPropertyPrices(extract(url))
            if i>=984:
                break
    meanprice=sum(pricedata)/len(pricedata)
    meanprice=round(meanprice,-3)
    return pricedata,meanprice

def generateHist(pricedata):
    n,bins,patches=plt.hist(pricedata,bins=10)
    plt.xlabel='Price'
    plt.ylabel='Frequency'
    plt.title='Distribution of house prices'

    buffer=io.BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    buffer.close()
    response=HttpResponse(image_png, content_type='image/png')
    print(response.url)
    
    return response