import hashlib


class BG_Report:
    def __init__(self):
        self.strClassification = ""
        self.strURL = ""
        self.strTitle = ""
        self.strReportText = ""
        self.strDate = ""

    def setClassification(self, strClassification):
        self.strClassification = strClassification

    def setURL(self, strURL):
        self.strURL = strURL

    def setTitle(self, strTitle):
        self.strTitle = strTitle

    def setReportText(self, strReportText):
        self.strReportText = strReportText

    def setDate(self, strDate):
        self.strDate = strDate

    def setProductID(self, strProductID):
        pass

    def getClassification(self):
        return self.strClassification

    def getURL(self):
        return self.strURL

    def getTitle(self):
        return self.strTitle

    def getReportText(self):
        return self.strReportText

    def getDate(self):
        return self.strDate

    def getSerialNumber(self):
        return "0/12345-22"

    def getProductID(self):
        allText = self.strURL + self.strTitle + self.strDate
        return hashlib.sha1(bytearray(allText.encode(encoding="utf-8"))).hexdigest()
