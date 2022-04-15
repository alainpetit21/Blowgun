import hashlib


class BG_Report:
    def __init__(self):
        self.classification = ""
        self.serial_number = ""
        self.url = ""
        self.title = ""
        self.text = ""
        self.date = ""
        self.product_id = ""

    def setClassification(self, classification):
        self.classification = classification

    def setURL(self, url):
        self.url = url

    def setTitle(self, title):
        self.title = title

    def setReportText(self, text):
        self.text = text

    def setDate(self, strDate):
        self.date = strDate

    def setProductID(self, product_id):
        self.product_id = product_id

    def getClassification(self):
        return self.classification

    def getURL(self):
        return self.url

    def getTitle(self):
        return self.title

    def getReportText(self):
        return self.text

    def getDate(self):
        return self.date

    def getSerialNumber(self):
        return self.serial_number

    def getProductID(self):
        allText = self.url + self.title + self.date
        self.product_id = hashlib.sha1(bytearray(allText.encode(encoding="utf-8"))).hexdigest()
        return self.product_id

    def getReportDatabaseDefinitionList(self) -> str:
        lstVariables = list(vars(self).keys())

        #This object will be all TEXT, so little tweak here for that, in other instance
        #where INT, are going to be used, we'll need to adjust on a case per case
        strRes = " TEXT, ".join(lstVariables)

        return strRes

    def getReportDefinitionList(self) -> list:
        return list(vars(self).keys())

    def getReportValuesList(self) -> list:
        dicVars = vars(self)
        return list(dicVars.values())
