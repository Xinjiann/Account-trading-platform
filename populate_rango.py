import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ITECH_Project.settings')

import django
django.setup()
from rango.models import Category,Page

def populate():
    

    LOL_pages = [
        {"title": "Official Website",
        "url":"https://www.leagueoflegends.com/en-gb/"}]

    CSGO_pages = [
        {"title":"Official Website",
        "url":"https://blog.counter-strike.net/"}]

    Overwatch_pages = [
        {"title":"Official Website",
        "url":"https://playoverwatch.com/en-gb/"}]


    cats = {"LOL": {"pages": LOL_pages,'likes':64},
        "CSGO": {"pages": CSGO_pages,'likes':34},
        "Overwatch": {"pages": Overwatch_pages,'likes':54}}

    
   
    for cat,cat_data in cats.items():
        c = add_cat(cat,cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c,p['title'],p['url'])



    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat,title,url,views=0):
    p = Page.objects.get_or_create(category=cat,title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name,likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes = likes
    c.save()
    return c


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
    
