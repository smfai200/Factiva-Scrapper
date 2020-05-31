import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import warnings
warnings.filterwarnings("ignore")

class Authenticate():
    def __init__(self):
        self.username = "12203271"
        self.password = "rahatuom@331"
        self.session = requests.session()
        self.Loginurl = ""
        self.ticketvalue = ""
        self.xsid = ""
        self.vidvalue = ""
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0 Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language":"en-US,en;q=0.5"
        }
        self.debug = False
        #self.driver = webdriver.Firefox(executable_path="")
        self.options = Options()
        #self.options.headless = True
        self.driver = webdriver.Firefox(firefox_options=self.options, executable_path=r'Webdriver\geckodriver.exe')


    def HiddenValueExtractor_FieldExecution(self,debug=False):
        Response = self.session.get(self.Loginurl)
        html_tree = BeautifulSoup(Response.text,'html.parser')
        hiddenfield = {"name":"execution"}
        Hidden_ExecutionField = html_tree.find("input",hiddenfield)
        Hidden_Value = Hidden_ExecutionField["value"]
        if(debug or self.debug):
            print("|1| => Hidden Field|Execution : {0}".format(Hidden_Value))
        return Hidden_Value

    def Pre_Requests(self,debug=False):
        #url = "https://uts.primo.exlibrisgroup.com/primaws/suprimaExtLogin?institution=61UTS_INST&lang=en&target-url=https%3A%2F%2Fsearch.lib.uts.edu.au%2Fdiscovery%2Ffulldisplay%3Fdocid%3Dalma991000259909705671%26context%3DL%26vid%3D61UTS_INST%3A61UTS%26lang%3Den%26search_scope%3DMyInst%25255Fand%25255FCI%26adaptor%3DLocal%252520Search%252520Engine%26tab%3DEverything%26query%3Dany%25252Ccontains%25252Cfactiva%252520electronic%252520source%26offset%3D0&authenticationProfile=PRIMOCAS&idpCode=PRIMOCAS&auth=CAS&view=61UTS_INST%3A61UTS&isSilent=false"
        url = "https://search.lib.uts.edu.au/view/action/uresolver.do?operation=resolveService&package_service_id=2490810350005671&institutionId=5671&customerId=5670"
        response = self.session.get(url,verify=False)
        self.Loginurl = response.url
        if(debug or self.debug):
            print("|0| > Login URL Retrived : {0}".format(response.url))

    def Post_FactivaRemoteRequest(self):
        url = "http://global-factiva-com.ezproxy.lib.uts.edu.au/factivalogin/login.asp?xsid="+str(self.xsid)
        payload = {
            "REMOTE_ADDR":"10.146.145.229",
            "HTTP_REFERER": "",
            "TargetSite": "global.factiva.com",
            "InterfaceLanguage": "en",
            "LandingPage": "http://global-factiva-com.ezproxy.lib.uts.edu.au/en/sess/login.asp",
            "ReferedSite": "",
            "emglsssl": '0',
        }
        response = self.session.post(url,data=payload,verify=False)
        return response

    def Post_Factiva_Eproxy_Request(self):
        url = "https://global-factiva-com.ezproxy.lib.uts.edu.au/factivalogin/login.asp?xsid="+str(self.xsid)+"&productname=global"
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
        }
        payload = {
            "REMOTE_ADDR":"10.146.145.229",
            "HTTP_REFERER": "",
            "TargetSite": "global.factiva.com",
            "InterfaceLanguage": "en",
            "LandingPage": "http://global-factiva-com.ezproxy.lib.uts.edu.au/en/sess/login.asp",
            "ReferedSite": "",
            "emglsssl": '0',
        }
        response = self.session.post(url,data=payload,headers=headers,verify=False)
        return response

    def Post_Factiva_Home_Request(self):
        url = "https://global-factiva-com.ezproxy.lib.uts.edu.au/sb/default.aspx?lnep=hp"
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
        }
        payload = {
            "FpIdAjs1008":"Factiva+Login",
        }
        # response = self.session.post(url,data=payload,headers=headers)
        response = self.session.get(url, headers=headers,verify=False)
        return response

    def Login(self,debug=False):
        pre_requests = self.Pre_Requests()
        check_Bool = False
        payload = {
            "_eventId":"submit",
            "geolocation":"",
            "submit": "Login",
            "rememberMe": "true",
            "username": self.username,
            "password": self.password,
            "execution":self.HiddenValueExtractor_FieldExecution()
        }
        AuthenticatedSession = self.session.post(self.Loginurl,data=payload,headers=self.headers,verify=False)
        postrequest_response = None
        if(AuthenticatedSession.history[0].status_code == 302):
            check_Bool = True
            self.xsid = str(AuthenticatedSession.url).split("?")[1].split("=")[1]
            postrequest_response = self.Post_FactivaRemoteRequest()
            post_eproxy_response = self.Post_Factiva_Eproxy_Request()

            self.driver.get(post_eproxy_response.url)
            dict_resp_cookies = post_eproxy_response.cookies.get_dict()
            response_cookies_browser = [{'name': name, 'value': value} for name, value in dict_resp_cookies.items()]
            c = [self.driver.add_cookie(c) for c in response_cookies_browser]
            self.driver.get(post_eproxy_response.url)
            print(self.driver.current_url)
            print(self.driver.get_cookies())

            post_home_response = self.Post_Factiva_Home_Request()

        if(debug or self.debug):
            if(check_Bool):
                print("\n\n|2| > Login Successful")
                print("|$| => Current Window URL : {0}".format(AuthenticatedSession.url))
                print("|$| => Status Code : {0}".format(AuthenticatedSession.status_code))
                print("|$| ==> Status Code History : {0}".format(AuthenticatedSession.history))

                print("\n|3| > Post Request Current URL: {0}".format(postrequest_response.url))
                print("|$| => Post Request Status Code: {0}".format(postrequest_response.status_code))

                print("\n|3| > E-Proxy Post Request Current URL: {0}".format(post_eproxy_response.url))
                print("|$| => E-Proxy Post Request Status Code: {0}".format(post_eproxy_response.status_code))
                print("|$| => E-Proxy Post Request Status Code History: {0}".format(post_eproxy_response.history))

                print("\n|3| > Home Request Current URL: {0}".format(post_home_response.url))
                print("|$| => Home Request Status Code: {0}".format(post_home_response.status_code))
                print("|$| => Response : {0}".format(post_home_response.text))
            else:
                print("\n\n|2| > Login Failed")
                print("|$| => Payload : {0}".format(payload))
                print("|$| => Post URL : {0}".format(self.Loginurl))
                print("|$| ==> Status Code : {0}".format(AuthenticatedSession.status_code))
                print("|$| ==> Status Code History : {0}".format(AuthenticatedSession.history))
                print("|$| ==> Response Text : {0}".format(AuthenticatedSession.text))




obj = Authenticate()
obj.debug = True
obj.Login()