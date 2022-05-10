from threading import local
from django.shortcuts import render
from .models import Dannie
import requests
from bs4 import BeautifulSoup
from django.core.paginator import *

URL = 'https://news.mail.ru/'
API = 'https://api.domainsdb.info/v1/domains/search?domain='

def get_html(url):
    r=requests.get(url)
    return r

def create(request): 
    Dannie.objects.all().delete()
    html=get_html(URL).text 
    itog = []
    result = []
    linsApi = {}
    soup=BeautifulSoup(html,'html.parser')

    #формирование списка ссылок
    for link in soup.find_all('a'):
        if link.get('href')!=None and ('https'in link.get('href') or 'http'in link.get('href')) and link.get('href') not in result:
             result.append(link.get('href'))
             itog.append(API+link.get('href'))
    
    #перебор ссылок и извлечение нужной информации
    print('Перебор ссылок начался!\n')
    i = 0
    for api_get in itog:
        linsApi[result[i]] = get_html(api_get).json()['domains'] 
        i+=1
        if i==20:
            print('Стоит немного подождать...')
        elif i ==50:
            print('Совсем чуть-чуть...')

    i=1
    print('Готово!')
    #формирование строк для БД
    for key,values in linsApi.items():
        allDomain = ""
        allCreate = ""
        allUpdate = ""
        allCountry = ""
        allIsDead = ""
        AllA = ""
        AllNS = ""
        allCname = ""
        AllMx = ""
        AllTXT = ""
        for val in values:
            domain = val['domain']
            allDomain+=str(domain)+'\n'
            create_date = val['create_date']
            allCreate+=str(create_date)+'\n'
            update_date = val['update_date']
            allUpdate+=str(update_date)+'\n'
            country = val['country']
            allCountry+=str(country)+'\n'
            isDead = val['isDead']
            allIsDead+=str(isDead)+'\n'
            A = " ".join(val['A']) if isinstance(val['A'], list) else 'None'
            AllA+=str(A)+'\n'
            NS = " ".join(val['NS']) if isinstance(val['NS'], list) else 'None'
            AllNS+=str(NS)+'\n'
            CNAME = val['CNAME']
            allCname+=str(CNAME)+'\n'
            MX = []
            if isinstance(val['MX'], list):
                for elm in val['MX']:
                    for key2,value2 in elm.items():
                        MX.append(key2)
                        MX.append(str(value2))
            else:
                MX.append(None)
            if len(MX)==0:
                MX2=''
            elif len(MX)!=0 and MX[0]==None:
                MX2='None'
            else:
                MX2 = " ".join(MX)
            AllMx+=str(MX2)+'\n'
            TXT = " ".join(val['TXT']) if isinstance(val['TXT'], list) else 'None'
            AllTXT+=str(TXT)+'\n'
            
        #добавление строки с помощью метода POST
        strok = Dannie()
        strok.id = i
        strok.url = key
        strok.domain = allDomain
        strok.create_date = allCreate
        strok.update_date = allUpdate
        strok.country = allCountry
        strok.isDead = allIsDead
        strok.A = AllA
        strok.NS = AllNS
        strok.CNAME = allCname
        strok.MX = AllMx
        strok.TXT = AllTXT
        strok.save()  
        i+=1

    print('Все данные успешно записаны!')



def home(request):
    obnov =request.POST.get('obnovlenie','')
    print(obnov)
    if obnov:
        create("POST")

    search_query = request.GET.get('search','') 
    search_querybtn = request.GET.get('url','')  
    if search_query:
        allStrok = Dannie.objects.filter(id=search_query)
    else:
        allStrok = Dannie.objects.all()
    if search_querybtn:
        allStrok = Dannie.objects.order_by(search_querybtn)

    #пагинация таблицы 
    page = request.GET.get('page', 1)
    paginator = Paginator(allStrok, 10)

    #получение нужных данных
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request,'parserr/home.html',{'users': users})

