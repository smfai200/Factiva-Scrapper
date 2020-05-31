from Articles_Model import Articles_Model
import time
import pandas as pd

class Scrapper():
    def __init__(self,driver,session):
        self.driver = driver
        self.data = None
        self.session = session
        self.MigrateSeleniumtoRequests()
        self.articleslist = []
        self.duplicatelist = []

    def Navigate_NextPage(self,count):
        self.driver.execute_script("viewNext('"+str(count)+"00');")
        time.sleep(20)
        if("No search results" in self.driver.page_source):
            return True
        return False

    def GetAllArticles(self):
        while True:
            try:
                data = self.driver.find_elements_by_class_name("headline")
                self.data = data
                if(len(data) <= 0):
                    raise Exception("Exception")
                print(len(self.data))
                break
            except:
                time.sleep(3)

    def Read_FullArticle(self,value):
        script = "article_click(this,'"+str(value)+"');"
        time.sleep(3)
        ArticleText = ""
        while True:
            try:
                self.driver.execute_script(script)
                time.sleep(7)
                articletext = self.driver.find_elements_by_class_name("articleParagraph")
                for singlearticle in articletext:
                    ArticleText = ArticleText+"\n"+str(singlearticle.text)
                break
            except:
                time.sleep(3)

        return ArticleText

    def Request_FullArticle(self,value):
        url = "https://global-factiva-com.ezproxy.lib.uts.edu.au/du/article.aspx/?accessionno="+value+"&fcpil=en&napc=S&sa_from=&cat=a"
        result = self.session.get(url=url)
        print(result.text)

    def MigrateSeleniumtoRequests(self):
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

    def Parse_Articles(self):
        for singlerec in self.data:
            model = Articles_Model()
            model.values = singlerec.find_element_by_name("hdl").get_attribute('id')
            model.title = singlerec.find_element_by_class_name("enHeadline").text
            print("Article: ", model.title, " , ", model.FullArticle[:10], ", ", len(model.FullArticle))
            model.leads_source = singlerec.find_element_by_class_name("leadFields").text
            model.snippet = singlerec.find_element_by_class_name("snippet").text
            model.FullArticle = self.Read_FullArticle(value=model.values)
            if (model in self.articleslist):
                print("Failed")
                return "Fail"
            self.articleslist.append(model.to_dict())

    def Save_ToDataFrame(self,companyname,date):
        df = pd.DataFrame(self.articleslist)
        try:
            df.to_excel(str(companyname)+str(date)+str(".xls"))
        except:
            df.to_excel(str(companyname[:10]) + str(date) + str(".xls"))
        # df.to_csv(str(sel"BP_PLC.csv")


