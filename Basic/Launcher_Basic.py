from Basic.Basic_Authenticate_Selenium import Authenticate
from Basic.Searcher_Basic import Searcher
from Basic.Scrapper_Basic import Scrapper
import pandas as pd
import time
import concurrent.futures

def csvLoader():
    data = pd.read_excel("projectdata.xls")
    return data

def Generic_Authenticate():
    def VerifyLogin():
        obj.debug = True
        obj.LoginUser()
        obj.MigrateSeleniumtoRequests()
        return True

    obj = Authenticate(headlessoption=False)
    LoggedInStatus = VerifyLogin()
    return obj.session,obj.driver

def Retrieve_All_Pages(obj):
    pages = []
    for i in range(1,20):
        soup = obj.NextPage(count=i)
        if (soup == False):
            break
        else:
            pages.append(soup)
    return pages

def CompanyExtraction():
    pass

def run():
    data = csvLoader()
    session,driver = Generic_Authenticate()
    obj2 = Scrapper(session=session)

    companyrecords = []
    for singledata in data.iterrows():
        record = list(singledata[1])
        company = str(record[0]).split("(")[0].strip()
        date = str(record[1]).split(" ")[0]
        print("|#| -> Company: ",company, ", Date: ",date)

        obj1 = Searcher(company_name=company,date=date, driver=driver, session=session)
        obj1.SetSearchRequest()
        AllPages_Parsed = Retrieve_All_Pages(obj=obj1)
        companyrecords.append({
            "Company":company,
            "Date":date,
            "Records":len(AllPages_Parsed)
        })
        print("Pages: ", len(AllPages_Parsed))

    df_new = pd.DataFrame(companyrecords)
    df_new.to_csv("Records_List.csv")
    return

    # obj1 = Searcher(date="12-17-2007",driver=driver,session=session)
    #
    # output = obj1.SetSearchRequest()
    # AllPages_Parsed = Retrieve_All_Pages(obj=obj1)
    # AllPages_Parsed.append(output)
    # print("Pages: ",len(AllPages_Parsed))
    # Allarticles  = []
    # for singleoutput in AllPages_Parsed:
    #     obj2.Scrape_All(soup=singleoutput)
    #
    # Allarticles.append(obj2.Confirmed_Articles())
    # obj2.Save_ToDataFrame(articleslist=Allarticles[0])
    #
    # print("All-Articles: ",Allarticles)
    # print("All-Articles Length: ",len(Allarticles))



#csvLoader()
run()