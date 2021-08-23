# This file is created by me

from django.http import HttpResponse
from django.shortcuts import render
from itertools import combinations#use itertools to generate diffrent combinations of elements
from youtube_search import YoutubeSearch#Use to fetch youtube top search results

base="Cooking recipes only with"#Will be used to concat with inpur recipe
def search(query):
  re=['id', 'thumbnails', 'title','channel', 'duration', 'views','long_desc']#unwanted detials fetched by api so we will be using other results except elements in the re
  results = YoutubeSearch(query, max_results=1).to_dict()#use to fetch results of youtube and max_results as 1 so we will be getting top results
  for i in results:
    l=[i.pop(key) for key in re]#except elements in 're'  
    i['url_suffix']="https://www.youtube.com/"+i['url_suffix']#api will give the url with "youtube.com" so we will be adding them mannualy
    return i
def index(response):
    return render(response, 'index.html')

def chef(request):
    djtext=request.POST.get('text', 'off')#retrive text from user input in website
    small = request.POST.get('small', 'off')#as we use checkbox so if user selected the option it will retrun 'on' or else 'false'
    med = request.POST.get('med', 'off')
    large = request.POST.get('large', 'off')
    pas="You didn't select any operation "+"\n    or    \n"+"User Should Provide Minimum Ingredients as Provided"+'\n'+"For Small Recipes:- atleast 1\n"+"For Medium Recipes:- atmost 3\n"+"For Large Recipes:- atleast 3\n"+"THANK YOU"
    params = {'name': 'Error is', 'string': pas}
    aa=len(djtext.split(','))
    res1="\n CAUTION For Small Recipes:- Atleast 1 Ingredient\n"
    res2 = "\n CAUTION For Medium Recipes:- Atmost 3 Ingredient\n"
    res3 = "\n CAUTION For Large Recipes:- Atleast 3 Ingredient3\n"
    if(aa>=1 and small == 'on'):
        res1 = ""
        a=djtext.split(",")
        for i in range(len(a)):
            query = base + " " + a[i]
            try:
                s=search(query)    
                url = s['url_suffix']
                ss=url+" "+"(Ingredients Used : "+a[i]+")"
                res1=ss+'\n'+res1
            except:
                continue
        res1='These are the best quick recipes for your ingredients'+'\n'+res1
        params = {'name':'', 'string': str(res1+'\n'+res2+'\n'+res3)}
    if((aa<=3 and aa>=2) and med == 'on'):
        res2=""
        a=djtext.split(",")
        a=list(combinations(a,2))
        for i in a:
            query = base + " " + i[0] + " and "+ i[1]
            try:
                s=search(query)    
                url = s['url_suffix']
                ss=url+" "+"(Ingredients Used : "+i[0]+","+i[1]+")"
                res2=ss+'\n'+res2
            except:
                continue
        res2='These are the best Medium Recipes for your ingredients  : '+'\n'+res2
        params = {'name': '', 'string':  str(res2+'\n'+res1+'\n'+res3)}
    if(aa>=3 and large == 'on'):
        res3=""
        a=djtext.split(",")
        if len(a)>3:
            a= list(combinations(a,4))
            for i in a:
                if len(a) <= 3:
                    query = base + " " + i[0] + " and " + i[1] + " and " + i[2]
                    try:
                        s=search(query)    
                        url = s['url_suffix']

                        ss=url+" "+"(Ingredients Used : "+i[0] + "," + i[1] + " and " + i[2]+")"
                        res3=ss+'\n'+res3
                    except:
                        continue  
                    res3='These are the best Large Recipes for your ingredients  : '+'\n'+res3
                    params = {'name': '', 'string':  str(res3+'\n'+res1+'\n'+res2)}                    
                else:
                    query = base + " " + i[0] + " , " + i[1] + " and " + i[2]+" and "+i[3]
                    try:
                        s=search(query)    
                        url = s['url_suffix']

                        ss=url+" "+"(Ingredients Used : "+i[0] + "," + i[1] + " and " + i[2]+")"
                        res3=ss+'\n'+res3
                    except:
                        continue                    
                    res3='These are the best Large Recipes for your ingredients  : '+'\n'+res3
                    params = {'name': '', 'string':  str(res3+'\n'+res1+'\n'+res2)}
        else:
            a=djtext.split(",")
            a = list(combinations(a, 3))
            for i in a:
                if len(a) <= 3:
                    query = base + " " + i[0] + " and " + i[1] + " and " + i[2]
                    try:
                        s=search(query)    
                        url = s['url_suffix']

                        ss=url+" "+"(Ingredients Used : "+i[0] + "," + i[1] + " and " + i[2]+")"
                        res3=ss+'\n'+res3
                    except:
                        continue  
                    res3='These are the best Large Recipes for your ingredients  : '+'\n'+res3
                    params = {'name': '', 'string':  str(res3+'\n'+res1+'\n'+res2)}                    
                else:
                    query = base + " " + i[0] + " , " + i[1] + " and " + i[2]+" and "+i[3]
                    try:
                        s=search(query)    
                        url = s['url_suffix']

                        ss=url+" "+"(Ingredients Used : "+i[0] + "," + i[1] + " and " + i[2]+")"
                        res3=ss+'\n'+res3
                    except:
                        continue                    
                    res3='These are the best Large Recipes for your ingredients  : '+'\n'+res3
                    params = {'name': '', 'string':  str(res3+'\n'+res1+'\n'+res2)}
    return render(request, 'punc.html', params)
