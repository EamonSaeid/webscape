from django.http import HttpResponse
from django.shortcuts import render
import base64

from .functions import *

def getdata(request):
    return render(request,"marketscape/elements.html",{"inputdata":["price",'type']})

def home(request):
    return render(request,"marketscape/index.html",{"inputdata":["price",'type']})

def fibonnaci(request):
    if request.method=='POST':
        x=int(request.POST.get('x'))
        output=fibcounter(x)
        return render(request,'marketscape/fibanswer.html',{'output':output})
    return render(request, 'marketscape/fibanswer.html')

def scraper(request):
    if request.method=='POST':
        try:
            
            url=request.POST.get('urlinput')
            pricedata,meanprice=scrape(url)
            
            # Generate histogram data
            n, bins, patches = plt.hist(pricedata, bins=20)
            plt.xlabel('Price')
            plt.ylabel('Frequency')
            plt.title('Distribution of House Prices')
            plt.ticklabel_format(style='plain')
            
            # Save plot image to buffer and create HTTP response
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            plt.cla()
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            image_uri = base64.b64encode(image_png).decode('utf-8')
            
            
            return render(request,'marketscape/scraper.html',{'prices':pricedata,'mean':meanprice,'hist':image_uri})
        except:
            return render(request,'marketscape/scraper.html',{'error':'Ensure you are using a valid rightmove search url!'})
    return render(request,'marketscape/scraper.html')
