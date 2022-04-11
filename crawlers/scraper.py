from bs4 import BeautifulSoup
import urllib.request,sys,time,os
import requests
import json
import pymongo



#Creating the database

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["news_db"]
mycol = mydb["articles"]

list_of_urls = """https://www.ertnews.gr/
https://www.stratologia.gr/
https://www.protothema.gr/
https://www.newsit.gr/
https://www.iefimerida.gr/
https://www.news247.gr/
https://www.newsbomb.gr/
https://www.in.gr/
https://www.newsbeast.gr/
https://www.kathimerini.gr/
https://www.enikos.gr/
https://naftemporiki.gr/
https://www.parapolitika.gr/
https://www.ethnos.gr/
https://www.tovima.gr/
http://e-amyna.com/
https://www.avgi.gr/
https://www.tanea.gr/
https://www.topontiki.gr/
https://www.agon.gr/
https://neoiagones.gr/""".split("\n")

ts = time.time()
data = "data_"+str(ts)
os.mkdir(data)

for URL in list_of_urls:
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    try:
        page = requests.get(URL, headers = headers)
    except requests.exceptions.SSLError:
        page = requests.get(URL, headers=headers, verify = False)


    soup = BeautifulSoup(page.content, "html.parser")

    # Get time and date of the article
    

    # Find text in a tags and strip it
    news_elements = soup.find_all("a")
    news_dict = {}
    for news in news_elements:
        news_list = news.text.split('\n')
        
        for element in news_list:
            
            if len(element.split()) >= 3  and (news.get("href", "").startswith("http") or news.get("href", "").startswith("/")) :
                
                new_url = news["href"]
                if new_url.startswith("/"):
                    new_url = URL +new_url
                if new_url.startswith(URL):
                    news_dict[new_url] =  element.strip()

                

            

    # print(list)
  
    with open(data+"/" + URL.split("//")[-1].split("/")[0],"w") as f:
        for i in news_dict.items():
            json_obj = {"url":i[0], "title":i[1], "time": ts }
            #f.write(" , ".join(i)+"\n") 
            f.write(json.dumps(json_obj, ensure_ascii=False) +" \n")
            mycol.insert_one(json_obj)
            



    # time.sleep(2)


    # print(page.text)

