
class Articles_Model():
    def __init__(self):
        self.values = ""
        self.title = ""
        self.leads_source = ""
        self.snippet = ""
        self.FullArticle = ""
        self.CompanyName = ""
        self.ArticleHeader = ""

    def to_dict(self):
        try:
            return {
                'Value': self.values,
                'Article_title': self.title,
                'leads_source': self.leads_source,
                'Article_snippet': self.snippet,
                'full_text': self.FullArticle,
                'article_header':self.ArticleHeader,
                "Company_name":self.CompanyName,
                "Article_Date": self.leads_source.split(",")[1],
            }
        except:
            return {
                'Value': "",
                'Article_title': "",
                'leads_source': "",
                'Article_snippet': "",
                'full_text': "",
                "Company_name":"",
                "Article_Date": "",
            }