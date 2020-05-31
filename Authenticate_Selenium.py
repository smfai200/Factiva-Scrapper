from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup

class Authenticate():
    def __init__(self,headlessoption):
        self.username = "12203271"
        self.password = "rahatuom@331"
        self.Loginurl = "https://search.lib.uts.edu.au/view/action/uresolver.do?operation=resolveService&package_service_id=2506511000005671&institutionId=5671&customerId=5670"
        self.timeout = 3
        self.session = requests.session()
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0 Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language":"en-US,en;q=0.5"
        }
        self.debug = False
        self.options = Options()
        self.options.headless = headlessoption
        self.driver = webdriver.Chrome(ChromeDriverManager(path="D:\\").install(),chrome_options=self.options)
        # self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=r'Webdriver\chromedriver.exe')
        #self.driver = webdriver.Firefox(firefox_options=self.options, executable_path=r'Webdriver\geckodriver.exe')

    def ClickNoticeOK(self):
        self.driver.find_element_by_id("okBtn").click()
        pass

    def GetRequest(self,url,debug=False):
        self.driver.get(url)
        if (debug or self.debug):
            print("\n\n|1| > Login Url Request Processing: {0}".format(self.driver.current_url))

    def Page_Loaded(self,id,debug=False):
        try:
            element_present = EC.presence_of_element_located((By.ID, str(id)))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            return False
        finally:
            pass
        return True

    def Page_Loaded_BasedonURL(self,url,debug=False):
        while True:
            if (url in self.driver.current_url):
                break
            else:
                time.sleep(3)

        return True

    def LoginForm_Fill(self,debug=False):
        try:
            username = self.driver.find_element_by_id("username")
            username.clear()
            username.send_keys(self.username)

            password = self.driver.find_element_by_name("password")
            password.clear()
            password.send_keys(self.password)
        except:
            return False
        return True

    def MigrateSeleniumtoRequests(self):
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

    def Post_Factiva_Home_Request(self):
        url = "https://global-factiva-com.ezproxy.lib.uts.edu.au/sb/default.aspx?lnep=hp"
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
        }

        response = self.session.get(url, headers=headers,verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("form")
        # return response

    def get_form_details(self,form):
        details = {}
        action = str(form.attrs.get("action")).lower()
        method = str(form.attrs.get("method", "get")).lower()
        inputs = []
        for input_tag in form.find_all("input"):
            # input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value = input_tag.attrs.get("value", "")
            details[input_name] = input_value
        return details

    def LoginUser(self,debug=False):
        check_Bool = False
        self.GetRequest(url=self.Loginurl)
        if(self.Page_Loaded(id="password")):
            if(self.LoginForm_Fill()):
                self.driver.find_element_by_name("submit").click()
                time.sleep(20)
                self.ClickNoticeOK()

                if(self.Page_Loaded_BasedonURL(url="?lnep=hp")):
                    self.timeout = 30
                    check_Bool = True
                    #self.MigrateSeleniumtoRequests()
                    if (self.Page_Loaded(id="dr")):
                        pass

        if (debug or self.debug):
            if (check_Bool):
                print("|2| > Login Successful")
                print("\t|$| => Current Window URL : {0}".format(self.driver.current_url))
                print("\t|$| => Current Window Title : {0}".format(self.driver.title))
                return
                # print("\t|$| => Migrated Cookies : {0}".format(self.session.cookies.get_dict()))
                # reponse = self.Post_Factiva_Home_Request()
                # print(reponse.text)
            else:
                print("\n\n|2| > Login Failed")
