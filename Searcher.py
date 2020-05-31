from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Searcher():

    def __init__(self,company_name,date,driver):
        self.date = date.split('-')
        self.day = int(self.date[2])
        self.month = int(self.date[1])
        self.year = int(self.date[0])
        self.day_lowrange = self.day - 2
        self.month_lowrange = self.month
        self.year_lowrange = self.year
        if (self.day > 28):
            self.day_highrange = 1
            self.month_highrange = self.month + 1
            self.year_highrange = self.year
        else:
            self.day_highrange = self.day + 2
            self.month_highrange = self.month
            self.year_highrange = self.year
        self.company = ""
        self.driver = driver
        self.search_id = "btnSearchBottom"
        self.from_day_id = "frd"
        self.from_month_id = "frm"
        self.from_year_id = "fry"
        self.to_day_id = "tod"
        self.to_month_id = "tom"
        self.to_year_id = "toy"
        self.selectiondate_id = "dr"
        self.company_id = "coTxt"
        self.timeout = 25
        self.companyname = company_name

    def Element_Loaded(self,id,debug=False):
        try:
            element_present = EC.presence_of_element_located((By.ID, str(id)))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            return False
        finally:
            pass
        return True

    def Element_Class_Loaded(self,classname,debug=False):
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, str(classname)))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            return False
        finally:
            pass
        return True

    def Select_CustomDateRange(self):
        while True:
            try:
                select = Select(self.driver.find_element_by_id(self.selectiondate_id))
                select.select_by_visible_text('Enter date range...')
                break
            except:
                time.sleep(3)

    def Enter_FromDate(self):
        time.sleep(2)
        while True:
            try:
                inputElement = self.driver.find_element_by_id(self.from_day_id).send_keys(self.day_lowrange)
                inputElement = self.driver.find_element_by_id(self.from_month_id).send_keys(self.month_lowrange)
                inputElement = self.driver.find_element_by_id(self.from_year_id).send_keys(self.year_lowrange)
                break
            except:
                time.sleep(3)

    def Enter_ToDate(self):
        inputElement = self.driver.find_element_by_id(self.to_day_id).send_keys(self.day_highrange)
        inputElement = self.driver.find_element_by_id(self.to_month_id).send_keys(self.month_highrange)
        inputElement = self.driver.find_element_by_id(self.to_year_id).send_keys(self.year_highrange)

    def Expand_JS(self):
        self.driver.execute_script("document.getElementById('coTab').click();")

    def Enter_Company(self):
        if (self.Element_Loaded(id="coTab")):
            time.sleep(3)
            while True:
                try:
                    self.Expand_JS()
                    # if (self.Element_Loaded(id=self.company_id)):
                    self.driver.find_element_by_id(self.company_id).send_keys(self.companyname)
                    break
                except:
                    time.sleep(3)

        if (self.Element_Class_Loaded(classname="dj_emg_autosuggest_even")):
            time.sleep(3)
            while True:
                try:
                    suggestions = self.driver.find_elements_by_class_name("dj_emg_autosuggest_even")
                    for suggestion in suggestions:
                        if (suggestion.find_element_by_class_name("ac_descriptor").text == "BP PLC"):
                            # print(suggestion.find_element_by_class_name("ac_descriptor").text)
                            suggestion.click()
                            break
                    break
                except:
                    time.sleep(3)

    def SubmitSearch(self):
        self.driver.find_element_by_id(self.search_id).click()

    # def Navigate_NextPage(self):
    #     self.driver.execute_script("viewNext('100');")
    #     time.sleep(20)

    # def GetAllArticles(self):
    #     # if (self.Element_Loaded(id="headline")):
    #     time.sleep(25)
    #     data = self.driver.find_elements_by_class_name("headline")
    #     print(len(data))
    #     return data
        # for singlerec in data:
        #     # print(singlerec.get_attribute('innerHTML'))
        #     values = singlerec.find_element_by_name("hdl").get_attribute('id')
        #     headline = singlerec.find_element_by_class_name("enHeadline")
        #     leads_source = singlerec.find_element_by_class_name("leadFields")
        #     snippet = singlerec.find_element_by_class_name("snippet")
        #     print(values)
        #     print(headline.text)
        #     print(leads_source.text)
        #     print(snippet.text)





