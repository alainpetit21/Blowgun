from lxml import etree
from src.Model.BG_Report import BG_Report


class BG_QueryResults:
    def __init__(self):
        self.results = []
        self.elResults = etree.Element("results")

    def addReportToResultSet(self, report: BG_Report):
        self.results.append(report)

    def buildXML(self) -> str:

        for report in self.results:
            elReport = etree.Element("result")

            lstName = ["Classification", "SN", "Title", "Date", "ProductID"]
            lstPredicate = [BG_Report.getClassification, BG_Report.getSerialNumber, BG_Report.getTitle, BG_Report.getDate, BG_Report.getProductID]
            for i in range(0, 4):
                elReportColumnName = etree.Element("name")
                elReportColumnName.text = lstName[i]

                elReportColumnValue = etree.Element("value")
                elReportColumnValue.text = (lstPredicate[i])(report)

                elReportColumn = etree.Element("column")
                elReportColumn.append(elReportColumnName)
                elReportColumn.append(elReportColumnValue)

            self.elResults.append(elReport)

        return etree.tostring(self.elResults)

