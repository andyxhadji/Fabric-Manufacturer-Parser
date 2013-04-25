#*********************************************************************
#interiors.py
#Gets info from a csv file of urls and inputs needed info to csv file
#Designers: Vaughan Designs, Wood and Hogan,John Rosselli Associates,
#Schumacher
#*********************************************************************

import csv
import os
import urllib2
import html5lib
from html5lib import treebuilders
from html5lib import treewalkers
import bs4
from bs4 import BeautifulSoup
import re

def main():
    path='URL_data.csv'
    urls=get_urls(path)
    parsed_data=parser(urls)
    print "Done!"

def get_urls(path):
# Get list of urls from csv file
    read=csv.reader(open(path, 'U'),delimiter=',')
    return [row[0] for row in read]

def parser(urls):
# Parses website page source
    start=input('What number do you want to start from?')
    new_path='Output_file.csv'
    writer=csv.writer(open(new_path, "wb"))
    for site in urls:
        open_site=urllib2.urlopen(site)
        soup = BeautifulSoup(open_site)
        designer_name=find_designer(soup)
        if designer_name=="Vaughan Designs":
            data=vaughan(soup, designer_name, site, start)
            writer.writerow(data)
        if designer_name=="Wood and Hogan":
            data=hogan(soup, designer_name, site, start)
            writer.writerow(data)
        if designer_name=="John Rosselli Associates":
            data=rosselli(soup, designer_name, site, start)
            writer.writerow(data)
        if designer_name=="Schumacher":
            data=schumacher(soup, designer_name, site, start)
            writer.writerow(data)            
        #insert next designer
        start=start+1

def find_designer(soup):
#finds correct designer so data can be extracted
    designer=soup.find_all(text=re.compile("Vaughan Designs"))
    if len(designer)>0:
        designer_name="Vaughan Designs"
    designer=soup.find_all(text=re.compile("Wood and Hogan"))
    if len(designer)>0:
        designer_name="Wood and Hogan"
    designer=soup.find_all(text=re.compile("Rosselli"))
    if len(designer)>0:
        designer_name="John Rosselli Associates"
    designer=soup.find_all(text=re.compile("Schumacher"))
    if len(designer)>0:
        designer_name="Schumacher"
    #insert next designer here
    return designer_name
        
        
    
def vaughan(soup, designer_name, site, start):
#extracts data from vaughan site
    model=soup.find_all('td', limit=2)
    model=model[1].get_text()
    item_name=soup.find(class_='itemName')
    item_name_string=item_name.get_text()
    dimensions=soup.find_all(class_='dimensionValue')
    height='0'
    if len(dimensions)>0:
        height=dimensions[0].get_text()
    width='0'
    if len(dimensions)>2:
        width=dimensions[2].get_text()
    depth='0'
    if len(dimensions)>4:
        depth=dimensions[4].get_text()
    description=item_name_string+'\n'+"Width:"+width+'"'+'\n'+\
                 "Height:"+height+'"'+ '\n'+ "Depth:"+depth+'"'
    data=[designer_name, site, item_name_string, model, "Width:"+width+'"', \
          "Height:"+height+'"', "Depth:"+depth+'"', ' ',description ]
    return data
    
def hogan(soup, designer_name, site, start):
#extracts data from wood and hogan site
    description=soup.find_all('p', limit=2)
    description_string=description[1].get_text()
    info=soup.find_all('br')
    item_name_string=str(info[4].nextSibling)
    model=str(info[3].previousSibling)
    dimensions=str(info[6].nextSibling)
    description=item_name_string+'\n'+dimensions
    data=[designer_name, site, item_name_string, model,dimensions,' ', ' ', ' ',description]
    return data

def rosselli(soup, designer_name, site, start):
    description=soup.find_all('br')
    item_name_string=str(description[1].nextSibling)
    info=description[2].nextSibling
    info=info.encode('ascii', 'ignore')
    for count in range(0, 5):
        if len(description)==count+4:
            dimensions=description[count].nextSibling
    dimensions=dimensions.encode('ascii', 'ignore')
    description=item_name_string+'\n'+info+'\n'+dimensions
    data=[designer_name, site, item_name_string, ' ', dimensions, ' ',' ',' ',description]
    roselli_images(soup, start)
    return data

def roselli_images(soup, start):
#pulls images from roselli website, saves and numbers them
    image=soup.find_all('img')
    image2=image[4]["src"]
    image_url="http://www.johnrosselliassociates.com/admin"+image2[7:]
    opener=urllib2.build_opener()
    page=opener.open(image_url)
    picture=page.read()
    filename=str(start)
    outfile=open(filename+".jpeg", "wb")
    outfile.write(picture)
    outfile.close

def schumacher(soup, designer_name, site, start):
    item_name = soup.find_all('h1')
    item_name_string = item_name[0].get_text()
    item_color = soup.find_all('h2')
    item_color_string = item_color[0].get_text()
    dimensions = soup.find_all('li')
    width_string = dimensions[1].get_text()
    horizontal_repeat_string = dimensions[2].get_text()
    vertical_repeat_string = dimensions[3].get_text()
    fabric_string = dimensions[4].get_text()
    country_string = dimensions[5].get_text()
    item_name_string=item_name_string.encode('ascii', 'ignore')
    item_color_string=item_color_string.encode('ascii', 'ignore')
    width_string=width_string.encode('ascii', 'ignore')
    vertical_repeat_string=vertical_repeat_string.encode('ascii', 'ignore')
    fabric_string=fabric_string.encode('ascii', 'ignore')
    country_string=country_string.encode('ascii', 'ignore')
    horizontal_repeat_string=horizontal_repeat_string.encode('ascii', 'ignore')
    total_description_string = item_name_string + '\n' + item_color_string \
                               + '\n' + width_string + '\n' + horizontal_repeat_string \
                               + '\n' + vertical_repeat_string + '\n' + fabric_string \
                               + '\n' + country_string
    data = [designer_name, site, ' ', ' ', ' ', ' ', ' ', item_color_string, total_description_string]
    return data
                               
    
    
    
              
#call the main function
main()
