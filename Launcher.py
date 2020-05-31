from Authenticate_Selenium import Authenticate
from Searcher import Searcher
from Scrapper import Scrapper
import time
import pandas as pd
import threading

class Threaded_Selenium():
    def __init__(self):
        self.obj = None
        self.obj1 = None
        self.obj2 = None
        self.obj3 = None
        self.obj4 = None

    def csvLoader(self):
        data = pd.read_excel("projectdata.xls")
        return data

    def run_authenticate_0(self,value):
        obj = Authenticate(headlessoption=False)
        obj.debug = True
        obj.LoginUser()
        obj.MigrateSeleniumtoRequests()
        if(value == 1):
            self.obj = obj
        elif(value == 2):
            self.obj1 = obj
        elif(value == 3):
            self.obj2 = obj
        elif (value == 4):
            self.obj3 = obj
        elif (value == 5):
            self.obj4 = obj

    def run_Scrapper_0(self,value,companyname,date):
        obj_local = None
        if (value == 1):
            obj_local = self.obj
        elif (value == 2):
            obj_local = self.obj1
        elif (value == 3):
            obj_local = self.obj2
        elif (value == 4):
            obj_local = self.obj3
        elif (value == 5):
            obj_local = self.obj4

        obj_local.Post_Factiva_Home_Request()
        obj1 = Searcher(company_name=companyname,date=date, driver=obj_local.driver)
        obj1.Select_CustomDateRange()
        obj1.Enter_FromDate()
        obj1.Enter_ToDate()
        obj1.Enter_Company()
        obj1.SubmitSearch()

        obj2 = Scrapper(driver=obj_local.driver, session=obj_local.session)
        obj2.MigrateSeleniumtoRequests()
        count_ = 1
        while True:
            obj2.GetAllArticles()
            obj2.Parse_Articles()
            check = obj2.Navigate_NextPage(count=count_)
            if (check):
                break
            count_ += 1

        obj2.Save_ToDataFrame(companyname=companyname,date=date)

    def Auth_thread(self):
        x = threading.Thread(target=self.run_authenticate_0,args=(1,))
        y = threading.Thread(target=self.run_authenticate_0,args=(2,))
        z = threading.Thread(target=self.run_authenticate_0,args=(3,))
        a = threading.Thread(target=self.run_authenticate_0, args=(4,))
        b = threading.Thread(target=self.run_authenticate_0, args=(5,))

        a.start()
        b.start()
        x.start()
        y.start()
        z.start()

        a.join()
        b.join()
        x.join()
        y.join()
        z.join()

    def Scrapper_Thread(self,com,com1,com2,com3,com4,d0,d1,d2,d3,d4):
        x = threading.Thread(target=self.run_Scrapper_0, args=(1,com,d0))
        y = threading.Thread(target=self.run_Scrapper_0, args=(2,com1,d1))
        z = threading.Thread(target=self.run_Scrapper_0, args=(3,com2,d2))
        a = threading.Thread(target=self.run_Scrapper_0, args=(4,com3, d3))
        b = threading.Thread(target=self.run_Scrapper_0, args=(5,com4, d4))

        a.start()
        b.start()
        x.start()
        y.start()
        z.start()

        a.join()
        b.join()
        x.join()
        y.join()
        z.join()

    def run(self,):
        data = self.csvLoader()
        self.Auth_thread()

        for i in range(0,data.shape[0],5):
            record = data.iloc[i]
            company = str(record[0]).split("(")[0].strip()
            date = str(record[1]).split(" ")[0].strip()
            print("|#| -> Company: ",company, ", Date: ",date)

            record_1 = data.iloc[i+1]
            company_1 = str(record_1[0]).split("(")[0].strip()
            date_1 = str(record_1[1]).split(" ")[0].strip()
            print("|#| -> Company-1: ", company_1, ", Date-1: ", date_1)

            record_2 = data.iloc[i+2]
            company_2 = str(record_2[0]).split("(")[0].strip()
            date_2 = str(record_2[1]).split(" ")[0].strip()
            print("|#| -> Company-2: ", company_2, ", Date-2: ", date_2)

            record_3 = data.iloc[i+3]
            company_3 = str(record_3[0]).split("(")[0].strip()
            date_3 = str(record_3[1]).split(" ")[0].strip()
            print("|#| -> Company-3: ", company_3, ", Date-3: ", date_3)

            record_4 = data.iloc[i+4]
            company_4 = str(record_4[0]).split("(")[0].strip()
            date_4 = str(record_4[1]).split(" ")[0].strip()
            print("|#| -> Company-4: ", company_4, ", Date-4: ", date_4)
            self.Scrapper_Thread(com=company,com1=company_1,com2=company_2,com3=company_3,com4=company_4
                                 ,d0=date,d1=date_1,d2=date_2,d3=date_3,d4=date_4)



op = Threaded_Selenium()
op.run()