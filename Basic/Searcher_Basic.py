import json
from bs4 import BeautifulSoup

class Searcher():

    def __init__(self,company_name,date,driver,session):
        self.date = date.split('-')
        self.day = int(self.date[2])
        self.month = int(self.date[1])
        self.year = int(self.date[0])
        self.day_lowrange = self.day - 2
        self.month_lowrange = self.month
        self.year_lowrange = self.year
        if(self.day > 28):
            self.day_highrange = 1
            self.month_highrange = self.month+1
            self.year_highrange = self.year
        else:
            self.day_highrange = self.day + 2
            self.month_highrange = self.month
            self.year_highrange = self.year
        self.company = ""
        self.driver = driver
        self.session = session
        self.timeout = 25
        self.companyname = company_name
        self.payload_global = '''ht=Advanced&ipid=&ipin=&ipgi=False&isst=LegacySavedSearch&PageScriptManager_HiddenField=;;EMG.Toolkit.Web,+Version=1.2.0.10,+Culture=neutral,+PublicKeyToken=null:en-US:55db77bb-794f-4654-8902-b81d872e89e8:5502fedf;AjaxControlToolkit,+Version=3.0.30930.28736,+Culture=neutral,+PublicKeyToken=28f01b0e84b6d53e:en-US:b0eefc76-0092-471b-ab62-f3ddc8240d71:e2e86ef9:a9a7729d:9ea3f0e2:1df13a87:8ccd9c1b:bae32fb7:182913ba:9e8e87e9:4c9865be:ba594826:507fcf1b:c7a4182e;EMG.Toolkit.Web,+Version=1.2.0.10,+Culture=neutral,+PublicKeyToken=null:en-US:55db77bb-794f-4654-8902-b81d872e89e8:7ddfc2a5:6f871244:4519dc77:bc5d12e6:25499212:80ba8c1:22998473:25f53794&_XFORMSESSSTATE=ACN7MDp7VToiL3NiL2RlZmF1bHQuYXNweCIsMTg3OnswOjAsMjoiUyIsMzpbXSw0OiJlbiIsNaADDTE6MSwyOjAsMzoiOUFVUyJ4AwACbW9uaXNoYS5nOEBnbWFpbC5jb21gBgBRIkU2T08ySFZDUUhWUEZRQzJONURFRjVLRUNZIiw2OiIxOCIsNzp7MToiNzA3MjA4ODMxRUQ4MDEwM0U1MDAwNkQyNjRDODMyODFBM0YwQzA1RTAxODBCQTAwMTB8MjJ8NXwwKQcANXw1KjgALCwADDV8LTF8MjA0OHwxMCIsMGwZDSJjb2V4ZSwwLDA7Y290cm6EAQARZW50d3NqcCwyO2NvY3VzLDAiLDE6ImR0bW9uLDA7QkVJSlh8BJQbBjAwODYifX0sOIgYAAo1QzA4QzQwMUQwMTAwQ0MwMDMxMXwwMjExMDIwJwAAAjExMjEweBeFAjFlATKoGJISMjJgEwIxfSwyM2wKAzAsMDowfXQVdC4IMDoxfSwxMTowLDFTL0FsbGwvkDVsAqwyAjB9LDI0bAgDMCwxOjEyZzV9LDKINwVbezA6ImRvdI4zMTpsAwAbIjgifV19LDE3Ont9LDE0OjEsOTowfX0sOToidXRzMDIifSw2OjAsNzoibWJtWCYKODoibWJtMC0wIn19fREAAEQCAAA=&_XFORMSTATE=AAJ7MTp7MjY6ezExOjAsMjE6W10sM2kBNXAABDE0OjAsMzRxAjSWADI5YAJwAAMxNzowLDVlATNlATRxADVyADczYQkyfASQAAI4OjAsNmYBMTVkBnIANjWFCjh1ADZqDDQwiAECMDowLDGZBzN9ATOVADRhAjGsBWgBhgExNnQKiQE1agE1MmAGlAh8FoAHCTY6W10sNzpbXX19fREAAOYAAAA=&__VIEWSTATE=&directLinkURLName=Factiva&directLinkURLHRef=https://global-factiva-com.ezproxy.lib.uts.edu.au/en/du/search.asp?accountid=9THE011100&namespace=18&scs=[]&xsc=[]&sls=[]&xsls=[]&als=[]&xaul=[]&xil=[]&ils=[]&xrl=[]&rls=[]&xnl=[]&nls=[]&xpl=[]&pls=[]&aus=[]&xau=[]&xco=[]&cls=[]&xcl=[]&pes=[]&xpe=[]&nss=[]&xns=[]&ins=[]&xin=[]&res=[]&xre=[]&ipcl=[EN]&iadmio=False&ist=Advanced&iceu=0&fess=[]&iefs=[]&sicr=0&aicr=0&cicr=0&nsicr=0&iicr=0&ricr=0&pecr=0&flagBox=lo&scrAllPub={14:1,0:0,11:"P|",12:0,4:0,5:0,6:0,7:0,8:"All+Publications",10:0}&scrAllWeb={14:3,0:0,11:"W|",12:0,4:0,5:0,6:0,7:0,8:"All+Web+News",10:0}&scrAllPic={14:2,0:0,11:"I|",12:0,4:0,5:0,6:0,7:0,8:"All+Pictures",10:0}&scrAllMlt={14:5,0:0,11:"M|",12:0,4:0,5:0,6:0,7:0,8:"All+Multimedia",10:0}&scrAllBlg={14:6,0:0,11:"B|",12:0,4:0,5:0,6:0,7:0,8:"All+Blogs",10:0}&searchBuilder=1&atx=&otx=&ntx=&htx=&ftx=&inasm=false&sbFTQSize=2048&dr=Custom'''

    def Post_Factiva_Home_Request(self):
        url = "https://global-factiva-com.ezproxy.lib.uts.edu.au/sb/default.aspx?lnep=hp"
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
        }

        response = self.session.get(url, headers=headers,verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_CompanySuggestions(self,suggestContextvalue,companyname):
        url = "https://suggest-factiva-com.ezproxy.lib.uts.edu.au/Search/2.0/Company?timestamp=1589961763660"
        url += "&format=json"
        url += "&maxResults=10"
        url += "&autocompletionType=Company"
        url += "&suggestContext="+str(suggestContextvalue) #YPC0P9uW1Y1h0s_2Fv0nvy9KEpZNqzujMimbpcY1Q8bM8zfMu7_2B7NJAjf3nLnjaL_2Fr9BkFG61HWBU_3D%7C2"
        url += "&columnCount=1"
        url += "&searchText="+str(companyname).replace(" ","+")
        url += "&showViewAllPrivateMarkets=false"
        url += "&dataSet=newsCodedAbt"
        url += "&filterADR=false"
        url += "&callback=_jqjsp&_1589961763660="

        response = self.session.get(url=url)
        result_text = str(response.text)[8:-1].strip()
        json_object = json.loads(result_text)
        companies = json_object["company"]
        ##[{5:"BAMRCI",29:"BP America Inc"},{5:"BECATO",29:"BTG Hotels (Group) Co., Ltd."}]
        listofcompanies = []
        for company in companies:
            data = {
                5:company["code"],
                29:company["matchedOn"],
                "base_score" : company["baseScore"]
            }
            listofcompanies.append(data)

        return listofcompanies

    def Set_Dates(self):
        query = "&frd=" + str(self.day_lowrange)
        query += "&frm=" + str(self.month_lowrange)
        query += "&fry="+ str(self.year_lowrange)
        query += '''&dateFrom_txb=________&dateFrom_extc_ClientState={"CalendarPosition":1,"CalendarDateDisplayFormat":"d+MMMM+yyyy","CalendarMonthYearDisplayFormat":"MMM,+yyyy"}&dateFrom_extc__MaskedEditExtender_ClientState=&'''
        query += "tod=" + str(self.day_highrange)
        query += "&tom=" + str(self.month_highrange)
        query += "&toy=" + str(self.year_highrange)
        query += '''&dateTo_txb=________&dateTo_extc_ClientState={"CalendarPosition":0,"CalendarDateDisplayFormat":"d+MMMM+yyyy","CalendarMonthYearDisplayFormat":"MMM,+yyyy"}&dateTo_extc__MaskedEditExtender_ClientState=&frdt=&todt=&dfmt=DDMMCCYY&isrd=High&srcNmOnly=on&excDiscSrcs=on&cop=Or&sop=Or&iop=Or&rop=Or&srcNmOnlylk=on&excDiscSrcslk=on&sfd=&istesfn=False&ister=False&isteo=False&hso=PublicationDateMostRecentFirst'''
        self.payload_global += query

    def Set_Company(self,companylist):
        query = '''&cos=['''
        for singlecompany in companylist:
            if (singlecompany[29] == self.companyname):
                matchedOn = str(singlecompany[29]).replace(" ","+")
                code = str(singlecompany[5])

                query += '''{5: "'''+str(code)+'''", '''
                query += '''29: "'''+ str(matchedOn) +'''"}'''
                break

        query += ''']'''
        self.payload_global += query
        return True

    def Construct_PostData(self):
        def Extract_SuggestContext():
            response = self.Post_Factiva_Home_Request()
            suggestContextvalue = None
            script_tag = response.find_all("script")
            for i in range(0,len(script_tag)):
                if("suggestContext" in script_tag[i].text and
                    "Search/2.0" in script_tag[i].text):
                    suggestContextvalue = str(script_tag[i].text).split(',\r\n')[14].strip()
                    suggestContextvalue = suggestContextvalue.split(':')[1].strip().replace("'","")

            return suggestContextvalue

        def InjectCompany(suggestContextvalue,companyname):
            listofcompanies = self.get_CompanySuggestions(suggestContextvalue=suggestContextvalue,companyname=companyname)
            self.Set_Company(companylist=listofcompanies)

        def InjectDates():
            self.Set_Dates()

        suggestContextvalue = Extract_SuggestContext()
        InjectCompany(suggestContextvalue,companyname=self.companyname)
        InjectDates()
        self.payload_global += "&hs=0"

    def SetSearchRequest(self):
        self.Construct_PostData()
        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
        }
        url = "https://global-factiva-com.ezproxy.lib.uts.edu.au/ha/default.aspx"
        #payload = '''hs=0&ht=Advanced&ipid=&ipin=&ipgi=False&isst=LegacySavedSearch&PageScriptManager_HiddenField=%3B%3BEMG.Toolkit.Web%2C+Version%3D1.2.0.10%2C+Culture%3Dneutral%2C+PublicKeyToken%3Dnull%3Aen-US%3A55db77bb-794f-4654-8902-b81d872e89e8%3A5502fedf%3BAjaxControlToolkit%2C+Version%3D3.0.30930.28736%2C+Culture%3Dneutral%2C+PublicKeyToken%3D28f01b0e84b6d53e%3Aen-US%3Ab0eefc76-0092-471b-ab62-f3ddc8240d71%3Ae2e86ef9%3Aa9a7729d%3A9ea3f0e2%3A1df13a87%3A8ccd9c1b%3Abae32fb7%3A182913ba%3A9e8e87e9%3A4c9865be%3Aba594826%3A507fcf1b%3Ac7a4182e%3BEMG.Toolkit.Web%2C+Version%3D1.2.0.10%2C+Culture%3Dneutral%2C+PublicKeyToken%3Dnull%3Aen-US%3A55db77bb-794f-4654-8902-b81d872e89e8%3A7ddfc2a5%3A6f871244%3A4519dc77%3Abc5d12e6%3A25499212%3A80ba8c1%3A22998473%3A25f53794&_XFORMSESSSTATE=ACN7MDp7VToiL3NiL2RlZmF1bHQuYXNweCIsMTg3OnswOjAsMjoiUyIsMzpbXSw0OiJlbiIsNaADDTE6MSwyOjAsMzoiOUFVUyJ4AwACbW9uaXNoYS5nOEBnbWFpbC5jb21gBgBRIkU2T08ySFZDUUhWUEZRQzJONURFRjVLRUNZIiw2OiIxOCIsNzp7MToiNzA3MjA4ODMxRUQ4MDEwM0U1MDAwNkQyNjRDODMyODFBM0YwQzA1RTAxODBCQTAwMTB8MjJ8NXwwKQcANXw1KjgALCwADDV8LTF8MjA0OHwxMCIsMGwZDSJjb2V4ZSwwLDA7Y290cm6EAQARZW50d3NqcCwyO2NvY3VzLDAiLDE6ImR0bW9uLDA7QkVJSlh8BJQbBjAwODYifX0sOIgYAAo1QzA4QzQwMUQwMTAwQ0MwMDMxMXwwMjExMDIwJwAAAjExMjEweBeFAjFlATKoGJISMjJgEwIxfSwyM2wKAzAsMDowfXQVdC4IMDoxfSwxMTowLDFTL0FsbGwvkDVsAqwyAjB9LDI0bAgDMCwxOjEyZzV9LDKINwVbezA6ImRvdI4zMTpsAwAbIjgifV19LDE3Ont9LDE0OjEsOTowfX0sOToidXRzMDIifSw2OjAsNzoibWJtWCYKODoibWJtMC0wIn19fREAAEQCAAA%3D&_XFORMSTATE=AAJ7MTp7MjY6ezExOjAsMjE6W10sM2kBNXAABDE0OjAsMzRxAjSWADI5YAJwAAMxNzowLDVlATNlATRxADVyADczYQkyfASQAAI4OjAsNmYBMTVkBnIANjWFCjh1ADZqDDQwiAECMDowLDGZBzN9ATOVADRhAjGsBWgBhgExNnQKiQE1agE1MmAGlAh8FoAHCTY6W10sNzpbXX19fREAAOYAAAA%3D&__VIEWSTATE=&directLinkURLName=Factiva&directLinkURLHRef=https%3A%2F%2Fglobal-factiva-com.ezproxy.lib.uts.edu.au%2Fen%2Fdu%2Fsearch.asp%3Faccountid%3D9THE011100%26namespace%3D18&scs=%5B%5D&xsc=%5B%5D&sls=%5B%5D&xsls=%5B%5D&als=%5B%5D&xaul=%5B%5D&xil=%5B%5D&ils=%5B%5D&xrl=%5B%5D&rls=%5B%5D&xnl=%5B%5D&nls=%5B%5D&xpl=%5B%5D&pls=%5B%5D&aus=%5B%5D&cos=%5B%5D&xau=%5B%5D&xco=%5B%5D&cls=%5B%5D&xcl=%5B%5D&pes=%5B%5D&xpe=%5B%5D&nss=%5B%5D&xns=%5B%5D&ins=%5B%5D&xin=%5B%5D&res=%5B%5D&xre=%5B%5D&ipcl=%5BEN%5D&iadmio=False&ist=Advanced&iceu=0&fess=%5B%5D&iefs=%5B%5D&sicr=0&aicr=0&cicr=1&nsicr=0&iicr=0&ricr=0&pecr=0&flagBox=lo&scrAllPub=%7B14%3A1%2C0%3A0%2C11%3A%22P%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Publications%22%2C10%3A0%7D&scrAllWeb=%7B14%3A3%2C0%3A0%2C11%3A%22W%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Web+News%22%2C10%3A0%7D&scrAllPic=%7B14%3A2%2C0%3A0%2C11%3A%22I%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Pictures%22%2C10%3A0%7D&scrAllMlt=%7B14%3A5%2C0%3A0%2C11%3A%22M%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Multimedia%22%2C10%3A0%7D&scrAllBlg=%7B14%3A6%2C0%3A0%2C11%3A%22B%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Blogs%22%2C10%3A0%7D&searchBuilder=1&atx=&otx=&ntx=&htx=&ftx=fds%3Dbp&inasm=false&sbFTQSize=2048&dr=Custom&frd=12&frm=01&fry=2008&dateFrom_txb=________&dateFrom_extc_ClientState=%7B%22CalendarPosition%22%3A1%2C%22CalendarDateDisplayFormat%22%3A%22d+MMMM+yyyy%22%2C%22CalendarMonthYearDisplayFormat%22%3A%22MMM%2C+yyyy%22%7D&dateFrom_extc__MaskedEditExtender_ClientState=&'''
        response = self.session.post(url=url,data=self.payload_global, headers=headers,verify=False)
        soup = BeautifulSoup(response.text,'html.parser')
        return soup

    def NextPage(self,count):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
        }
        url = "https://global-factiva-com.ezproxy.lib.uts.edu.au/ha/default.aspx"
        payload = self.payload_global[:-1]
        payload += str(count)+"00"
        response = self.session.post(url=url, data=payload, headers=headers, verify=False)
        print(response.text)
        if ("No search" in response.text):
            return False
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
