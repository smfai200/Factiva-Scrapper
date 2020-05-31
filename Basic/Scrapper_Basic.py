from Articles_Model import Articles_Model
import time
import pandas as pd
from bs4 import BeautifulSoup
# from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

class Scrapper():
    def __init__(self,session,driver=None):
        self.driver = driver
        self.data = None
        self.session = session
        self.articleslist = []

    def Navigate_ToFullArticleText(self,url):
        response = self.session.get(url=url,timeout=15)
        if ("doLinkPost" in response.text):
            pass
        else:
            return False,False
        soup = BeautifulSoup(response.text,'html.parser')
        script_tag = soup.find_all("script")
        ArticleText = ""
        for i in range(0, len(script_tag)):
            if("doLinkPost" in script_tag[i].text):
                script = script_tag[i].text
                payload = {
                    "_XFORMSTATE":str(script.split('(')[1].split(')')[0].split(",")[1].replace('''"''', "")),
                    "_XFORMSESSSTATE": str(script.split('(')[1].split(')')[0].split(",")[2].replace('''"''', ""))
                }
                URL = script.split('(')[1].split(')')[0].split(",")[0].replace('''"''', "")
                headers_new = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
                }
                result = self.session.post(url=URL,data=payload,headers=headers_new,timeout=40)
                soup = BeautifulSoup(result.text,'html.parser')
                articleparagraphs = soup.find_all('div', {"class": "enArticle"})
                paragraphs = soup.find_all('p', {"class": "articleParagraph"})
                headertitle = [a.text for a in articleparagraphs]
                for singlearticle in paragraphs:
                    ArticleText = ArticleText+"\n"+str(singlearticle.text)

        if(len(headertitle) >= 1):
            return ArticleText,headertitle[0]

        return ArticleText, "No Header"

    def Scrape_Parallel(self,article):
        try:
            model = Articles_Model()
            headline = article.find('a',{"class":"enHeadline"})
            model.title = headline.text.strip()
            model.values = "https://global-factiva-com.ezproxy.lib.uts.edu.au"+headline["href"].strip()[2:]
            model.leads_source =  article.find('div',{"class":"leadFields"}).text.strip()
            model.snippet = article.find('div', {"class": "snippet"}).text.strip()
            ArticleText,ArticleHeader = self.Navigate_ToFullArticleText(url=model.values)
            print("Title: ",model.title, "Values: ",model.values)
            model.ArticleHeader = ArticleHeader
            model.FullArticle = ArticleText
            self.articleslist.append(model.to_dict())
            return model
        except Exception as e:
            return

    def Scrape_All(self,soup):
        All_Articles_Metadata = soup.find_all('tr',attrs={"class":"headline"})
        print("Scrapping: ",len(All_Articles_Metadata))
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_url = {executor.submit(self.Scrape_Parallel, url): url for url in All_Articles_Metadata}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    print(data)
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    print('Page is %d bytes' % (len(self.articleslist)))

    def Confirmed_Articles(self):
        confirmed_articles = []
        for singlearticle in self.articleslist:
            if (not singlearticle["full_text"] is "" or not singlearticle["full_text"] is ''):
                confirmed_articles.append(singlearticle)

        print("Success Articles: ", len(confirmed_articles))
        print(self.articleslist)
        print(len(self.articleslist))
        return confirmed_articles

    def Save_ToDataFrame(self,articleslist):
        df = pd.DataFrame(articleslist)
        df.to_csv("BP_PLC.csv")